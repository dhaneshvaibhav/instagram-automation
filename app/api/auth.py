import os
import aiohttp
from datetime import datetime
from urllib.parse import urlencode
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import RedirectResponse
from app.core.config import APP_ID, REDIRECT_URI, TOKEN_FILE
from app.services.token_service import exchange_code_for_token, exchange_short_for_long_token, fetch_ig_profile
from app.utils.file_helpers import load_token_data, save_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get('/login')
async def auth_login():
    if not APP_ID:
        raise HTTPException(status_code=500, detail="APP_ID not configured")

    params = {
        "client_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "instagram_basic,instagram_manage_comments,instagram_manage_messages,pages_show_list,pages_read_engagement",
        "response_type": "code",
    }
    # Using Facebook Login for Business flow
    auth_url = f"https://www.facebook.com/v21.0/dialog/oauth?{urlencode(params)}"
    return RedirectResponse(url=auth_url)

@router.get('/callback')
async def auth_callback(
    code: str = Query(None),
    error: str = Query(None),
    error_reason: str = Query(None)
):
    if error:
        print(f"Auth error: {error} - {error_reason}")
        raise HTTPException(status_code=400, detail=f"Auth failed: {error_reason or error}")

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    try:
        # Step 1: Short-lived token
        short_data = await exchange_code_for_token(code)
        short_token = short_data.get("access_token")

        if not short_token:
            raise Exception("No access token in response")

        # Step 2: Long-lived token
        long_data = await exchange_short_for_long_token(short_token)
        long_token = long_data.get("access_token")

        if not long_token:
            raise Exception("No long-lived token in response")

        # Step 3: Get profile
        profile = await fetch_ig_profile(long_token)
        ig_account_id = profile.get("id")
        username = profile.get("username", "")

        if not ig_account_id:
            raise Exception("Could not get Instagram account ID")

        # Step 4: Save token
        save_token(long_token, ig_account_id, username)
        print(f"✓ Connected: @{username} (ID: {ig_account_id})")

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
        days_left = (expiry - datetime.now()).days
        return {
            "connected": True,
            "username": token_data.get("username"),
            "ig_account_id": token_data.get("ig_account_id"),
            "expires_at": expires_at,
            "days_left": days_left
        }

    return {"connected": True}

@router.get('/logout')
async def auth_logout():
    try:
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
            print("✓ Logged out")
    except Exception as e:
        print(f"Logout error: {e}")
    return RedirectResponse(url="/")
