# Features & Core Logic

This document covers the internal logic of the bot's functions and utility scripts.

## Core Logic: Comment-to-DM

The primary logic resides in `backend/app/controllers/webhook_controller.py`. 

1. **Verification**: The backend verifies the `X-Hub-Signature-256` header using the `APP_SECRET` to ensure the request is actually from Meta.
2. **Filtering**: 
   - Checks if the `media_id` (Reel ID) exists in the `reel` table.
   - If a `keyword` is set for that Reel, it performs a case-insensitive search in the comment text.
3. **Execution**: Calls `send_dm` in `instagram_service.py`.

## Messaging & Media Logic

All core Instagram interactions are consolidated in `backend/app/services/instagram_service.py`.

### 1. Sending DMs (`send_dm`)
- **Capability**: Sends a text message or a button template to a user.
- **Logic**: Automatically detects if a Reel has configured buttons and builds the appropriate payload.

### 2. Fetching Media (`fetch_ig_media`)
- **Capability**: Retrieves all Reels and posts from the connected Instagram account.
- **Used for**: Populating the "Select Reel" dropdown in the dashboard.

### 3. Profile Management (`fetch_ig_profile`)
- **Capability**: Fetches user stats (Followers, Media Count, Bio) for the dashboard display.

## Future Feature Utilities

Additional pre-written functions are available in `backend/app/utils/future_features.py` for future implementation:

### 1. Follower Check (`is_following`)
- **Capability**: Checks if a user follows your business account.
- **API**: `GET /{user-id}/friendships/{target-user-id}`.

### 2. Public Replies (`public_comment_reply`)
- **Capability**: Allows the bot to reply publicly to a comment.
- **API**: `POST /{comment-id}/replies`.

### 3. Comment Moderation (`moderate_comment`)
- **Capability**: Programmatically Hides or Deletes comments.
- **API**: `POST /{comment-id}` (hide) or `DELETE /{comment-id}`.

### 4. Media Insights (`get_media_insights`)
- **Capability**: Fetches reach, impressions, and engagement metrics for a Reel.
- **API**: `GET /{media-id}/insights`.

## Testing the Logic
You can test the future feature logic independently by running:
```bash
python backend/app/utils/future_features.py
```
*(Note: Requires valid `INSTAGRAM_ACCESS_TOKEN` in `.env`)*
