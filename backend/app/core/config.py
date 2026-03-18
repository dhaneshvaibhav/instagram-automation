import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/auth/callback')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

DEFAULT_MESSAGE = "Thanks for commenting! Check back soon for more updates."
