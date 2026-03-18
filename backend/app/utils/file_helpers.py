import os
from datetime import datetime, timedelta
from sqlmodel import Session, select
from app.core.db import engine, Token, Reel, Stats

LOG_FILE = "app.log"

def append_log(message: str, level: str = "INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {e}")
    print(log_entry.strip()) # Also print to terminal if it's visible

def get_logs(limit: int = 50):
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return lines[-limit:]
    except Exception as e:
        print(f"Error reading log file: {e}")
        return []

def clear_logs():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.truncate(0)
        except Exception as e:
            print(f"Error clearing log file: {e}")
    return True

def load_token_data():
    with Session(engine) as session:
        statement = select(Token)
        token = session.exec(statement).first()
        if token:
            return {
                "access_token": token.access_token,
                "ig_account_id": token.ig_account_id,
                "username": token.username,
                "name": token.name,
                "profile_picture_url": token.profile_picture_url,
                "followers_count": token.followers_count,
                "follows_count": token.follows_count,
                "media_count": token.media_count,
                "biography": token.biography,
                "expires_at": token.expires_at.isoformat() if token.expires_at else None
            }
        return None

def save_token(data: dict):
    # data can be a full profile or just basic info
    with Session(engine) as session:
        # Clear old tokens (assuming one account for now)
        from sqlalchemy import text
        session.execute(text("DELETE FROM token"))
        
        expires_at = data.get("expires_at")
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at)
        elif not expires_at:
            expires_at = datetime.now() + timedelta(days=60)

        token = Token(
            access_token=data.get("access_token"),
            ig_account_id=data.get("ig_account_id"),
            username=data.get("username", ""),
            name=data.get("name"),
            profile_picture_url=data.get("profile_picture_url"),
            followers_count=data.get("followers_count", 0),
            follows_count=data.get("follows_count", 0),
            media_count=data.get("media_count", 0),
            biography=data.get("biography", ""),
            expires_at=expires_at
        )
        session.add(token)
        session.commit()

def get_access_token():
    data = load_token_data()
    if not data:
        return None
    expires_at = data.get("expires_at")
    if expires_at:
        if datetime.fromisoformat(expires_at) < datetime.now():
            return None
    return data.get("access_token")

def load_reels(ig_account_id: str = None):
    if not ig_account_id:
        token = load_token_data()
        if not token: return {}
        ig_account_id = token["ig_account_id"]
        
    with Session(engine) as session:
        statement = select(Reel).where(Reel.ig_account_id == ig_account_id)
        reels = session.exec(statement).all()
        return {
            reel.reel_id: {
                "mode": reel.mode,
                "dm_message": reel.dm_message, 
                "public_reply": reel.public_reply,
                "keyword": reel.keyword,
                "ai_enabled": reel.ai_enabled,
                "ai_context": reel.ai_context,
                "ai_summary": reel.ai_summary
            } for reel in reels
        }

def save_reels(data: dict, ig_account_id: str = None):
    if not ig_account_id:
        token = load_token_data()
        if not token: return
        ig_account_id = token["ig_account_id"]

    with Session(engine) as session:
        # Clear reels for this user
        session.query(Reel).filter(Reel.ig_account_id == ig_account_id).delete()
        for reel_id, reel_data in data.items():
            reel = Reel(
                ig_account_id=ig_account_id,
                reel_id=reel_id,
                mode=reel_data.get("mode", "dm"),
                dm_message=reel_data.get("dm_message", ""),
                public_reply=reel_data.get("public_reply", ""),
                keyword=reel_data.get("keyword"),
                ai_enabled=reel_data.get("ai_enabled", False),
                ai_context=reel_data.get("ai_context"),
                ai_summary=reel_data.get("ai_summary")
            )
            session.add(reel)
        session.commit()

def load_stats(ig_account_id: str = None):
    if not ig_account_id:
        token = load_token_data()
        if not token: return {"total_dms": 0, "dms_today": 0, "last_reset": datetime.now().date().isoformat()}
        ig_account_id = token["ig_account_id"]

    with Session(engine) as session:
        statement = select(Stats).where(Stats.ig_account_id == ig_account_id)
        stats = session.exec(statement).first()
        if not stats:
            stats = Stats(ig_account_id=ig_account_id)
            session.add(stats)
            session.commit()
            session.refresh(stats)
        
        today = datetime.now().strftime("%Y-%m-%d")
        if stats.last_reset != today:
            stats.dms_today = 0
            stats.last_reset = today
            session.add(stats)
            session.commit()
            session.refresh(stats)
            
        return {
            "total_dms": stats.total_dms,
            "dms_today": stats.dms_today,
            "last_reset": stats.last_reset
        }

def save_stats(data: dict, ig_account_id: str = None):
    if not ig_account_id:
        token = load_token_data()
        if not token: return
        ig_account_id = token["ig_account_id"]

    with Session(engine) as session:
        stats = session.get(Stats, ig_account_id)
        if not stats:
            stats = Stats(ig_account_id=ig_account_id)
        
        stats.total_dms = data.get("total_dms", stats.total_dms)
        stats.dms_today = data.get("dms_today", stats.dms_today)
        stats.last_reset = data.get("last_reset", stats.last_reset)
        
        session.add(stats)
        session.commit()

def delete_token():
    with Session(engine) as session:
        session.query(Token).delete()
        session.commit()

def increment_dm_count(ig_account_id: str = None):
    if not ig_account_id:
        token = load_token_data()
        if not token: return
        ig_account_id = token["ig_account_id"]

    with Session(engine) as session:
        stats = session.get(Stats, ig_account_id)
        if not stats:
            stats = Stats(ig_account_id=ig_account_id)
            session.add(stats)
        
        today = datetime.now().strftime("%Y-%m-%d")
        if stats.last_reset != today:
            stats.dms_today = 0
            stats.last_reset = today
            
        stats.total_dms += 1
        stats.dms_today += 1
        
        session.add(stats)
        session.commit()
