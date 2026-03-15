import os
import json
import aiohttp
from datetime import datetime, timedelta
from urllib.parse import urlencode
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="Instagram Reel DM Bot", version="1.0.0")

# In-memory storage for reels (use database in production)
reels_db = {}

# Configuration from .env
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/auth/callback')
GRAPH_API_VERSION = 'v19.0'

# Reel ID to custom DM message mapping
REEL_MESSAGES = {
    "REEL_ID_1": "Hey! Thanks for commenting! Here's the link: [link]",
    "REEL_ID_2": "Hey! Here's the recipe I mentioned: [link]",
    "REEL_ID_3": "Here's your discount code: SAVE20"
}

DEFAULT_MESSAGE = "Thanks for commenting! Check back soon for more updates."


# Pydantic models for request validation
class WebhookPayload(BaseModel):
    object: str = None
    entry: list = None


class ReelData(BaseModel):
    reel_id: str
    message: str
    keyword: str = None


class ReelUpdate(BaseModel):
    message: str
    keyword: str = None


# Helper Functions
def get_access_token():
    """
    Retrieve access token from token.json file.
    Returns None if file doesn't exist or token is expired.
    """
    try:
        with open("token.json") as f:
            data = json.load(f)
            # Check if token is expired
            expires_at = data.get("expires_at")
            if expires_at:
                if datetime.fromisoformat(expires_at) < datetime.now():
                    return None
            return data.get("access_token")
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading token.json: {e}")
        return None


def save_token(access_token: str, ig_account_id: str):
    """
    Save access token and IG account ID to token.json with 60-day expiry.
    """
    expires_at = (datetime.now() + timedelta(days=60)).isoformat()
    token_data = {
        "access_token": access_token,
        "ig_account_id": ig_account_id,
        "expires_at": expires_at
    }
    with open("token.json", "w") as f:
        json.dump(token_data, f, indent=2)


def load_token_data():
    """
    Load token data from token.json.
    """
    try:
        with open("token.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading token.json: {e}")
        return None


async def exchange_code_for_token(code: str):
    """
    Exchange OAuth code for short-lived access token.
    """
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/oauth/access_token"
    params = {
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params) as response:
            if response.status != 200:
                raise Exception(f"Failed to exchange code: {await response.text()}")
            return await response.json()


async def exchange_short_token_for_long(short_token: str):
    """
    Exchange short-lived token for long-lived token (60 days).
    """
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": short_token
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise Exception(f"Failed to get long-lived token: {await response.text()}")
            return await response.json()


async def get_ig_account_id(access_token: str):
    """
    Get Instagram business account ID from the long-lived token.
    """
    # First get the page ID
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/me/accounts"
    params = {"access_token": access_token}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise Exception(f"Failed to get accounts: {await response.text()}")
            data = await response.json()
            
            if not data.get("data"):
                raise Exception("No pages found")
            
            page_id = data["data"][0]["id"]
            
            # Now get the Instagram business account from the page
            url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}"
            params = {
                "fields": "instagram_business_account",
                "access_token": access_token
            }
            
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Failed to get IG account: {await response.text()}")
                data = await response.json()
                
                ig_account = data.get("instagram_business_account", {})
                return ig_account.get("id")


# OAuth Routes
@app.get('/auth/login')
async def auth_login():
    """
    Redirect user to Instagram OAuth login page.
    """
    oauth_url = "https://www.facebook.com/v19.0/dialog/oauth"
    params = {
        "client_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "instagram_business_basic,instagram_business_manage_messages,instagram_business_manage_comments,pages_read_engagement,pages_manage_metadata,pages_read_user_content",
        "response_type": "code"
    }
    
    auth_url = f"{oauth_url}?{urlencode(params)}"
    return RedirectResponse(url=auth_url)


