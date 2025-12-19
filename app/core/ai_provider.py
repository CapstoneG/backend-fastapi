from abc import ABC, abstractmethod
from typing import Optional

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text response"""
        pass
    
    @abstractmethod
    def check_health(self) -> bool:
        """Check if API is working"""
        pass

class GeminiProvider(AIProvider):
    """Google Gemini Provider"""
    
    def __init__(self, api_key: str, model: str):
        from google import genai
        self.client = genai.Client(api_key=api_key)
        self.model = model
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Gemini API Error: {str(e)}")
    
    def check_health(self) -> bool:
        try:
            self.generate_text("Hello")
            return True
        except:
            return False
        
def get_gemini_provider(api_key: str, model: str) -> GeminiProvider:
    return GeminiProvider(api_key=api_key, model=model)