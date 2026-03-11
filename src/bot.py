"""
╔══════════════════════════════════════════╗
║   SOL Gas Fee Alert Bot 🚨               ║
║   Powered by OpenClaw + Telegram         ║
╚══════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import json
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot
from telegram.constants import ParseMode

load_dotenv()

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CHECK_INTERVAL   = int(os.getenv("CHECK_INTERVAL_SECONDS", 300))

RPC_ENDPOINTS = [
    "https://api.mainnet-beta.solana.com",
    "https://solana-api.projectserum.com",
    "https://rpc.ankr.com/solana",
]

ALERT_LOW_LAMPORTS  = 4000
ALERT_HIGH_LAMPORTS = 10000

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

last_fee_lamports = None
alert_sent_low    = False
alert_sent_high   = False


async def get_recent_fee(session):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getRecentPrioritizationFees",
        "params": []
    }
    for endpoint in RPC_ENDPOINTS:
        try:
            async with session.post(endpoint, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                data = await resp.json()
                fees = data.get("result", [])
                if fees:
                    recent = [f["prioritizationFee"] for f in fees[:5]]
                    avg_priority = sum(recent) // len(recent)
                    base_fee = 5000
                    return {
                        "fee_lamports": base_fee + avg_priority,
                        "base_fee": base_fee,
                        "priority_fee": avg_priority,
                        "endpoint": endpoint
                    }
        except Exception as e:
            log.warning(f"RPC {endpoint} gagal: {e}")
            continue
    return None


def lamports_to_sol(lamports):
    return lamports / 1_000_000_000

def fee_emoji(fee):
    if fee <= ALERT_LOW_LAMPORTS:
        return "🟢"
    elif fee <= 7000:
        return "🟡"
    else:
        return "🔴"

def format_alert_message(fee_data, alert_type):
    fee   = fee_data["fee_lamports"]
    sol   = lamports_to_sol(fee)
    emoji = fee_emoji(fee)
    now   = datetime.now().strftime("%H:%M:%S WIB")
    base  = fee_data.get("base_fee", 5000)
    prio  = fee_data.get("priority_fee", fee - 5000)

    if alert_type == "low":
        header = "🚨 *GAS FEE MURAH SEKARANG\\!*"
        action = "✅ Waktu yang tepat untuk transaksi SOL\\!"
    elif alert_type == "high":
        header = "⚠️ *GAS FEE LAGI TINGGI\\!*"
        action = "⏳ Tahan dulu, tunggu fee turun\\."
    else:
        header = "📊 *UPDATE GAS FEE SOLANA*"
        action = "ℹ️ Fee dalam kondisi normal\\."

    return f"""
{header}

{emoji} *Fee Sekarang:* `{fee:,} lamports`
💰 *Dalam SOL:* `{sol:.9f} SOL`
⚡ *Base Fee:* `{base:,} lamports`
🎯 *Priority Fee:* `{prio:,} lamports`

{action}

🕐 _Update: {now}_
🤖 _Powered by OpenClaw_
    """.strip()


async def send_telegram(bot, message):
    try:
        from telegram.constants import ParseMode
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
        log.info("✅ Pesan Telegram terkirim")
    except Exception as e:
        log.error(f"❌ Gagal kirim Telegram: {e}")


async def main():
    global last_fee_lamports, alert_sent_low, alert_sent_high

    log.info("🚀 SOL Gas Alert Bot starting...")
    bot = Bot(token=TELEGRAM_TOKEN)

    await send_telegram(bot, "🤖 *SOL Gas Fee Alert Bot aktif\\!*\nMonitoring Solana network setiap 5 menit\\.")

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                log.info("🔍 Checking Solana gas fee...")
                fee_data = await get_recent_fee(session)

                if fee_data is None:
                    log.error("Gagal ambil fee data dari semua RPC")
                    await asyncio.sleep(60)
                    continue

                current_fee = fee_data["fee_lamports"]
                log.info(f"💰 Current fee: {current_fee:,} lamports")

                if current_fee <= ALERT_LOW_LAMPORTS and not alert_sent_low:
                    await send_telegram(bot, format_alert_message(fee_data, "low"))
                    alert_sent_low  = True
                    alert_sent_high = False

                elif current_fee >= ALERT_HIGH_LAMPORTS and not alert_sent_high:
                    await send_telegram(bot, format_alert_message(fee_data, "high"))
                    alert_sent_high = True
                    alert_sent_low  = False

                elif ALERT_LOW_LAMPORTS < current_fee < ALERT_HIGH_LAMPORTS:
                    if alert_sent_low or alert_sent_high:
                        await send_telegram(bot, format_alert_message(fee_data, "normal"))
                    alert_sent_low  = False
                    alert_sent_high = False

                last_fee_lamports = current_fee

            except Exception as e:
                log.error(f"Error di main loop: {e}")

            await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())