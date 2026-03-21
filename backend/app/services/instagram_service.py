import aiohttp
import json
import logging
from datetime import datetime, timedelta
from app.core.db_helpers import load_token_data, save_token, load_reels, increment_dm_count, append_log
from app.core.config import DEFAULT_MESSAGE, APP_ID, APP_SECRET, REDIRECT_URI

logger = logging.getLogger(__name__)

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
                logger.error(f"✗ Token exchange failed: {result}")
                raise Exception(f"Token exchange failed: {result}")
            
            token = result.get("access_token")
            if token:
                logger.info(f"✓ Access Token received.")
            else:
                logger.warning("✗ Response received but access_token is missing")
                
            return result

async def get_long_lived_token(short_lived_token: str):
    url = "https://graph.instagram.com/access_token"
    params = {
        "grant_type": "ig_exchange_token",
        "client_secret": APP_SECRET,
        "access_token": short_lived_token
    }
    
    async with aiohttp.ClientSession() as session:
        logger.info(f"Attempting long-lived token exchange...")
        async with session.get(url, params=params) as response:
            result = await response.json()
            if response.status == 200:
                logger.info("✓ Long-lived token received!")
                return result
            
            logger.warning(f"⚠ Literal GET failed: {result.get('error', {}).get('message')}")
            params["method"] = "GET"
            async with session.get(url, params=params) as method_response:
                method_result = await method_response.json()
                if method_response.status == 200:
                    logger.info("✓ Long-lived token received (with method=GET)!")
                    return method_result
                
                logger.error(f"✗ Both literal and method-override failed: {method_result}")
                return None

async def refresh_long_lived_token(long_lived_token: str):
    url = "https://graph.instagram.com/refresh_access_token"
    params = {
        "grant_type": "ig_refresh_token",
        "access_token": long_lived_token
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            result = await response.json()
            if response.status == 200:
                logger.info("✓ Token refreshed!")
                return result
            return None

async def fetch_ig_profile(access_token: str, user_id: str = None):
    url = "https://graph.instagram.com/v25.0/me"
    fields = "id,user_id,username,name,account_type,profile_picture_url,followers_count,follows_count,media_count,biography"
    params = {
        "fields": fields,
        "access_token": access_token
    }
    
    async with aiohttp.ClientSession() as session:
        logger.info(f"Attempting profile fetch...")
        async with session.get(url, params=params) as response:
            result = await response.json()
            if response.status == 200:
                logger.info(f"✓ Full profile fetch successful!")
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
            
            logger.warning(f"⚠ Full fetch failed: {result.get('error', {}).get('message')}. Retrying with documented fields...")
            params["fields"] = "id,user_id,username,name,account_type,profile_picture_url,followers_count,follows_count,media_count"
            async with session.get(url, params=params) as doc_response:
                doc_result = await doc_response.json()
                if doc_response.status == 200:
                    logger.info(f"✓ Documented profile fetch successful!")
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
    url = f"https://graph.instagram.com/v25.0/{user_id}/media"
    params = {
        "fields": "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp",
        "access_token": access_token
    }
    
    async with aiohttp.ClientSession() as session:
        logger.info(f"Attempting media fetch for ID {user_id}...")
        async with session.get(url, params=params) as response:
            result = await response.json()
            if response.status == 200:
                logger.info(f"✓ Media fetch successful! Found {len(result.get('data', []))} items.")
                return result.get("data", [])
            
            logger.error(f"✗ Media fetch failed: {result.get('error', {}).get('message')}")
            return []

async def get_valid_token():
    """Returns a valid access token, refreshing it if it's close to expiring."""
    token_data = load_token_data()
    if not token_data:
        return None

    access_token = token_data.get("access_token")
    expires_at = token_data.get("expires_at")
    
    if expires_at:
        expiry = datetime.fromisoformat(expires_at)
        # If expired or expiring within 7 days, try to refresh
        if (expiry - datetime.now()) < timedelta(days=7):
            refresh_data = await refresh_long_lived_token(access_token)
            if refresh_data:
                access_token = refresh_data.get("access_token")
                expires_in = refresh_data.get("expires_in", 5184000)
                token_data["access_token"] = access_token
                token_data["expires_at"] = (datetime.now() + timedelta(seconds=expires_in)).isoformat()
                save_token(token_data)
                append_log("✓ Token automatically refreshed.")
    
    return access_token

async def send_dm(user_id: str, media_id: str, comment_id: str = None):
    try:
        access_token = await get_valid_token()
        token_data = load_token_data() # Refresh data after potential update
        
        if not access_token or not token_data:
            append_log("✗ No valid token found", "ERROR")
            return None

        ig_account_id = token_data.get("ig_account_id")
        if not ig_account_id:
            append_log("✗ Missing account ID", "ERROR")
            return None

        # Get message for this specific reel
        reels = load_reels(ig_account_id)
        reel_data = reels.get(media_id)

        if reel_data:
            message_text = reel_data.get("message", DEFAULT_MESSAGE)
            buttons_data = reel_data.get("buttons")
        else:
            message_text = DEFAULT_MESSAGE
            buttons_data = None

        # Build the message payload
        message_payload = {}
        if buttons_data:
            try:
                buttons = json.loads(buttons_data) if isinstance(buttons_data, str) else buttons_data
                if buttons and len(buttons) > 0:
                    message_payload = {
                        "attachment": {
                            "type": "template",
                            "payload": {
                                "template_type": "button",
                                "text": message_text,
                                "buttons": buttons
                            }
                        }
                    }
                else:
                    message_payload = {"text": message_text}
            except Exception as e:
                append_log(f"⚠ Error parsing buttons: {e}. Falling back to text message.", "WARNING")
                message_payload = {"text": message_text}
        else:
            message_payload = {"text": message_text}

        # This API (Instagram Login) supports the 'comment_id' recipient type
        # for automated DMs in response to a comment.
        if comment_id:
            url = f"https://graph.instagram.com/v25.0/{ig_account_id}/messages"
            payload = {
                "recipient": {"comment_id": comment_id},
                "message": message_payload
            }
            append_log(f"ℹ Using Instagram Messaging endpoint with comment_id {comment_id}")
        else:
            url = f"https://graph.instagram.com/v25.0/{ig_account_id}/messages"
            payload = {
                "recipient": {"id": user_id},
                "message": message_payload
            }
            append_log(f"ℹ Using standard user_id messaging endpoint for user {user_id}")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                result = await response.json()
                if response.status in [200, 201]:
                    append_log(f"✅ DM sent successfully to {user_id}!")
                    increment_dm_count()
                    return result
                else:
                    error_msg = result.get("error", {}).get("message", "Unknown error")
                    append_log(f"✗ Failed to send DM: {error_msg}", "ERROR")
                    return None

    except Exception as e:
        append_log(f"✗ Exception in send_dm: {e}", "ERROR")
        return None

# --- FOLLOWER CHECK ---
async def check_is_follower(target_user_id: str, business_user_id: str, access_token: str) -> bool:
    """
    Checks if a target user follows the business account using the Graph API.
    """
    url = f"https://graph.instagram.com/v20.0/{business_user_id}/friendships/{target_user_id}"
    params = {"access_token": access_token}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                result = await response.json()
                if response.status == 200:
                    is_follower = result.get("followed_by", False)
                    if is_follower:
                        append_log(f"👤 User {target_user_id} IS a follower.")
                    else:
                        append_log(f"👤 User {target_user_id} is NOT a follower.")
                    return is_follower
                
                logger.error(f"Friendship check failed: {result}")
                return False
    except Exception as e:
        logger.error(f"Error checking follower status: {e}")
        return False

# --- ENGAGEMENT ACTIONS ---

async def like_comment(comment_id: str, access_token: str) -> bool:
    """Likes a specific comment."""
    url = f"https://graph.instagram.com/v20.0/{comment_id}"
    payload = {"user_likes": True, "access_token": access_token}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload) as response:
                result = await response.json()
                if response.status == 200 and result.get("success"):
                    append_log(f"❤️ Successfully liked comment {comment_id}")
                    return True
                append_log(f"⚠️ Failed to like comment {comment_id}: {result}", "WARNING")
                return False
    except Exception as e:
        logger.error(f"Error in like_comment: {e}")
        return False

