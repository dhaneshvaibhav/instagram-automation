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
        reels = load_reels()
        reel_data = reels.get(media_id)

        if reel_data:
            message = reel_data.get("message", DEFAULT_MESSAGE)
        else:
            message = DEFAULT_MESSAGE

        # If triggered by a comment, we attempt to use the Private Replies endpoint.
        # NOTE: This endpoint is technically part of the 'Instagram Graph API'.
        # For 'Instagram API with Instagram Login', this may require the 'instagram_manage_messages' permission
        # and for the app to be in 'Live' mode.
        if comment_id:
            # We try graph.facebook.com as it's the primary host for Private Replies
            url = f"https://graph.facebook.com/v25.0/{comment_id}/private_replies"
            payload = {"message": message}
            append_log(f"ℹ Attempting Private Reply to comment {comment_id} via Graph API...")
        else:
            # Standard messaging (requires 24h window)
            url = f"https://graph.instagram.com/v25.0/{ig_account_id}/messages"
            payload = {
                "recipient": {"id": user_id},
                "message": {"text": message}
            }
            append_log(f"ℹ Using Standard Messages endpoint for user {user_id}")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                result = await response.json()
                
                # If Private Reply fails with "Object does not exist", it means this API product 
                # (Instagram Login) doesn't support it. We fall back to standard messaging.
                if comment_id and response.status != 200 and result.get("error", {}).get("code") in [100, 10]:
                    append_log(f"⚠ Private Reply not supported by this API. Falling back to Standard Messaging...", "WARN")
                    url = f"https://graph.instagram.com/v25.0/{ig_account_id}/messages"
                    payload = {
                        "recipient": {"id": user_id},
                        "message": {"text": message}
                    }
                    async with session.post(url, json=payload, headers=headers) as retry_resp:
                        result = await retry_resp.json()
                        response = retry_resp

                if response.status == 200:
                    append_log(f"✅ DM sent successfully to {user_id}")
                    increment_dm_count()
                else:
                    error_msg = result.get("error", {}).get("message", "Unknown error")
                    append_log(f"❌ DM failed for {user_id}: {error_msg}", "ERROR")
                    if "outside of allowed window" in error_msg.lower():
                        append_log("💡 Tip: This API (Instagram Login) requires the user to message you first. For 100% automated replies to any commenter, you must use the 'Instagram Graph API' (with Facebook Page connection).", "INFO")
                return result

    except Exception as e:
        append_log(f"Error in send_dm: {e}", "ERROR")
        return None