@app.get('/auth/callback')
async def auth_callback(code: str = Query(None), error: str = Query(None)):
    """
    Callback endpoint after user logs in to Instagram.
    Exchanges code for access token and saves it.
    """
    if error:
        raise HTTPException(status_code=400, detail=f"Auth failed: {error}")
    
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    
    try:
        # Exchange code for short-lived token
        short_token_response = await exchange_code_for_token(code)
        short_token = short_token_response.get("access_token")
        
        # Exchange short token for long-lived token
        long_token_response = await exchange_short_token_for_long(short_token)
        long_token = long_token_response.get("access_token")
        
        # Get IG Account ID
        ig_account_id = await get_ig_account_id(long_token)
        
        if not ig_account_id:
            raise Exception("Could not retrieve Instagram account ID")
        
        # Save token and account ID
        save_token(long_token, ig_account_id)
        
        print(f"✓ Instagram account connected: {ig_account_id}")
        return RedirectResponse(url="/")
    
    except Exception as e:
        print(f"✗ OAuth callback error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")


@app.get('/auth/status')
async def auth_status():
    """
    Check if Instagram account is connected and token status.
    """
    token_data = load_token_data()
    
    if not token_data:
        return {"connected": False}
    
    expires_at = token_data.get("expires_at")
    
    # Check if token is expired
    if expires_at:
        if datetime.fromisoformat(expires_at) < datetime.now():
            return {"connected": False}
    
    return {
        "connected": True,
        "expires_at": expires_at,
        "ig_account_id": token_data.get("ig_account_id")
    }


@app.get('/auth/logout')
async def auth_logout():
    """
    Logout and delete saved token.
    """
    try:
        if os.path.exists("token.json"):
            os.remove("token.json")
            print("✓ User logged out, token deleted")
    except Exception as e:
        print(f"Error during logout: {e}")
    
    return RedirectResponse(url="/")


# Webhook Routes
@app.get('/webhook')
async def webhook_get(request):
    """
    Webhook verification endpoint.
    Validates the webhook request from Meta.
    """
    # Extract query parameters
    hub_mode = request.query_params.get('hub.mode')
    hub_verify_token = request.query_params.get('hub.verify_token')
    hub_challenge = request.query_params.get('hub.challenge')
    
    if hub_mode == 'subscribe' and hub_verify_token == VERIFY_TOKEN:
        print(f"✓ Webhook verified successfully")
        return hub_challenge
    else:
        print(f"✗ Webhook verification failed - mode: {hub_mode}, token: {hub_verify_token}")
        raise HTTPException(status_code=403, detail="Forbidden")


