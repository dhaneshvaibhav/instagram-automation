import aiohttp
from app.core.config import APP_ID, APP_SECRET, REDIRECT_URI

async def exchange_code_for_token(code: str):
    code = code.replace("#_", "").strip()
    # Using Graph API (Facebook) for Business App
    url = "https://graph.facebook.com/v21.0/oauth/access_token"
    params = {
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            result = await response.json()
            print("Short token response:", result)
            if response.status != 200:
                raise Exception(f"Token exchange failed: {result}")
            return result

async def exchange_short_for_long_token(short_token: str):
    # Using Graph API (Facebook) for Business App
    url = "https://graph.facebook.com/v21.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": short_token
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            result = await response.json()
            print("Long token response:", result)
            if response.status != 200:
                raise Exception(f"Long token exchange failed: {result}")
            return result

async def fetch_ig_profile(access_token: str):
    # For Business apps, we need to find the Instagram ID linked to a Facebook Page
    # Step 1: Get the Facebook Pages linked to this user
    url = "https://graph.facebook.com/v21.0/me/accounts"
    params = {
        "fields": "id,name,instagram_business_account{id,username}",
        "access_token": access_token
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            result = await response.json()
            print("Pages response:", result)
            
            if response.status != 200:
                raise Exception(f"Failed to fetch linked pages: {result}")
            
            # Step 2: Find a page that has a linked Instagram Business Account
            pages = result.get("data", [])
            for page in pages:
                ig_account = page.get("instagram_business_account")
                if ig_account:
                    return {
                        "id": ig_account.get("id"),
                        "username": ig_account.get("username")
                    }
            
            raise Exception("No Instagram Business Account linked to your Facebook Pages. Please link your Instagram Business account to a Facebook Page.")
