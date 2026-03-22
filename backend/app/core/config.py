import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/auth/callback')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://instagram-automation-navy.vercel.app')

# Default to SQLite if DATABASE_URL is missing or still the placeholder
_db_url = os.getenv('DATABASE_URL')
if not _db_url or 'user:password' in _db_url:
    DATABASE_URL = 'sqlite:///instagram_automation.db'
else:
    DATABASE_URL = _db_url

DEFAULT_MESSAGE = "Thanks for commenting! Check back soon for more updates."
