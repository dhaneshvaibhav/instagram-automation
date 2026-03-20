from datetime import datetime, timedelta
from fastapi import HTTPException
from app.models.reel import ReelData, ReelUpdate
from app.core.db_helpers import load_reels, save_reels, load_token_data
from app.services.instagram_service import send_dm, fetch_ig_media

# In-memory cache for media results to improve response time
_media_cache = {}
CACHE_EXPIRY_MINUTES = 5

async def get_instagram_reels():
    token_data = load_token_data()
    if not token_data or not token_data.get("access_token"):
        raise HTTPException(status_code=401, detail="Not connected")
    
    ig_id = token_data["ig_account_id"]
    now = datetime.now()
    
    # Check cache first
    if ig_id in _media_cache:
        cached_reels, expiry = _media_cache[ig_id]
        if now < expiry:
            return {"reels": cached_reels}
    
    # Cache miss or expired
    reels = await fetch_ig_media(
        token_data["access_token"], 
        token_data["ig_account_id"]
    )
    
    # Update cache
    _media_cache[ig_id] = (reels, now + timedelta(minutes=CACHE_EXPIRY_MINUTES))
    
    return {"reels": reels}

async def test_dm(data: dict):
    user_id = data.get("user_id")
    media_id = data.get("media_id")
    
    token_data = load_token_data()
    if not token_data:
        raise HTTPException(status_code=401, detail="Not connected")

    if not user_id or user_id.lower() == 'me':
        user_id = token_data.get("ig_account_id")
    
    if not user_id or not media_id:
        raise HTTPException(status_code=400, detail="Missing user_id or media_id")
        
    result = await send_dm(user_id, media_id)
    if result and "id" in result:
        return {"status": "success", "message_id": result["id"]}
    
    error_msg = result.get("error", {}).get("message", "Unknown error") if result else "Failed to send DM"
    raise HTTPException(status_code=500, detail=error_msg)

import json

async def list_reels():
    token_data = load_token_data()
    if not token_data:
        return {"reels": []}
    
    reels = load_reels(token_data["ig_account_id"])
    return {
        "reels": [
            {
                "id": k, 
                "message": v["message"], 
                "keyword": v.get("keyword"),
                "buttons": v.get("buttons")
            }
            for k, v in reels.items()
        ]
    }

async def get_reel_by_id(reel_id: str):
    token_data = load_token_data()
    if not token_data:
        raise HTTPException(status_code=401, detail="Not connected")
    
    reels = load_reels(token_data["ig_account_id"])
    if reel_id not in reels:
        raise HTTPException(status_code=404, detail="Reel not found")
    reel = reels[reel_id]
    return {
        "id": reel_id,
        "message": reel.get("message"),
        "keyword": reel.get("keyword"),
        "buttons": reel.get("buttons")
    }

async def create_reel(reel: ReelData):
    token_data = load_token_data()
    if not token_data:
        raise HTTPException(status_code=401, detail="Not connected")
    
    ig_id = token_data["ig_account_id"]
    reels = load_reels(ig_id)
    if reel.reel_id in reels:
        raise HTTPException(status_code=400, detail="Reel already exists")
    
    buttons_json = None
    if reel.buttons:
        if isinstance(reel.buttons, list):
            buttons_json = json.dumps([b.dict() for b in reel.buttons])
        else:
            buttons_json = reel.buttons

    reels[reel.reel_id] = {
        "message": reel.message, 
        "keyword": reel.keyword,
        "buttons": buttons_json
    }
    save_reels(reels, ig_id)
    return {"id": reel.reel_id, "status": "created"}

async def update_reel(reel_id: str, reel: ReelUpdate):
    token_data = load_token_data()
    if not token_data:
        raise HTTPException(status_code=401, detail="Not connected")
    
    ig_id = token_data["ig_account_id"]
    reels = load_reels(ig_id)
    if reel_id not in reels:
        raise HTTPException(status_code=404, detail="Reel not found")
    
    buttons_json = None
    if reel.buttons:
        if isinstance(reel.buttons, list):
            buttons_json = json.dumps([b.dict() for b in reel.buttons])
        else:
            buttons_json = reel.buttons

    reels[reel_id] = {
        "message": reel.message, 
        "keyword": reel.keyword,
        "buttons": buttons_json
    }
    save_reels(reels, ig_id)
    return {"id": reel_id, "status": "updated"}

async def delete_reel(reel_id: str):
    token_data = load_token_data()
    if not token_data:
        raise HTTPException(status_code=401, detail="Not connected")
    
    ig_id = token_data["ig_account_id"]
    reels = load_reels(ig_id)
    if reel_id not in reels:
        raise HTTPException(status_code=404, detail="Reel not found")
    
    reels.pop(reel_id)
    save_reels(reels, ig_id)
    return {"id": reel_id, "status": "deleted"}
