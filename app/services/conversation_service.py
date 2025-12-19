from app.core.ai_provider import get_gemini_provider
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', '')

class ConversationService:
    def __init__(self):
        self.client = get_gemini_provider(GEMINI_API_KEY, GEMINI_MODEL)

    def check_health(self):
        return self.client.check_health()
