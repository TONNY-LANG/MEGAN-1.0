import smtplib
from email.mime.text import MIMEText
from datetime import datetime

class MEGANSMSAlert:
    def __init__(self, phone_number, carrier="att"):
        self.phone = phone_number
        self.carrier = carrier
        self.gateways = {
            "att": "@txt.att.net",
            "verizon": "@vtext.com",
            "tmobile": "@tmomail.net",
            "gmail": "@txt.att.net",  # Change as needed
        }
        self.email_gateway = self.phone + self.gateways.get(carrier, "@txt.att.net")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send(self, trade_type="success", pnl=0.0, pair="EURUSD", reason=""):
        status = "✅ PROFIT" if trade_type == "success" else "❌ LOSS"
        message = f"MEGAN Trade Alert\n{status}: {pair} | PnL: ${pnl:.2f}\nReason: {reason}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        try:
            msg = MIMEText(message)
            msg["Subject"] = f"MEGAN {status} Trade"
            msg["From"] = "megan@trading.bot"
            msg["To"] = self.email_gateway

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login("YOUR_GMAIL@gmail.com", "YOUR_APP_PASSWORD")
                server.send_message(msg)

            print(f"[SMS] {status} alert sent via Email-to-SMS")
            return True
        except Exception as e:
            print(f"[SMS Error] {e}")
            return False

# Usage example
if __name__ == "__main__":
    alert = MEGANSMSAlert("1234567890", "att")
    alert.send("success", 245.50, "EURUSD", "Strong BOS + FVG fill")
