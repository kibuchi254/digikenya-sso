from fastapi import HTTPException
from httpx_oauth.clients.google import GoogleOAuth2
from app.config import config # Assuming this imports your configuration

# --- Initialization of the GoogleOAuth2 Client ---
# The constructor should only contain credentials.
# Scopes and redirect_uri must be passed to the flow methods (e.g., get_authorization_url) 
# in the router, not the constructor.
oauth2_google = GoogleOAuth2(
    client_id=config.OAUTH2_PROVIDERS["google"]["client_id"],
    client_secret=config.OAUTH2_PROVIDERS["google"]["client_secret"],
)

# --- Function to Fetch User Information ---
async def get_user_info(token: dict):
    """
    Fetches user information from Google using the received access token.

    Args:
        token (dict): The token response containing the 'access_token'.

    Returns:
        dict: The user's information payload (e.g., 'sub', 'email', 'name').
    """
    try:
        # Use the internal httpx client for the request
        async with oauth2_google.client as client:
            # The 'userinfo' endpoint URL is standard for Google
            response = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo", 
                headers={"Authorization": f"Bearer {token['access_token']}"}
            )
            
            if response.status_code != 200:
                # Raise an exception if the token is invalid or user info fetch fails
                raise HTTPException(
                    status_code=400, 
                    detail=f"Failed to fetch user info. Google returned status {response.status_code}."
                )
                
            return response.json()
            
    except KeyError:
        # Handle cases where the token dict might not contain 'access_token'
        raise HTTPException(status_code=400, detail="Token response missing 'access_token'.")
    except Exception as e:
        # Catch any other potential errors (like network issues)
        print(f"Error fetching user info: {e}")
        raise HTTPException(status_code=500, detail="Internal error during user info fetch.")