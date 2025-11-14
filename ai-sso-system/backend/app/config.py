import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/ai_sso_db")
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    SMS_API_KEY = os.getenv("SMS_API_KEY")  # e.g., Twilio
    OAUTH2_PROVIDERS = {
        "google": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
        },
        # Add more providers as needed
    }

config = Config()