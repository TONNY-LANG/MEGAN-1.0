"""
MEGAN God-Tier Trading System
Module: Telegram/broadcaster/broadcaster.py
Purpose: Professional Telegram notifications + chart explanations
"""

import asyncio
import requests
from Core.monitor.monitor import monitor
from Screenshot.capturer.capturer import ScreenshotCapturer

class TelegramBroadcaster:
    def __init__(self):
        self.token = "YOUR_TELEGRAM_BOT_TOKEN"      # ← Change
        self.chat_id = "YOUR_CHAT_ID"               # ← Change
        self.capturer = ScreenshotCapturer()
        monitor.log_success("TELEGRAM", "Broadcaster Initialized")

    async def send_message(self, text: str, parse_mode="HTML"):
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": parse_mode
            }
            requests.post(url, json=payload)
            monitor.log_success("TELEGRAM", "Message sent", text[:100])
        except Exception as e:
            monitor.log_error("TELEGRAM", e)

    async def send_trade_alert(self, trade_result):
        """Send full professional trade alert with screenshot"""
        status = "✅ PROFIT" if trade_result['pnl'] > 0 else "❌ LOSS"
        
        message = f"""
<b>MEGAN TRADE EXECUTED</b>

{status} | {trade_result['pair']}
PnL: <b>${trade_result['pnl']:.2f}</b>
Reason: {trade_result['reason']}
Time: {trade_result['time']}
Confidence: {trade_result.get('confidence', 85)}%
        """
        
        await self.send_message(message)
        
        # Capture and send chart
        await self.capturer.capture_and_send(trade_result['pair'], message)

# Global instance
broadcaster = TelegramBroadcaster()
