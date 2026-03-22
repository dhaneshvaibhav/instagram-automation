import json
import hmac
import hashlib
import asyncio
from fastapi import Request, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from app.core.config import VERIFY_TOKEN, APP_SECRET
from app.services.instagram_service import send_dm
from app.core.db_helpers import append_log, load_reels, load_token_data

def verify_signature(payload: bytes, signature: str):
    if not APP_SECRET:
        append_log("WARNING: No APP_SECRET found in .env. Skipping signature check.", "WARN")
        return True
    
    if not signature:
        append_log("No signature header found in request", "ERROR")
        return False
        
    expected_signature = hmac.new(
        APP_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    actual_signature = signature.replace('sha256=', '')
    is_valid = hmac.compare_digest(expected_signature, actual_signature)
    
    if not is_valid:
        append_log(f"SIGNATURE MISMATCH: Expected {expected_signature[:10]}... Received {actual_signature[:10]}...", "ERROR")
        return False 
        
    return True

async def verify_webhook(request: Request):
    append_log("WEBHOOK VERIFICATION ATTEMPT DETECTED!")
    mode = request.query_params.get('hub.mode')
    token = request.query_params.get('hub.verify_token')
    challenge = request.query_params.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        append_log("✓ Webhook verification SUCCESS")
        return PlainTextResponse(content=challenge)

    append_log("✗ Webhook verification FAILED (Token mismatch or wrong mode)", "ERROR")
    raise HTTPException(status_code=403, detail="Forbidden")

async def receive_webhook(request: Request):
    append_log("[RAW HIT] Webhook endpoint reached!")
    try:
        payload = await request.body()
        signature = request.headers.get('X-Hub-Signature-256')
        
        if not verify_signature(payload, signature):
            return JSONResponse(content={"status": "invalid signature"}, status_code=401)

        body = json.loads(payload)
        append_log("✅ Signature Verified. Processing event...")

        entries = body.get("entry", [])
        if not entries:
            append_log("ℹ Webhook received but no entries found")
            return JSONResponse(content={"status": "ok"})

        for entry in entries:
            # 1. Handle standard "changes" (like comments)
            changes = entry.get("changes", [])
            for change in changes:
                field = change.get("field")
                value = change.get("value", {})

                if field == "comments":
                    commenter_id = value.get("from", {}).get("id")
                    media_id = value.get("media", {}).get("id")
                    comment_id = value.get("id")
                    comment_text = value.get("text", "")
                    
                    append_log(f"💬 New Comment: From {commenter_id} on Reel {media_id}: '{comment_text}'")

                    if commenter_id and media_id:
                        # Find the account that owns this media (if possible) or just use the current token
                        token_data = load_token_data()
                        if not token_data:
                            append_log(f"⏭ Skipping: No Instagram account connected.")
                            continue
                        
                        ig_id = token_data["ig_account_id"]
                        reels = load_reels(ig_id)
                        reel_data = reels.get(media_id)

                        if not reel_data:
                            append_log(f"⏭ Skipping: Reel ID {media_id} is not tracked.")
                            continue

                        should_send = True
                        if reel_data.get("keyword"):
                            keyword = reel_data["keyword"].strip().lower()
                            if keyword not in comment_text.lower():
                                should_send = False
                                append_log(f"⏭ Skipping: Keyword '{keyword}' not found.")

                        if should_send:
                            append_log(f"🚀 Logic passed! Triggering DM to {commenter_id} via comment {comment_id}...")
                            asyncio.create_task(send_dm(commenter_id, media_id, comment_id=comment_id))
                else:
                    append_log(f"ℹ Webhook field '{field}' received (ignored)")

            # 2. Handle "messaging" (DMs, postbacks)
            messaging = entry.get("messaging", [])
            for message_event in messaging:
                sender_id = message_event.get("sender", {}).get("id")
                
                if "postback" in message_event:
                    postback = message_event["postback"]
                    payload = postback.get("payload")
                    title = postback.get("title")
                    append_log(f"🔘 Button Clicked: From {sender_id}, Payload: '{payload}', Title: '{title}'")
                    # Potential logic: send a reply based on the payload
                
                elif "message" in message_event:
                    msg = message_event["message"]
                    # Skip echoes (messages sent by the bot itself)
                    if msg.get("is_echo"):
                        continue
                        
                    text = msg.get("text")
                    append_log(f"📩 New DM: From {sender_id}: '{text}'")
                    
        return JSONResponse(content={"status": "ok"})

    except Exception as e:
        append_log(f"Webhook error: {e}", "ERROR")
        return JSONResponse(content={"status": "ok"})
