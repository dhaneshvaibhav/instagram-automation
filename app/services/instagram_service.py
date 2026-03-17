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

        # To send a DM to a commenter (even if they haven't messaged you first),
        # we MUST use the Private Replies endpoint. This creates a DM in their inbox.
        if comment_id:
            # We use graph.instagram.com for the Private Replies endpoint
            url = f"https://graph.instagram.com/v25.0/{comment_id}/private_replies"
            payload = {"message": message}
            append_log(f"ℹ Attempting Private Reply (DM) to comment {comment_id} via Instagram host...")
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
                    
                    # If Private Reply failed, we fall back to standard messaging as a last resort
                    if comment_id and response.status != 200:
                        append_log(f"⚠ Private Reply failed, falling back to Standard Messaging...", "WARN")
                        url = f"https://graph.instagram.com/v25.0/{ig_account_id}/messages"
                        payload = {
                            "recipient": {"id": user_id},
                            "message": {"text": message}
                        }
                        async with session.post(url, json=payload, headers=headers) as retry_resp:
                            result = await retry_resp.json()
                            if retry_resp.status == 200:
                                append_log(f"✅ DM sent via Standard Messaging fallback")
                                increment_dm_count()
                            else:
                                append_log(f"❌ Fallback also failed: {result.get('error', {}).get('message')}", "ERROR")
                return result

    except Exception as e:
        append_log(f"Error in send_dm: {e}", "ERROR")
        return None
