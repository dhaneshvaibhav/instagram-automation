# Architecture & Connection

This document explains how the Frontend and Backend communicate and the overall system architecture.

## Frontend-Backend Connection

The application uses a decoupled architecture where the Frontend (React) communicates with the Backend (FastAPI) via RESTful APIs.

- **API Client**: The frontend uses `axios` (configured in `frontend/src/api.js`) to make requests.
- **Base URL**: Controlled by the `VITE_API_URL` environment variable.
- **Authentication**: Uses Instagram OAuth. The backend handles the redirect to Instagram and the callback exchange. Once authenticated, the token is stored in the database, and the frontend polls the `/auth/status` endpoint to verify connectivity.

## System Workflow

1. **User Login**: User connects their Instagram account via OAuth.
2. **Rule Creation**: User defines a "Keyword" and a "Message" (with optional buttons) for a specific Reel.
3. **Webhook Trigger**: 
   - Instagram sends a POST request to `/webhook` when a comment is made.
   - Backend verifies the signature (`X-Hub-Signature-256`).
   - Backend matches the Reel ID and Keyword.
4. **Action**: Backend calls the Instagram Graph API to send a DM to the commenter.

## Deployment Strategy

### Backend (e.g., Render, Railway, DigitalOcean)
- The backend is a Python FastAPI app.
- It requires a persistent PostgreSQL database.
- Ensure `FRONTEND_URL` in backend `.env` matches the deployed frontend URL to allow CORS.

### Frontend (e.g., Vercel, Netlify)
- The frontend is a static React site built with Vite.
- Ensure `VITE_API_URL` points to the deployed backend API.

### Database
- Uses PostgreSQL. 
- Schema is managed by SQLModel. 
- Migration for the `buttons` column was performed manually via `ALTER TABLE`.
