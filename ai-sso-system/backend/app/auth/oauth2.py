from fastapi import HTTPException
from httpx_oauth.clients.google import GoogleOAuth2
from app.config import config

# --- CHANGE HERE: Removed 'redirect_uri' and 'scope' ---
oauth2_google = GoogleOAuth2(
    client_id=config.OAUTH2_PROVIDERS["google"]["client_id"],
    client_secret=config.OAUTH2_PROVIDERS["google"]["client_secret"],
)
# --------------------------------------------------------

async def get_user_info(token: dict):
    # This logic remains correct for fetching user info after a successful token exchange
    async with oauth2_google.client as client:
        response = await client.get("https://www.googleapis.com/oauth2/v3/userinfo", headers={"Authorization": f"Bearer {token['access_token']}"})
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user info")
        return response.json()