@app.post('/webhook')
async def webhook_post(payload: WebhookPayload):
    """
    Webhook POST endpoint.
    Receives comment notifications and sends DMs.
    """
    if not payload or not payload.entry:
        return {"status": "ok"}
    
    try:
        # Parse webhook payload
        entries = payload.entry or []
        
        for entry in entries:
            changes = entry.get('changes', [])
            
            for change in changes:
                field = change.get('field')
                
                # Only process comments
                if field == 'comments':
                    value = change.get('value', {})
                    
                    # Extract comment details
                    commenter_id = value.get('from', {}).get('id')
                    media_id = value.get('media', {}).get('id')
                    comment_text = value.get('text')
                    
                    if commenter_id and media_id:
                        print(f"📝 New comment on media {media_id} from user {commenter_id}: {comment_text}")
                        # Send DM asynchronously without waiting
                        # In production, consider using background tasks or a task queue
                        import asyncio
                        asyncio.create_task(send_dm(commenter_id, media_id))
        
        return {"status": "ok"}
    
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def send_dm(user_id: str, media_id: str):
    """
    Send a DM to the user based on the Reel they commented on (async).
    
    Args:
        user_id: Instagram user ID of the commenter
        media_id: Instagram media (Reel) ID
    """
    try:
        # Get access token
        access_token = get_access_token()
        if not access_token:
            print(f"✗ No access token available")
            return None
        
        # Get the custom message for this reel, or use default
        message = REEL_MESSAGES.get(media_id, DEFAULT_MESSAGE)
        
        # Meta Graph API endpoint for sending messages
        url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/me/messages"
        
        payload = {
            "recipient": {
                "id": user_id
            },
            "message": {
                "text": message
            },
            "access_token": access_token
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    print(f"✓ DM sent to user {user_id}")
                    return await response.json()
                else:
                    text = await response.text()
                    print(f"✗ Failed to send DM to user {user_id}: {text}")
                    return None
    
    except Exception as e:
        print(f"Error sending DM: {str(e)}")
        return None


@app.get('/refresh-token')
async def refresh_token():
    """
    Refresh the access token using the Graph API (async).
    """
    try:
        token_data = load_token_data()
        if not token_data:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        current_token = token_data.get("access_token")
        url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/oauth/access_token"
        params = {
            "grant_type": "ig_refresh_token",
            "access_token": current_token
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    new_token = data.get("access_token")
                    
                    # Save the new token
                    save_token(new_token, token_data.get("ig_account_id"))
                    
                    expires_at = (datetime.now() + timedelta(days=60)).isoformat()
                    print("✓ Token refreshed successfully")
                    return {
                        "status": "refreshed",
                        "expires_at": expires_at
                    }
                else:
                    text = await response.text()
                    print(f"✗ Token refresh failed: {text}")
                    raise HTTPException(
                        status_code=response.status,
                        detail="Token refresh failed"
                    )
    
    except Exception as e:
        print(f"Error refreshing token: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/health')
async def health_check():
    """
    Health check endpoint (async).
    """
    return {"status": "healthy"}


# Dashboard Routes
@app.get('/')
async def serve_dashboard():
    """
    Serve the dashboard HTML file.
    """
    template_path = Path(__file__).parent / "templates" / "index.html"
    if not template_path.exists():
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return FileResponse(template_path, media_type="text/html")


# API Routes for Dashboard
@app.get('/api/stats')
async def get_stats():
    """
    Get dashboard statistics.
    """
    return {
        "total_reels": len(reels_db),
        "dms_sent_today": 0,  # Would be fetched from database in production
        "total_dms_sent": 0   # Would be fetched from database in production
    }


@app.get('/api/reels')
async def get_reels():
    """
    Get all reels with their messages.
    """
    reels_list = [
        {
            "id": reel_id,
            "message": data["message"],
            "keyword": data.get("keyword")
        }
        for reel_id, data in reels_db.items()
    ]
    return {"reels": reels_list}


@app.get('/api/reels/{reel_id}')
async def get_reel(reel_id: str):
    """
    Get a specific reel by ID.
    """
    if reel_id not in reels_db:
        raise HTTPException(status_code=404, detail="Reel not found")
    
    return {
        "id": reel_id,
        "message": reels_db[reel_id]["message"],
        "keyword": reels_db[reel_id].get("keyword")
    }


@app.post('/api/reels')
async def create_reel(reel: ReelData):
    """
    Create a new reel with custom message and optional keyword.
    """
    if reel.reel_id in reels_db:
        raise HTTPException(status_code=400, detail="Reel already exists")
    
    reels_db[reel.reel_id] = {
        "message": reel.message,
        "keyword": reel.keyword
    }
    
    return {
        "id": reel.reel_id,
        "message": reel.message,
        "keyword": reel.keyword,
        "status": "created"
    }


@app.put('/api/reels/{reel_id}')
async def update_reel(reel_id: str, reel: ReelUpdate):
    """
    Update an existing reel's message and keyword.
    """
    if reel_id not in reels_db:
        raise HTTPException(status_code=404, detail="Reel not found")
    
    reels_db[reel_id]["message"] = reel.message
    reels_db[reel_id]["keyword"] = reel.keyword
    
    return {
        "id": reel_id,
        "message": reel.message,
        "keyword": reel.keyword,
        "status": "updated"
    }


@app.delete('/api/reels/{reel_id}')
async def delete_reel(reel_id: str):
    """
    Delete a reel.
    """
    if reel_id not in reels_db:
        raise HTTPException(status_code=404, detail="Reel not found")
    
    deleted = reels_db.pop(reel_id)
    
    return {
        "id": reel_id,
        "status": "deleted"
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
