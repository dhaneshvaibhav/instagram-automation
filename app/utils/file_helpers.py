import json
import os
from datetime import datetime, timedelta
from app.core.config import TOKEN_FILE, REELS_FILE, STATS_FILE

LOG_FILE = "app.log"

def append_log(message: str, level: str = "INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(log_entry.strip()) # Also print to terminal if it's visible

def get_logs(limit: int = 50):
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        return lines[-limit:]

def load_token_data():
    try:
        with open(TOKEN_FILE) as f:
            return json.load(f)
    except:
        return None

def save_token(access_token: str, ig_account_id: str, username: str = ""):
    expires_at = (datetime.now() + timedelta(days=60)).isoformat()
    data = {
        "access_token": access_token,
        "ig_account_id": ig_account_id,
        "username": username,
        "expires_at": expires_at
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_access_token():
    data = load_token_data()
    if not data:
        return None
    expires_at = data.get("expires_at")
    if expires_at:
        if datetime.fromisoformat(expires_at) < datetime.now():
            return None
    return data.get("access_token")

def load_reels():
    try:
        with open(REELS_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_reels(data: dict):
    with open(REELS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_stats():
    try:
        with open(STATS_FILE) as f:
            return json.load(f)
    except:
        return {"total_dms": 0, "dms_today": 0, "last_reset": datetime.now().date().isoformat()}

def save_stats(data: dict):
    with open(STATS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def increment_dm_count():
    stats = load_stats()
    today = datetime.now().date().isoformat()
    # Reset today's count if it's a new day
    if stats.get("last_reset") != today:
        stats["dms_today"] = 0
        stats["last_reset"] = today
    stats["total_dms"] = stats.get("total_dms", 0) + 1
    stats["dms_today"] = stats.get("dms_today", 0) + 1
    save_stats(stats)
