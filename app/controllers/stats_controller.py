from app.utils.file_helpers import load_stats, load_reels, load_token_data, get_logs, clear_logs

async def get_logs_data():
    return {"logs": get_logs()}

async def clear_logs_data():
    clear_logs()
    return {"status": "success"}

async def get_dashboard_stats():
    stats = load_stats()
    reels = load_reels()
    return {
        "total_reels": len(reels),
        "dms_sent_today": stats.get("dms_today", 0),
        "total_dms": stats.get("total_dms", 0)
    }

async def health_check():
    token_data = load_token_data()
    return {
        "status": "healthy",
        "instagram_connected": token_data is not None,
        "total_reels": len(load_reels())
    }
