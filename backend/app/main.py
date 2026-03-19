from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, webhook, reels, stats
from app.core.db import init_db

import logging
from app.core.config import FRONTEND_URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Instagram Reel DM Bot", version="1.0.0")

@app.on_event("startup")
def on_startup():
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized.")

# Add CORS Middleware
allowed_origins = [FRONTEND_URL] if FRONTEND_URL else ["*"]
if "*" in allowed_origins:
    logger.warning("CORS allowed origins set to '*'. This should be restricted in production.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