async def public_comment_reply(comment_id: str, message: str, access_token: str) -> bool:
    """Replies publicly to a specific comment."""
    url = f"https://graph.instagram.com/v20.0/{comment_id}/replies"
    payload = {"message": message, "access_token": access_token}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload) as response:
                result = await response.json()
                if response.status == 200:
                    append_log(f"💬 Successfully replied to comment {comment_id}")
                    return True
                append_log(f"⚠️ Failed to reply to comment {comment_id}: {result}", "WARNING")
                return False
    except Exception as e:
        logger.error(f"Error in public_reply: {e}")
        return False

# --- COMMENT MODERATION (HIDE/DELETE) ---
async def moderate_comment(comment_id: str, action: str, access_token: str) -> bool:
    """Hides or Deletes a comment. Action: 'HIDE' or 'DELETE'."""
    url = f"https://graph.instagram.com/v20.0/{comment_id}"
    try:
        async with aiohttp.ClientSession() as session:
            if action.upper() == "HIDE":
                payload = {"hide": True, "access_token": access_token}
                async with session.post(url, json=payload) as response:
                    return response.status == 200
            elif action.upper() == "DELETE":
                params = {"access_token": access_token}
                async with session.delete(url, params=params) as response:
                    return response.status == 200
        return False
    except Exception as e:
        logger.error(f"Error in moderation: {e}")
        return False

# --- MEDIA INSIGHTS ---
async def get_media_insights(media_id: str, access_token: str) -> dict:
    """Fetches reach, impressions, and engagement for a specific Reel/Post."""
    url = f"https://graph.instagram.com/v20.0/{media_id}/insights"
    params = {
        "metric": "reach,impressions,engagement,saved",
        "access_token": access_token
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return {}
    except Exception as e:
        logger.error(f"Error fetching insights: {e}")
        return {}
