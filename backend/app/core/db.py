from sqlmodel import SQLModel, create_engine, Session, Field
from typing import Optional
from app.core.config import DATABASE_URL
from datetime import datetime

# Adjust DATABASE_URL for asyncpg if necessary, though SQLModel's create_engine usually handles it.
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    pass

engine = create_engine(DATABASE_URL)

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

class Stats(SQLModel, table=True):
    ig_account_id: str = Field(primary_key=True)
    total_dms: int = 0
    dms_today: int = 0
    last_reset: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
