import smtplib
from email.mime.text import MIMEText
from app.config import config
import asyncio

async def send_email(to: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = config.EMAIL_USERNAME
    msg["To"] = to

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _send_email_sync, msg, to)

def _send_email_sync(msg, to):
    with smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT) as server:
        server.starttls()
        server.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
        server.sendmail(config.EMAIL_USERNAME, to, msg.as_string())

async def send_otp_email(to: str, otp: int):
    await send_email(to, "Your OTP Code", f"Your OTP is {otp}. It expires in 5 minutes.")

async def send_activation_email(to: str):
    await send_email(to, "Activate Your Account", "Please click the link to activate your account: [activation_link]")