import os
from datetime import datetime, timedelta
from urllib.parse import urlencode
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import RedirectResponse
from app.core.config import APP_ID, REDIRECT_URI, TOKEN_FILE
from app.services.token_service import (
    exchange_code_for_token, 
    fetch_ig_profile, 
    get_long_lived_token,
    refresh_long_lived_token
)
from app.utils.file_helpers import load_token_data, save_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get('/login')
async def auth_login():
    if not APP_ID:
        raise HTTPException(status_code=500, detail="APP_ID not configured")

    params = {
        "client_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "instagram_business_basic,instagram_business_manage_comments,instagram_business_manage_messages",
        "response_type": "code"
    }
    # Standard Instagram OAuth
    auth_url = f"https://www.instagram.com/oauth/authorize?{urlencode(params)}"
    return RedirectResponse(url=auth_url)

@router.get('/callback')
async def auth_callback(
    code: str = Query(None),
    error: str = Query(None),
    error_reason: str = Query(None)
):
    if error:
        raise HTTPException(status_code=400, detail=f"Auth failed: {error_reason or error}")

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    try:
        # Step 1: Exchange code for short-lived access token
        print("Starting token exchange...")
        token_data = await exchange_code_for_token(code)
        access_token = token_data.get("access_token")
        token_user_id = token_data.get("user_id")
        
        if not access_token:
            print("✗ Failed: No access token in response")
            raise Exception("No access token in response")

        print(f"✓ Token exchange successful for User ID: {token_user_id}")

        # Step 1.5: Exchange short-lived for long-lived (60 days)
        print("Exchanging for long-lived token...")
        long_lived_data = await get_long_lived_token(access_token)
        if long_lived_data:
            access_token = long_lived_data.get("access_token")
            # expires_in is in seconds
            expires_in = long_lived_data.get("expires_in", 5184000) # Default 60 days
            expires_at = (datetime.now() + timedelta(seconds=expires_in)).isoformat()
            print(f"✓ Long-lived token secured. Expiry: {expires_at}")
        else:
            print("⚠ Long-lived exchange failed, falling back to short-lived (1hr)")
            expires_at = (datetime.now() + timedelta(hours=1)).isoformat()

        # Step 2: Fetch profile (to get details)
        ig_account_id = str(token_user_id) if token_user_id else None
        username = "Instagram User"
        profile = {}
        
        try:
            # Passing token_user_id directly to avoid /me errors
            profile = await fetch_ig_profile(access_token, ig_account_id)
            ig_account_id = profile.get("id") or ig_account_id
            username = profile.get("username") or username
        except Exception as e:
            print(f"⚠ Could not fetch profile details: {e}")
            if not ig_account_id:
                raise e # If we don't even have the user_id, it's a hard fail

        # Step 3: Save the token
        from app.utils.file_helpers import save_token
        import json
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
        with open(TOKEN_FILE, "w") as f:
            json.dump(data, f, indent=2)
            
        print(f"✓ Connected: @{username}")
        return RedirectResponse(url="/")

    except Exception as e:
        print(f"✗ Callback error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/status')
async def auth_status():
    token_data = load_token_data()
    if not token_data:
        return {"connected": False}

    expires_at = token_data.get("expires_at")
    if expires_at:
        expiry = datetime.fromisoformat(expires_at)
        if datetime.now() > expiry:
            return {"connected": False, "reason": "expired"}
        
        # Calculate time remaining
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

@router.get('/refresh-token')
async def refresh_token_route():
    token_data = load_token_data()
    if not token_data or not token_data.get("access_token"):
        raise HTTPException(status_code=401, detail="Not connected")
    
    # documentation: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/business-login#refresh-a-long-lived-access-token
    print("Refreshing long-lived token...")
    refresh_data = await refresh_long_lived_token(token_data["access_token"])
    
    if not refresh_data:
        raise HTTPException(status_code=500, detail="Failed to refresh token")
    
    # Update token data
    token_data["access_token"] = refresh_data.get("access_token")
    expires_in = refresh_data.get("expires_in", 5184000)
    token_data["expires_at"] = (datetime.now() + timedelta(seconds=expires_in)).isoformat()
    
    # Save updated data
    with open(TOKEN_FILE, "w") as f:
        import json
        json.dump(token_data, f, indent=2)
        
    print(f"✓ Token refreshed. New expiry: {token_data['expires_at']}")
    return {"status": "success", "expires_at": token_data["expires_at"]}

@router.get('/logout')
async def auth_logout():
    try:
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
            print("✓ Logged out")
    except Exception as e:
        print(f"Logout error: {e}")
    return RedirectResponse(url="/")
