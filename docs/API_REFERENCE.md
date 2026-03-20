# API Reference

Detailed information about the available endpoints in the Reelzy Backend.

## Authentication (`/auth`)

### `GET /auth/login`
Redirects the user to Instagram for OAuth authorization.

### `GET /auth/callback`
Handles the redirect back from Instagram. Exchanges the `code` for a long-lived access token.

### `GET /auth/status`
Checks if the account is currently connected. Returns profile stats and token expiry info.

### `GET /auth/refresh-token`
Manually triggers a refresh of the long-lived token.

---

## Messaging & Media (`/api/reels` & `/webhook`)

All core Instagram API logic is handled in `backend/app/services/instagram_service.py`.

### `send_dm(user_id, media_id, comment_id)`
Sends the automated message (text or buttons) to a user.

### `fetch_ig_media(access_token, user_id)`
Fetches the list of Reels for the dashboard dropdown.

### `fetch_ig_profile(access_token, user_id)`
Fetches the connected account's stats and biography.

---

## Webhook (`/webhook`)

### `GET /webhook`
Verification endpoint for Meta Webhook setup. Requires matching `VERIFY_TOKEN`.

### `POST /webhook`
Receives comment events from Instagram. Processes the logic to trigger DMs.

---

## Logs & Stats

### `GET /api/logs`
Returns the latest server activity logs.

### `DELETE /api/logs`
Clears the activity log file.
