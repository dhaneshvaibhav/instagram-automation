from sqlmodel import SQLModel, create_engine, Session, Field
from typing import Optional, List
from app.core.config import DATABASE_URL
from datetime import datetime
import json

# SQLite needs check_same_thread=False for FastAPI
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

def init_db():
    # Only create tables if they don't exist.
    # In a real production app, you'd use Alembic for migrations.
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# Models
class Token(SQLModel, table=True):
    ig_account_id: str = Field(primary_key=True)
    access_token: str
    username: str
    name: Optional[str] = None
    profile_picture_url: Optional[str] = None
    followers_count: Optional[int] = 0
    follows_count: Optional[int] = 0
    media_count: Optional[int] = 0
    biography: Optional[str] = ""
    expires_at: Optional[datetime] = None

class Reel(SQLModel, table=True):
    ig_account_id: str = Field(primary_key=True)
    reel_id: str = Field(primary_key=True)
    message: str
    keyword: Optional[str] = None
    # JSON-encoded string of buttons: [{"type": "web_url", "url": "...", "title": "..."}, ...]
    buttons: Optional[str] = None 

class Stats(SQLModel, table=True):
    ig_account_id: str = Field(primary_key=True)
    total_dms: int = 0
    dms_today: int = 0
    last_reset: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

class Subscription(SQLModel, table=True):
    ig_account_id: str = Field(primary_key=True)
    plan: str = Field(default="starter")  # starter, pro, business
    started_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    expires_at: Optional[str] = None
    is_first_time: bool = Field(default=True)
    is_trial: bool = Field(default=True)  # 7-day free trial for starter
    trial_started_at: Optional[str] = None
