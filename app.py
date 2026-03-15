import os
import aiohttp
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="Instagram Reel DM Bot", version="1.0.0")

# Configuration
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
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


@app.get('/webhook')
async def webhook_get(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    """
    Webhook verification endpoint.
    Validates the webhook request from Meta.
    """
    if hub_mode == 'subscribe' and hub_verify_token == VERIFY_TOKEN:
        print(f"✓ Webhook verified successfully")
        return hub_challenge
    else:
        print(f"✗ Webhook verification failed")
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
            "access_token": ACCESS_TOKEN
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
        url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/me"
        params = {
            "fields": "id,name",
            "access_token": ACCESS_TOKEN
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    print("✓ Token validation successful")
                    return {
                        "status": "success",
                        "data": data
                    }
                else:
                    text = await response.text()
                    print(f"✗ Token validation failed: {text}")
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


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
