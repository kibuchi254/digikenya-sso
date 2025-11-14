import aiohttp
from app.config import config

async def send_sms(phone: str, message: str):
    # Example with Twilio or similar
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(config.SMS_API_KEY.split(":")[0]),
            auth=aiohttp.BasicAuth(config.SMS_API_KEY.split(":")[0], config.SMS_API_KEY.split(":")[1]),
            data={"To": phone, "From": "your_twilio_number", "Body": message}
        ) as resp:
            if resp.status != 201:
                raise Exception("Failed to send SMS")