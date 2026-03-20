import aiohttp
import logging
import asyncio
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# --- 1. FOLLOWER CHECK ---
async def is_following(target_user_id: str, business_user_id: str, access_token: str) -> bool:
    """Checks if a target user follows the business account."""
    url = f"https://graph.instagram.com/v20.0/{business_user_id}/friendships/{target_user_id}"
    params = {"access_token": access_token}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                result = await response.json()
                if response.status == 200:
                    return result.get("followed_by", False)
                return False
    except Exception as e:
        logger.error(f"Error in is_following: {e}")
        return False

# --- 2. PUBLIC COMMENT REPLY ---
async def public_comment_reply(comment_id: str, message: str, access_token: str) -> bool:
    """Replies publicly to a specific comment."""
    url = f"https://graph.instagram.com/v20.0/{comment_id}/replies"
    payload = {"message": message, "access_token": access_token}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                return response.status == 200
    except Exception as e:
        logger.error(f"Error in public_reply: {e}")
        return False

# --- 3. COMMENT MODERATION (HIDE/DELETE) ---
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

# --- 4. MEDIA INSIGHTS ---
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

# --- 🧪 UNIFIED TEST RUNNER ---
async def run_feature_tests():
    load_dotenv()
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "mock_token")
    print("\n--- 🚀 Starting Future Features Logic Tests ---\n")

    # Test 1: Follower Check
    print(f"[TEST] Follower Check: {await is_following('u1', 'b1', token)}")
    
    # Test 2: Public Reply
    print(f"[TEST] Public Reply: {await public_comment_reply('c1', 'Hello!', token)}")
    
    # Test 3: Moderation
    print(f"[TEST] Moderation (Hide): {await moderate_comment('c1', 'HIDE', token)}")
    
    # Test 4: Insights
    print(f"[TEST] Media Insights: {await get_media_insights('m1', token)}")

    print("\n--- ✅ Logic Tests Finished ---")

if __name__ == "__main__":
    asyncio.run(run_feature_tests())
