import aiohttp
from fastapi import APIRouter, HTTPException
from app.utils.file_helpers import load_stats, load_reels, load_token_data, save_token

router = APIRouter(tags=["stats"])

@router.get('/api/stats')
async def get_stats():
    stats = load_stats()
    reels = load_reels()
    return {
        "total_reels": len(reels),
        "dms_sent_today": stats.get("dms_today", 0),
        "total_dms": stats.get("total_dms", 0)
    }

@router.get('/api/refresh-token')
async def refresh_token():
    token_data = load_token_data()
    if not token_data:
        raise HTTPException(status_code=401, detail="Not authenticated")

    current_token = token_data.get("access_token")

    try:
        url = "https://graph.instagram.com/refresh_access_token"
        params = {
            "grant_type": "ig_refresh_token",
            "access_token": current_token
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                result = await response.json()
                if response.status == 200:
                    new_token = result.get("access_token")
                    save_token(
                        new_token,
                        token_data.get("ig_account_id"),
                        token_data.get("username")
                    )
                    print("✓ Token refreshed")
                    return {"status": "refreshed", "expires_at": load_token_data().get("expires_at")}
                else:
                    raise HTTPException(status_code=400, detail=f"Refresh failed: {result}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/health')
async def health_check():
    token_data = load_token_data()
    return {
        "status": "healthy",
        "instagram_connected": token_data is not None,
        "total_reels": len(load_reels())
    }
