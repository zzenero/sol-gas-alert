# 🚨 SOL Gas Fee Alert Bot

**Monitor Solana network fee secara real-time dan kirim notifikasi otomatis ke Telegram**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Solana](https://img.shields.io/badge/Solana-Mainnet-9945FF?style=for-the-badge&logo=solana&logoColor=white)](https://solana.com)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026-FF4500?style=for-the-badge)](https://openclaw.ai)
[![License](https://img.shields.io/badge/MIT-22C55E?style=for-the-badge)](LICENSE)

<img src="https://img.shields.io/badge/status-active-success?style=flat-square" />
<img src="https://img.shields.io/badge/free-no%20API%20key%20needed-blue?style=flat-square" />

</div>

---

## 📱 Preview
```
🚨 GAS FEE MURAH SEKARANG!

🟢 Fee Sekarang : 3,800 lamports
💰 Dalam SOL   : 0.000003800 SOL
⚡ Base Fee    : 5,000 lamports
🎯 Priority Fee: 0 lamports

✅ Waktu yang tepat untuk transaksi SOL!

🕐 Update: 08:32:14 WIB
🤖 Powered by OpenClaw
```

---

## ✨ Fitur Utama

| Fitur | Keterangan |
|-------|-----------|
| 🟢 Alert Fee Murah | Notif otomatis saat fee ≤ 4,000 lamports |
| 🔴 Alert Fee Tinggi | Notif otomatis saat fee ≥ 10,000 lamports |
| 🔄 Multi-RPC Fallback | Auto ganti endpoint kalau RPC down |
| 🛡️ Auto Watchdog | Bot restart otomatis kalau crash |
| ⚡ OpenClaw Agent | Bisa diajak ngobrol via Telegram |
| 🆓 100% Gratis | Tidak butuh API key berbayar |

---

## 🛠️ Tech Stack
```
┌─────────────────────────────────────────┐
│  Python 3.11+     → Core bot logic      │
│  aiohttp          → Async HTTP requests │
│  python-telegram-bot → Notif Telegram   │
│  OpenClaw         → Agent & Scheduler   │
│  Solana Public RPC → Data fee gratis    │
└─────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone repo
```bash
git clone https://github.com/zzenero/sol-gas-alert
cd sol-gas-alert
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Telegram Bot
```
1. Chat @BotFather → /newbot → copy token
2. Chat @userinfobot → copy Chat ID kamu
```

### 4. Setup environment
```bash
cp .env.example .env
# Edit .env, isi token & chat ID
```

### 5. Setup AI Model (pilih salah satu)

#### Option A — OpenAI (GPT-4o-mini)
```bash
# Daftar & beli credit di https://platform.openai.com/settings/billing
# Buat API key di https://platform.openai.com/api-keys

openclaw models auth paste-token --provider openai
# Paste API key kamu (sk-proj-...)

openclaw models set openai/gpt-4o-mini
```

#### Option B — Anthropic (Gratis $5 credit)
```bash
# Daftar gratis di https://console.anthropic.com
# Buat API key → sk-ant-...

openclaw models auth paste-token --provider anthropic
# Paste API key kamu (sk-ant-...)
```

### 6. Jalankan!
```bash
# Tanpa OpenClaw
python src/bot.py

# Dengan OpenClaw Agent (recommended)
openclaw configure
openclaw gateway
```

---

## ⚙️ Konfigurasi

Edit nilai threshold di `src/bot.py`:
```python
ALERT_LOW_LAMPORTS  = 4000   # 🟢 Alert fee murah
ALERT_HIGH_LAMPORTS = 10000  # 🔴 Alert fee mahal
CHECK_INTERVAL      = 300    # ⏱️ Cek tiap 5 menit
```

---

## 📁 Struktur Project
```
sol-gas-alert/
├── 📂 src/
│   ├── 🐍 bot.py          # Main bot logic
│   └── 🐍 watchdog.py     # Auto-restart script
├── 📂 logs/               # Log files
├── ⚙️  openclaw-cron.yaml  # OpenClaw scheduler
├── 📦 requirements.txt    # Dependencies
├── 🔒 .env.example        # Config template
└── 📖 README.md
```

---

## 🔄 Cara Kerja
```
OpenClaw Cron
     │
     │  polling tiap 5 menit
     ▼
Solana Public RPC ──► bot.py ──► analisis fee
                                      │
                          ┌───────────┴───────────┐
                          │                       │
                     fee murah?              fee mahal?
                          │                       │
                          ▼                       ▼
                   🟢 Alert ke               🔴 Alert ke
                    Telegram                  Telegram
```

---

## 🤖 OpenClaw Integration
```bash
openclaw configure
openclaw gateway

# Chat di Telegram!
# "Berapa gas fee SOL sekarang?"
# "Kapan waktu terbaik untuk transaksi?"
```

---

## 📄 License

MIT License — bebas dipakai dan dimodifikasi.

---

<div align="center">

Made with ❤️ by [zzenero](https://github.com/zzenero)

⭐ **Star repo ini kalau bermanfaat!** ⭐

</div>