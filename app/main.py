from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.api import auth, webhook, reels, stats

app = FastAPI(title="Instagram Reel DM Bot", version="1.0.0")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers FIRST
app.include_router(auth.router)
app.include_router(webhook.router)
app.include_router(reels.router)
app.include_router(stats.router)

# Serve the React Frontend from 'frontend/dist'
# This is where your built React files will live.
dist_path = Path(__file__).parent.parent / "frontend" / "dist"

# Catch-all route to serve index.html for React Router (SPA support)
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    # Check if the requested file exists in dist
    file_path = dist_path / full_path
    if file_path.is_file():
        return FileResponse(file_path)
    
    # Otherwise, serve index.html for all other routes
    index_path = dist_path / "index.html"
    if not index_path.exists():
        return {"error": "Frontend build not found. Please run 'npm run build' in the frontend directory."}
    return FileResponse(index_path)
