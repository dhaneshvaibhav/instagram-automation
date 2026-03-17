from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.api import auth, webhook, reels, stats

app = FastAPI(title="Instagram Reel DM Bot", version="1.0.0")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(webhook.router)
app.include_router(reels.router)
app.include_router(stats.router)

@app.get("/")
async def serve_dashboard():
    dashboard_path = Path(__file__).parent.parent / "templates" / "index.html"
    if not dashboard_path.exists():
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return FileResponse(dashboard_path)
