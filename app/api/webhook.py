import json
import hmac
import hashlib
import asyncio
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from app.core.config import VERIFY_TOKEN, APP_SECRET
from app.services.instagram_service import send_dm
from app.utils.file_helpers import load_reels

router = APIRouter(prefix="/webhook", tags=["webhook"])

def verify_signature(payload: bytes, signature: str):
    if not APP_SECRET:
        return True  # Skip if secret not set, though it should be in live mode
    
    if not signature:
        return False
        
    expected_signature = hmac.new(
        APP_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # signature usually comes as 'sha256=...'
    actual_signature = signature.replace('sha256=', '')
    return hmac.compare_digest(expected_signature, actual_signature)

@router.get('')
async def webhook_verify(request: Request):
    mode = request.query_params.get('hub.mode')
    token = request.query_params.get('hub.verify_token')
    challenge = request.query_params.get('hub.challenge')

    print(f"Webhook verify → mode: {mode}, token: {token}, challenge: {challenge}")

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("✓ Webhook verified")
        return PlainTextResponse(content=challenge)

    print("✗ Webhook verification failed")
    raise HTTPException(status_code=403, detail="Forbidden")

@router.post('')
async def webhook_receive(request: Request):
    try:
        # Get raw body for signature verification
        payload = await request.body()
        signature = request.headers.get('X-Hub-Signature-256')

        if not verify_signature(payload, signature):
            print("✗ Webhook signature verification failed")
            return JSONResponse(content={"status": "invalid signature"}, status_code=401)

        body = json.loads(payload)
        print("Webhook received:", json.dumps(body, indent=2))

        entries = body.get("entry", [])

        for entry in entries:
            changes = entry.get("changes", [])

            for change in changes:
                field = change.get("field")
                value = change.get("value", {})

                if field == "comments":
                    commenter_id = value.get("from", {}).get("id")
                    media_id = value.get("media", {}).get("id")
                    comment_text = value.get("text", "")

                    print(f"💬 Comment on reel {media_id} from {commenter_id}: {comment_text}")

                    if commenter_id and media_id:
                        # Check keyword if set
                        reels = load_reels()
                        reel_data = reels.get(media_id)

                        should_send = True

                        if reel_data and reel_data.get("keyword"):
                            keyword = reel_data["keyword"].lower()
                            if keyword not in comment_text.lower():
                                should_send = False
                                print(f"⏭ Keyword '{keyword}' not found in comment, skipping")

                        if should_send:
                            asyncio.create_task(send_dm(commenter_id, media_id))

        return JSONResponse(content={"status": "ok"})

    except Exception as e:
        print(f"Webhook error: {e}")
        return JSONResponse(content={"status": "ok"})
