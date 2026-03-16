from fastapi import APIRouter, HTTPException
from app.models.reel import ReelData, ReelUpdate
from app.utils.file_helpers import load_reels, save_reels, load_token_data
from app.services.token_service import fetch_ig_media
from app.services.instagram_service import send_dm

router = APIRouter(prefix="/api/reels", tags=["reels"])

@router.get('/instagram')
async def get_instagram_reels():
    token_data = load_token_data()
    if not token_data or not token_data.get("access_token"):
        raise HTTPException(status_code=401, detail="Not connected")
    
    reels = await fetch_ig_media(
        token_data["access_token"], 
        token_data["ig_account_id"]
    )
    return {"reels": reels}

@router.post('/test-dm')
async def test_dm_route(data: dict):
    user_id = data.get("user_id")
    media_id = data.get("media_id")
    
    token_data = load_token_data()
    if not token_data:
        raise HTTPException(status_code=401, detail="Not connected")

    # Support 'me' as a shortcut to send to yourself
    if not user_id or user_id.lower() == 'me':
        user_id = token_data.get("ig_account_id")
    
    if not user_id or not media_id:
        raise HTTPException(status_code=400, detail="Missing user_id or media_id")
        
    result = await send_dm(user_id, media_id)
    if result and "id" in result:
        return {"status": "success", "message_id": result["id"]}
    
    error_msg = result.get("error", {}).get("message", "Unknown error") if result else "Failed to send DM"
    raise HTTPException(status_code=500, detail=error_msg)

@router.get('')
async def get_reels():
    reels = load_reels()
    return {
        "reels": [
            {"id": k, "message": v["message"], "keyword": v.get("keyword")}
            for k, v in reels.items()
        ]
    }

@router.post('')
async def create_reel(reel: ReelData):
    reels = load_reels()
    if reel.reel_id in reels:
        raise HTTPException(status_code=400, detail="Reel already exists")
    reels[reel.reel_id] = {"message": reel.message, "keyword": reel.keyword}
    save_reels(reels)
    return {"id": reel.reel_id, "status": "created"}

@router.put('/{reel_id}')
async def update_reel(reel_id: str, reel: ReelUpdate):
    reels = load_reels()
    if reel_id not in reels:
        raise HTTPException(status_code=404, detail="Reel not found")
    reels[reel_id] = {"message": reel.message, "keyword": reel.keyword}
    save_reels(reels)
    return {"id": reel_id, "status": "updated"}

@router.delete('/{reel_id}')
async def delete_reel(reel_id: str):
    reels = load_reels()
    if reel_id not in reels:
        raise HTTPException(status_code=404, detail="Reel not found")
    reels.pop(reel_id)
    save_reels(reels)
    return {"id": reel_id, "status": "deleted"}
