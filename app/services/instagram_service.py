import aiohttp
from app.utils.file_helpers import load_token_data, load_reels, increment_dm_count, append_log
from app.core.config import DEFAULT_MESSAGE

async def send_dm(user_id: str, media_id: str, comment_id: str = None):
    try:
        token_data = load_token_data()
        if not token_data:
            append_log("✗ No token data found", "ERROR")
            return None

        access_token = token_data.get("access_token")
        ig_account_id = token_data.get("ig_account_id")

        if not access_token or not ig_account_id:
            append_log("✗ Missing access token or account ID", "ERROR")
            return None

        # Get message for this specific reel
        reels = load_reels(ig_account_id)
        reel_data = reels.get(media_id)

        if reel_data:
            message = reel_data.get("message", DEFAULT_MESSAGE)
        else:
            message = DEFAULT_MESSAGE

        # This API (Instagram Login) supports the 'comment_id' recipient type
        # for automated DMs in response to a comment.
        if comment_id:
            url = f"https://graph.instagram.com/v25.0/{ig_account_id}/messages"
            payload = {
                "recipient": {"comment_id": comment_id},
                "message": {"text": message}
            }
            append_log(f"ℹ Using Instagram Messaging endpoint with comment_id {comment_id}")
        else:
            url = f"https://graph.instagram.com/v25.0/{ig_account_id}/messages"
            payload = {
                "recipient": {"id": user_id},
                "message": {"text": message}
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
