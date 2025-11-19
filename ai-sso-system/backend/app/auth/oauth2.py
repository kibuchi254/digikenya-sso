from fastapi import HTTPException
from httpx_oauth.clients.google import GoogleOAuth2
from app.config import config

# Only client_id and client_secret should be in the constructor
oauth2_google = GoogleOAuth2(
    client_id=config.OAUTH2_PROVIDERS["google"]["client_id"],
    client_secret=config.OAUTH2_PROVIDERS["google"]["client_secret"],
    # redirect_uri and scope must be passed to the flow methods, not the constructor.
)

async def get_user_info(token: dict):
    async with oauth2_google.client as client:
        # Note: Scopes are needed earlier to get the 'access_token', but
        # this part of the code is correct for fetching user info using the token.
        response = await client.get("https://www.googleapis.com/oauth2/v3/userinfo", headers={"Authorization": f"Bearer {token['access_token']}"})
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user info")
        return response.json()