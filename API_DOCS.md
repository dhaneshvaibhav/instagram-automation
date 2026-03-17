# Instagram Reel DM Bot API Documentation

This document outlines the API structure, endpoints, and data formats for the Instagram Reel DM Bot.

## **Architecture Overview**

The project follows a modular structure:
- **Routes (`app/api/`)**: Defines the API endpoints and maps them to controllers.
- **Controllers (`app/controllers/`)**: Contains the business logic for each route.
- **Services (`app/services/`)**: Handles external API integrations (Instagram/Facebook Graph API).
- **Utils (`app/utils/`)**: Provides helper functions for file I/O, logging, and data persistence.
- **Models (`app/models/`)**: Defines data structures and validation using Pydantic.

---

## **1. Authentication (`/auth`)**

Handles Instagram OAuth login, token management, and status.

### **GET `/auth/login`**
- **Description**: Redirects the user to the Instagram OAuth authorization page.
- **Takes**: None
- **Returns**: 302 Redirect to Instagram.

### **GET `/auth/callback`**
- **Description**: Handles the OAuth redirect from Instagram. Exchanges code for access tokens.
- **Takes**:
  - `code` (query, string): The authorization code.
  - `error` (query, string, optional): Error message if auth failed.
- **Returns**: 302 Redirect to dashboard (`/`).

### **GET `/auth/status`**
- **Description**: Checks if an Instagram account is currently connected and valid.
- **Takes**: None
- **Returns**: JSON
  - `connected` (bool): Whether the account is connected.
  - `username` (string): Instagram username.
  - `expires_at` (string): Token expiration timestamp.

### **GET `/auth/refresh-token`**
- **Description**: Refreshes the long-lived access token.
- **Takes**: None
- **Returns**: JSON with new `expires_at`.

### **GET `/auth/logout`**
- **Description**: Disconnects the Instagram account and deletes the token file.
- **Takes**: None
- **Returns**: 302 Redirect to dashboard.

---

## **2. Reels Management (`/api/reels`)**

Manages the list of Reels to track and their automated responses.

### **GET `/api/reels`**
- **Description**: Retrieves all tracked Reels from `reels.json`.
- **Takes**: None
- **Returns**: JSON list of reels with `id`, `message`, and `keyword`.

### **POST `/api/reels`**
- **Description**: Adds a new Reel to track.
- **Takes**: JSON
  - `reel_id` (string, required): The Instagram Reel ID.
  - `message` (string, required): The DM text to send.
  - `keyword` (string, optional): Only send DM if comment contains this.
- **Returns**: JSON status.

### **PUT `/api/reels/{reel_id}`**
- **Description**: Updates an existing Reel configuration.
- **Takes**: JSON (same as POST).
- **Returns**: JSON status.

### **DELETE `/api/reels/{reel_id}`**
- **Description**: Stops tracking a Reel.
- **Takes**: Path parameter `reel_id`.
- **Returns**: JSON status.

### **GET `/api/reels/instagram`**
- **Description**: Fetches recent media directly from the connected Instagram account.
- **Takes**: None
- **Returns**: JSON list of media objects from Instagram API.

### **POST `/api/reels/test-dm`**
- **Description**: Sends a manual test DM to a specific user.
- **Takes**: JSON
  - `user_id` (string): Instagram User ID or 'me'.
  - `media_id` (string): Reel ID to use for the message.
- **Returns**: JSON status and `message_id`.

---

## **3. Webhook (`/webhook`)**

Endpoint for Instagram Real-time Updates.

### **GET `/webhook`**
- **Description**: Used by Facebook to verify the webhook endpoint.
- **Takes**: `hub.challenge`, `hub.verify_token`, `hub.mode`.
- **Returns**: Plain text challenge.

### **POST `/webhook`**
- **Description**: Receives real-time comment events from Instagram.
- **Takes**: JSON payload from Facebook Graph API.
- **Returns**: JSON `{"status": "ok"}`.

---

## **4. Stats & Logs (`/api/stats`, `/api/logs`)**

### **GET `/api/stats`**
- **Description**: Gets usage statistics for the dashboard.
- **Returns**: `total_reels`, `dms_sent_today`, `total_dms`.

### **GET `/api/logs`**
- **Description**: Fetches the latest activity logs.
- **Returns**: JSON list of log strings.

### **DELETE `/api/logs`**
- **Description**: Clears all server-side logs.
- **Returns**: JSON status.

### **GET `/health`**
- **Description**: Basic health check for the application.
- **Returns**: `status`, `instagram_connected`, `total_reels`.
