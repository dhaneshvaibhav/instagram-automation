# Getting Started with Reelzy

Reelzy is an Instagram automation tool that triggers Direct Messages based on Reel comments. This guide covers local setup and development.

## Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **PostgreSQL Database** (e.g., Neon.tech)
- **Meta Developer Account** with an Instagram Business App.

## Local Setup

### 1. Backend Setup
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate      # Mac/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend` root (see `.env.example` if available) with:
   - `APP_ID`: Your Meta App ID.
   - `APP_SECRET`: Your Meta App Secret.
   - `VERIFY_TOKEN`: A custom string for webhook verification.
   - `DATABASE_URL`: Your PostgreSQL connection string.
   - `FRONTEND_URL`: Usually `http://localhost:5173` for local dev.
5. Start the server:
   ```bash
   uvicorn app.main:app --reload --port 5000
   ```

### 2. Frontend Setup
1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file in the `frontend` root:
   - `VITE_API_URL`: `http://localhost:5000`
4. Start the development server:
   ```bash
   npm run dev
   ```

## Webhook Testing (Local)
To receive Instagram comments locally, you must use a tool like **ngrok** to expose your local port 5000:
```bash
ngrok http 5000
```
Then, update your **Callback URL** in the Meta Developer Portal to: `https://your-ngrok-url.ngrok-free.app/webhook`.
