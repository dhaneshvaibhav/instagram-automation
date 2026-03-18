from fastapi import HTTPException
from app.models.reel import ReelData, ReelUpdate
from app.utils.file_helpers import load_reels, save_reels, load_token_data
from app.services.token_service import fetch_ig_media, fetch_single_media
from app.services.instagram_service import send_dm
from app.services.ai_service import generate_reel_summary

async def get_instagram_reels():
    token_data = load_token_data()
    if not token_data or not token_data.get("access_token"):
        raise HTTPException(status_code=401, detail="Not connected")
    
    reels = await fetch_ig_media(
        token_data["access_token"], 
        token_data["ig_account_id"]
    )
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

async def list_reels():
    token_data = load_token_data()
    if not token_data:
        return {"reels": []}
    
    reels = load_reels(token_data["ig_account_id"])
    return {
        "reels": [
            {
                "id": k, 
                "mode": v.get("mode", "dm"),
                "dm_message": v.get("dm_message"), 
                "public_reply": v.get("public_reply"),
                "keyword": v.get("keyword"),
                "ai_enabled": v.get("ai_enabled"),
                "ai_context": v.get("ai_context"),
                "ai_summary": v.get("ai_summary")
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
        "mode": reel.get("mode", "dm"),
        "dm_message": reel.get("dm_message"),
        "public_reply": reel.get("public_reply"),
        "keyword": reel.get("keyword"),
        "ai_enabled": reel.get("ai_enabled"),
        "ai_context": reel.get("ai_context"),
        "ai_summary": reel.get("ai_summary")
    }

async def create_reel(reel: ReelData):
    token_data = load_token_data()
    if not token_data:
        raise HTTPException(status_code=401, detail="Not connected")
    
    ig_id = token_data["ig_account_id"]
    reels = load_reels(ig_id)
    if reel.reel_id in reels:
        raise HTTPException(status_code=400, detail="Reel already exists")
    
    # Try to fetch reel data for AI summary
    ai_summary = None
    if reel.ai_enabled:
        try:
            media_info = await fetch_single_media(token_data["access_token"], reel.reel_id)
            if media_info and media_info.get("caption"):
                ai_summary = await generate_reel_summary(
                    media_info["caption"], 
                    media_info.get("media_type", "VIDEO")
                )
        except Exception as e:
            print(f"Failed to generate AI summary: {e}")

    reels[reel.reel_id] = {
        "mode": reel.mode,
        "dm_message": reel.dm_message, 
        "public_reply": reel.public_reply,
        "keyword": reel.keyword,
        "ai_enabled": reel.ai_enabled,
        "ai_context": reel.ai_context,
        "ai_summary": ai_summary
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
    
    # Try to fetch reel data for AI summary if it's missing or if ai_enabled is toggled
    existing_reel = reels.get(reel_id, {})
    ai_summary = existing_reel.get("ai_summary")
    
    if reel.ai_enabled and not ai_summary:
        try:
            media_info = await fetch_single_media(token_data["access_token"], reel_id)
            if media_info and media_info.get("caption"):
                ai_summary = await generate_reel_summary(
                    media_info["caption"], 
                    media_info.get("media_type", "VIDEO")
                )
        except Exception as e:
            print(f"Failed to generate AI summary: {e}")

    reels[reel_id] = {
        "mode": reel.mode,
        "dm_message": reel.dm_message, 
        "public_reply": reel.public_reply,
        "keyword": reel.keyword,
        "ai_enabled": reel.ai_enabled,
        "ai_context": reel.ai_context,
        "ai_summary": ai_summary
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
