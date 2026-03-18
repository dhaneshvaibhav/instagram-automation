import aiohttp
from app.utils.file_helpers import load_token_data, load_reels, increment_dm_count, append_log
from app.core.config import DEFAULT_MESSAGE
from app.services.ai_service import analyze_media_and_generate_reply

async def send_dm(user_id: str, media_id: str, comment_id: str = None, comment_text: str = None):
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

        # Get configuration for this specific reel
        reels = load_reels(ig_account_id)
        reel_data = reels.get(media_id)

        message = DEFAULT_MESSAGE
        if reel_data:
            if reel_data.get("ai_enabled") and comment_text:
                append_log(f"🤖 Generating AI-personalized DM for comment: '{comment_text}'")
                ai_message = await analyze_media_and_generate_reply(
                    comment_text=comment_text,
                    ai_context=reel_data.get("ai_context"),
                    ai_summary=reel_data.get("ai_summary"),
                    is_dm=True
                )
                if ai_message:
                    message = ai_message
                else:
                    message = reel_data.get("dm_message") or DEFAULT_MESSAGE
            else:
                message = reel_data.get("dm_message") or DEFAULT_MESSAGE

        url = f"https://graph.instagram.com/v25.0/{ig_account_id}/messages"
        payload = {
            "recipient": {"comment_id": comment_id} if comment_id else {"id": user_id},
            "message": {"text": message}
        }
        
        append_log(f"ℹ Sending DM to {user_id} (comment_id: {comment_id})")

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
                return result

    except Exception as e:
        append_log(f"Error in send_dm: {e}", "ERROR")
        return None

async def send_public_reply(comment_id: str, media_id: str, comment_text: str = None):
    try:
        token_data = load_token_data()
        if not token_data:
            append_log("✗ No token data found for public reply", "ERROR")
            return None

        access_token = token_data.get("access_token")
        ig_account_id = token_data.get("ig_account_id")

        if not access_token:
            append_log("✗ Missing access token for public reply", "ERROR")
            return None

        # Get configuration for this specific reel
        reels = load_reels(ig_account_id)
        reel_data = reels.get(media_id)

        reply_text = "Thanks for your comment! Check your DMs 📩"
        if reel_data:
            if reel_data.get("ai_enabled") and comment_text:
                append_log(f"🤖 Generating AI-personalized public reply for comment: '{comment_text}'")
                ai_reply = await analyze_media_and_generate_reply(
                    comment_text=comment_text,
                    ai_context=reel_data.get("ai_context"),
                    ai_summary=reel_data.get("ai_summary"),
                    is_dm=False
                )
                if ai_reply:
                    reply_text = ai_reply
                else:
                    reply_text = reel_data.get("public_reply") or reply_text
            else:
                reply_text = reel_data.get("public_reply") or reply_text

        # API endpoint for replying to a comment
        url = f"https://graph.instagram.com/v25.0/{comment_id}/replies"
        params = {
            "message": reply_text,
            "access_token": access_token
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                result = await response.json()
                if response.status == 200:
                    append_log(f"✅ Public reply sent successfully to comment {comment_id}")
                else:
                    error_msg = result.get("error", {}).get("message", "Unknown error")
                    append_log(f"❌ Public reply failed for comment {comment_id}: {error_msg}", "ERROR")
                return result

    except Exception as e:
        append_log(f"Error in send_public_reply: {e}", "ERROR")
        return None
