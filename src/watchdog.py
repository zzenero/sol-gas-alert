"""
watchdog.py — Auto-restart bot kalau crash
Dijalankan oleh openclaw cron tiap 10 menit
"""

import subprocess
import logging
import os

log = logging.getLogger(__name__)

def is_bot_running():
    result = subprocess.run(
        ["pgrep", "-f", "src/bot.py"],
        capture_output=True, text=True
    )
    return result.returncode == 0

def restart_bot():
    log.info("🔄 Restarting bot...")
    subprocess.Popen(
        ["python", "src/bot.py"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        stdout=open("logs/bot.log", "a"),
        stderr=subprocess.STDOUT
    )
    log.info("✅ Bot restarted!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not is_bot_running():
        log.warning("⚠️  Bot tidak berjalan, restart...")
        restart_bot()
    else:
        log.info("✅ Bot masih running, tidak perlu restart")