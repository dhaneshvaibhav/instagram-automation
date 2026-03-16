from fastapi import APIRouter, HTTPException
from app.models.reel import ReelData, ReelUpdate
from app.utils.file_helpers import load_reels, save_reels

router = APIRouter(prefix="/api/reels", tags=["reels"])

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
