import os
import json
from datetime import datetime, timedelta
from fastapi import HTTPException, Query
from fastapi.responses import RedirectResponse
from app.core.config import APP_ID, REDIRECT_URI, FRONTEND_URL
from app.services.token_service import (
    exchange_code_for_token, 
    fetch_ig_profile, 
    get_long_lived_token,
    refresh_long_lived_token
)
from app.utils.file_helpers import load_token_data, save_token, delete_token

async def login():
    if not APP_ID:
        raise HTTPException(status_code=500, detail="APP_ID not configured")

    from urllib.parse import urlencode
    params = {
        "client_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "instagram_business_basic instagram_business_manage_comments instagram_business_manage_messages",
        "response_type": "code"
    }
    auth_url = f"https://www.instagram.com/oauth/authorize?{urlencode(params)}"
    return RedirectResponse(url=auth_url)

async def callback(code: str = None, error: str = None, error_reason: str = None):
    if error:
        raise HTTPException(status_code=400, detail=f"Auth failed: {error_reason or error}")

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    try:
        token_data = await exchange_code_for_token(code)
        access_token = token_data.get("access_token")
        token_user_id = token_data.get("user_id")
        
        if not access_token:
            raise Exception("No access token in response")

        long_lived_data = await get_long_lived_token(access_token)
        if long_lived_data:
            access_token = long_lived_data.get("access_token")
            expires_in = long_lived_data.get("expires_in", 5184000)
            expires_at = (datetime.now() + timedelta(seconds=expires_in)).isoformat()
        else:
            expires_at = (datetime.now() + timedelta(hours=1)).isoformat()

        ig_account_id = str(token_user_id) if token_user_id else None
        username = "Instagram User"
        profile = {}
        
        try:
            profile = await fetch_ig_profile(access_token, ig_account_id)
            ig_account_id = profile.get("id") or ig_account_id
            username = profile.get("username") or username
        except Exception as e:
            if not ig_account_id:
                raise e

        data = {
            "access_token": access_token,
            "ig_account_id": ig_account_id,
            "username": username,
            "name": profile.get("name"),
            "account_type": profile.get("account_type"),
            "profile_picture_url": profile.get("profile_picture_url"),
            "followers_count": profile.get("followers_count", 0),
            "follows_count": profile.get("follows_count", 0),
            "media_count": profile.get("media_count", 0),
            "biography": profile.get("biography", ""),
            "expires_at": expires_at
        }
        
        save_token(data)
            
        return RedirectResponse(url=f"{FRONTEND_URL}/")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_status():
    token_data = load_token_data()
    if not token_data:
        return {"connected": False}

    expires_at = token_data.get("expires_at")
    if expires_at:
        expiry = datetime.fromisoformat(expires_at)
        if datetime.now() > expiry:
            return {"connected": False, "reason": "expired"}
        
        remaining = expiry - datetime.now()
        minutes_left = int(remaining.total_seconds() / 60)
        days_left = int(remaining.total_seconds() / (24 * 3600))
        
        return {
            "connected": True,
            "username": token_data.get("username"),
            "name": token_data.get("name"),
            "ig_account_id": token_data.get("ig_account_id"),
            "profile_picture_url": token_data.get("profile_picture_url"),
            "followers_count": token_data.get("followers_count"),
            "follows_count": token_data.get("follows_count"),
            "account_type": token_data.get("account_type"),
            "media_count": token_data.get("media_count"),
            "biography": token_data.get("biography"),
            "expires_at": expires_at,
            "minutes_left": minutes_left,
            "days_left": days_left
        }
    return {"connected": True}

async def refresh_token():
    token_data = load_token_data()
    if not token_data or not token_data.get("access_token"):
        raise HTTPException(status_code=401, detail="Not connected")
    
    refresh_data = await refresh_long_lived_token(token_data["access_token"])
    if not refresh_data:
        raise HTTPException(status_code=500, detail="Failed to refresh token")
    
    token_data["access_token"] = refresh_data.get("access_token")
    expires_in = refresh_data.get("expires_in", 5184000)
    token_data["expires_at"] = (datetime.now() + timedelta(seconds=expires_in)).isoformat()
    
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)
        
    return {"status": "success", "expires_at": token_data["expires_at"]}

async def logout():
    try:
        delete_token()
    except Exception:
        pass
    return {"status": "success", "message": "Logged out successfully"}
