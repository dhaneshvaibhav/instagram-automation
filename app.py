import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

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


@app.route('/webhook', methods=['GET'])
def webhook_get():
    """
    Webhook verification endpoint.
    Validates the webhook request from Meta.
    """
    hub_mode = request.args.get('hub.mode')
    hub_verify_token = request.args.get('hub.verify_token')
    hub_challenge = request.args.get('hub.challenge')
    
    if hub_mode == 'subscribe' and hub_verify_token == VERIFY_TOKEN:
        print(f"✓ Webhook verified successfully")
        return hub_challenge, 200
    else:
        print(f"✗ Webhook verification failed")
        return "Forbidden", 403


@app.route('/webhook', methods=['POST'])
def webhook_post():
    """
    Webhook POST endpoint.
    Receives comment notifications and sends DMs.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "ok"}), 200
    
    try:
        # Parse webhook payload
        entries = data.get('entry', [])
        
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
                        send_dm(commenter_id, media_id)
        
        return jsonify({"status": "ok"}), 200
    
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


def send_dm(user_id, media_id):
    """
    Send a DM to the user based on the Reel they commented on.
    
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
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"✓ DM sent to user {user_id}")
            return response.json()
        else:
            print(f"✗ Failed to send DM to user {user_id}: {response.text}")
            return None
    
    except Exception as e:
        print(f"Error sending DM: {str(e)}")
        return None


@app.route('/refresh-token', methods=['GET'])
def refresh_token():
    """
    Refresh the access token using the Graph API.
    """
    try:
        url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/me"
        params = {
            "fields": "id,name",
            "access_token": ACCESS_TOKEN
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            print("✓ Token validation successful")
            return jsonify({
                "status": "success",
                "data": response.json()
            }), 200
        else:
            print(f"✗ Token validation failed: {response.text}")
            return jsonify({
                "status": "error",
                "message": "Token refresh failed"
            }), response.status_code
    
    except Exception as e:
        print(f"Error refreshing token: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
