import aiohttp
from app.core.config import APP_ID, APP_SECRET, REDIRECT_URI

async def exchange_code_for_token(code: str):
    # Get only the short-lived token (1 hour) using the Instagram endpoint
    url = "https://api.instagram.com/oauth/access_token"
    data = {
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code.replace("#_", "").strip()
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            result = await response.json()
            if response.status != 200:
                print(f"✗ Token exchange failed: {result}")
                raise Exception(f"Token exchange failed: {result}")
            
            # Log success and the ENTIRE token for verification as requested
            token = result.get("access_token")
            if token:
                print(f"✓ Access Token received: {token}")
            else:
                print("✗ Response received but access_token is missing")
                
            # This returns both access_token and user_id directly
            return result

async def get_long_lived_token(short_lived_token: str):
    # Documentation: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/business-login#get-a-long-lived-access-token
    # STRICLTY following the literal example in the documentation:
    # GET https://graph.instagram.com/access_token
    #   ?grant_type=ig_exchange_token
    #   &client_secret={instagram-app-secret}
    #   &access_token={short-lived-access-token}
    
    url = "https://graph.instagram.com/access_token"
    params = {
        "grant_type": "ig_exchange_token",
        "client_secret": APP_SECRET,
        "access_token": short_lived_token
    }
    
    async with aiohttp.ClientSession() as session:
        print(f"Attempting literal documentation exchange: {url}")
        async with session.get(url, params=params) as response:
            result = await response.json()
            if response.status == 200:
                print("✓ Long-lived token received!")
                return result
            
            # If literal fails, try with method=GET override just in case
            print(f"⚠ Literal GET failed: {result.get('error', {}).get('message')}")
            params["method"] = "GET"
            async with session.get(url, params=params) as method_response:
                method_result = await method_response.json()
                if method_response.status == 200:
                    print("✓ Long-lived token received (with method=GET)!")
                    return method_result
                
                print(f"✗ Both literal and method-override failed: {method_result}")
                return None

async def refresh_long_lived_token(long_lived_token: str):
    # Documentation: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/business-login#refresh-a-long-lived-access-token
    # Literal example: GET https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token={long-lived-access-token}
    url = "https://graph.instagram.com/refresh_access_token"
    params = {
        "grant_type": "ig_refresh_token",
        "access_token": long_lived_token
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            result = await response.json()
            if response.status == 200:
                print("✓ Token refreshed!")
                return result
            return None

async def fetch_ig_profile(access_token: str, user_id: str = None):
    # Documentation: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/get-started#fields
    # Requesting all documented professional fields + biography (if available)
    url = "https://graph.instagram.com/v25.0/me"
    fields = "id,user_id,username,name,account_type,profile_picture_url,followers_count,follows_count,media_count,biography"
    params = {
        "fields": fields,
        "access_token": access_token
    }
    
    async with aiohttp.ClientSession() as session:
        print(f"Attempting profile fetch with all fields: {url}")
        async with session.get(url, params=params) as response:
            result = await response.json()
            if response.status == 200:
                print(f"✓ Full profile fetch successful!")
                data = result.get("data", [result])[0] if isinstance(result.get("data"), list) else result
                return {
                    "id": data.get("user_id") or data.get("id"),
                    "username": data.get("username", "User"),
                    "name": data.get("name") or data.get("username"),
                    "account_type": data.get("account_type"),
                    "profile_picture_url": data.get("profile_picture_url"),
                    "followers_count": data.get("followers_count", 0),
                    "follows_count": data.get("follows_count", 0),
                    "media_count": data.get("media_count", 0),
                    "biography": data.get("biography", "")
                }
            
            # If full fetch fails (e.g. biography not supported), fallback to documented fields
            print(f"⚠ Full fetch failed: {result.get('error', {}).get('message')}. Retrying with documented fields...")
            params["fields"] = "id,user_id,username,name,account_type,profile_picture_url,followers_count,follows_count,media_count"
            async with session.get(url, params=params) as doc_response:
                doc_result = await doc_response.json()
                if doc_response.status == 200:
                    print(f"✓ Documented profile fetch successful!")
                    data = doc_result.get("data", [doc_result])[0] if isinstance(doc_result.get("data"), list) else doc_result
                    return {
                        "id": data.get("user_id") or data.get("id"),
                        "username": data.get("username", "User"),
                        "name": data.get("name") or data.get("username"),
                        "account_type": data.get("account_type"),
                        "profile_picture_url": data.get("profile_picture_url"),
                        "followers_count": data.get("followers_count", 0),
                        "follows_count": data.get("follows_count", 0),
                        "media_count": data.get("media_count", 0)
                    }

    raise Exception(f"All profile fetch attempts failed. Error: {result.get('error', {}).get('message')}")

async def fetch_ig_media(access_token: str, user_id: str):
    # Documentation: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/get-started#get-an-app-user-s-media-objects
    # URL: https://graph.instagram.com/v25.0/{user_id}/media
    url = f"https://graph.instagram.com/v25.0/{user_id}/media"
    params = {
        "fields": "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp",
        "access_token": access_token
    }
    
    async with aiohttp.ClientSession() as session:
        print(f"Attempting media fetch for ID {user_id}: {url}")
        async with session.get(url, params=params) as response:
            result = await response.json()
            if response.status == 200:
                print(f"✓ Media fetch successful! Found {len(result.get('data', []))} items.")
                return result.get("data", [])
            
            print(f"✗ Media fetch failed: {result.get('error', {}).get('message')}")
            return []

async def fetch_single_media(access_token: str, media_id: str):
    """
    Fetches details for a single media object.
    Documentation: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/get-started#get-media-data
    """
    url = f"https://graph.instagram.com/v25.0/{media_id}"
    params = {
        "fields": "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp",
        "access_token": access_token
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            result = await response.json()
            if response.status == 200:
                return result
            
            print(f"✗ Single media fetch failed for {media_id}: {result.get('error', {}).get('message')}")
            return None
