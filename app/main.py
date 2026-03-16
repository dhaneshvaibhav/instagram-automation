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

@app.get('/')
async def serve_dashboard():
    # Looking for templates directory in the root
    template_path = Path(__file__).parent.parent / "templates" / "index.html"
    if not template_path.exists():
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return FileResponse(template_path, media_type="text/html")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app.main:app", host='0.0.0.0', port=5000, reload=True)
