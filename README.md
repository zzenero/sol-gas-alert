\# 🚨 SOL Gas Fee Alert Bot



Monitor Solana network fee secara real-time dan kirim notifikasi otomatis ke Telegram — powered by OpenClaw.



\## Fitur

\- Real-time monitoring setiap 5 menit

\- Alert fee murah (bawah 4000 lamports)

\- Alert fee tinggi (atas 10000 lamports)

\- Auto-restart kalau bot crash

\- 100% gratis, tanpa API key berbayar



\## Cara Install



1\. Install dependencies

pip install -r requirements.txt



2\. Setup Telegram Bot

\- Chat @BotFather di Telegram → /newbot → copy token

\- Chat @userinfobot → copy Chat ID



3\. Buat file .env

\- Copy .env.example jadi .env

\- Isi TELEGRAM\_TOKEN dan TELEGRAM\_CHAT\_ID



4\. Jalankan bot

python src/bot.py



\## OpenClaw Integration

openclaw cron import openclaw-cron.yaml

openclaw gateway start



\## Tech Stack

\- Python 3.11+

\- aiohttp

\- python-telegram-bot

\- OpenClaw Cron

\- Solana Public RPC

