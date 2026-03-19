import aiohttp
import json
from datetime import datetime, timedelta
from app.core.db_helpers import load_token_data, save_token, load_reels, increment_dm_count, append_log
from app.core.config import DEFAULT_MESSAGE

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
            from app.services.token_service import refresh_long_lived_token
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

                if response.status == 200:
                    append_log(f"✅ DM sent successfully to {user_id}")
                    increment_dm_count()
                else:
                    error_msg = result.get("error", {}).get("message", "Unknown error")
                    append_log(f"❌ DM failed for {user_id}: {error_msg}", "ERROR")
                    
                    if "outside of allowed window" in error_msg.lower():
                        append_log("💡 Reminder: The 'Instagram API with Instagram Login' only allows replying to users who have messaged you first within 24 hours.", "INFO")
                return result

    except Exception as e:
        append_log(f"Error in send_dm: {e}", "ERROR")
        return None
