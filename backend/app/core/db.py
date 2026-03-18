from sqlmodel import SQLModel, create_engine, Session, Field
from typing import Optional
from app.core.config import DATABASE_URL
from datetime import datetime

# Adjust DATABASE_URL for asyncpg if necessary, though SQLModel's create_engine usually handles it.
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    pass

# Neon (and AWS) connections can sometimes close SSL connections unexpectedly.
# We add pool_pre_ping=True to check if the connection is alive before using it,
# and pool_recycle to refresh connections periodically.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10
)

def init_db():
    # In a real production app, you'd use Alembic for migrations.
    # We use create_all which only creates tables that don't exist.
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
    mode: str = Field(default="dm") # 'dm' or 'reply'
    dm_message: str = Field(default="")
    public_reply: str = Field(default="")
    keyword: Optional[str] = None
    ai_enabled: bool = Field(default=False)
    ai_context: Optional[str] = Field(default=None) # Context to help AI generate better replies
    ai_summary: Optional[str] = Field(default=None) # AI-generated summary of the reel

class Stats(SQLModel, table=True):
    ig_account_id: str = Field(primary_key=True)
    total_dms: int = 0
    dms_today: int = 0
    last_reset: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
