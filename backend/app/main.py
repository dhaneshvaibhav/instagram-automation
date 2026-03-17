from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, webhook, reels, stats
from app.core.db import init_db

app = FastAPI(title="Instagram Reel DM Bot", version="1.0.0")

@app.on_event("startup")
def on_startup():
    init_db()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for easier deployment; restrict this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router)
app.include_router(webhook.router)
app.include_router(reels.router)
app.include_router(stats.router)

@app.get("/")
async def root():
    return {"message": "Instagram DM Bot API is running"}
