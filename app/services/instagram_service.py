import aiohttp
from app.utils.file_helpers import load_token_data, load_reels, increment_dm_count
from app.core.config import DEFAULT_MESSAGE

async def send_dm(user_id: str, media_id: str):
    try:
        token_data = load_token_data()
        if not token_data:
            print("✗ No token data found")
            return None

        access_token = token_data.get("access_token")
        ig_account_id = token_data.get("ig_account_id")

        if not access_token or not ig_account_id:
            print("✗ Missing access token or account ID")
            return None

        # Get message for this specific reel
        reels = load_reels()
        reel_data = reels.get(media_id)

        if reel_data:
            message = reel_data.get("message", DEFAULT_MESSAGE)
        else:
            message = DEFAULT_MESSAGE

        # Instagram API endpoint for sending DMs (using Graph API)
        url = f"https://graph.facebook.com/v21.0/{ig_account_id}/messages"

        payload = {
            "recipient": {"id": user_id},
            "message": {"text": message}
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                result = await response.json()
                if response.status == 200:
                    print(f"✓ DM sent to {user_id} for reel {media_id}")
                    increment_dm_count()
                else:
                    print(f"✗ DM failed for {user_id}: {result}")
                return result

    except Exception as e:
        print(f"Error in send_dm: {e}")
        return None
