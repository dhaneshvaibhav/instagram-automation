import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/auth/callback')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
DATABASE_URL = os.getenv('DATABASE_URL')

# File paths
TOKEN_FILE = "token.json"
REELS_FILE = "reels.json"
STATS_FILE = "stats.json"

DEFAULT_MESSAGE = "Thanks for commenting! Check back soon for more updates."
