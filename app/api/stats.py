from fastapi import APIRouter
from app.utils.file_helpers import load_stats, load_reels, load_token_data, get_logs

router = APIRouter(tags=["stats"])

@router.get('/api/logs')
async def fetch_app_logs():
    return {"logs": get_logs()}

@router.get('/api/stats')
async def get_stats():
    stats = load_stats()
    reels = load_reels()
    return {
        "total_reels": len(reels),
        "dms_sent_today": stats.get("dms_today", 0),
        "total_dms": stats.get("total_dms", 0)
    }

@router.get('/health')
async def health_check():
    token_data = load_token_data()
    return {
        "status": "healthy",
        "instagram_connected": token_data is not None,
        "total_reels": len(load_reels())
    }
