from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Type
from pydantic import BaseModel
from google.genai import types

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text response"""
        pass

    @abstractmethod
    def generate_chat_response(
        self, 
        history: List[Dict[str, str]], 
        system_instruction: str,
        response_schema: Type[BaseModel]
    ) -> BaseModel:
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
        
    def generate_chat_response(
        self, 
        history: List[Dict[str, str]], 
        system_instruction: str,
        response_schema: Type[BaseModel]
    ) -> BaseModel:
        try:
            # 1. Convert history format (Dict -> SDK Format)
            # SDK mới thường nhận contents dạng list các dict hoặc object
            formatted_contents = []
            for msg in history:
                formatted_contents.append({
                    "role": msg["role"],
                    "parts": [{"text": msg["content"]}]
                })

            # 2. Config trả về JSON (Structured Output)
            generate_config = types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json",
                response_schema=response_schema, 
                system_instruction=system_instruction
            )

            # 3. Gọi Gemini
            response = self.client.models.generate_content(
                model=self.model,
                contents=formatted_contents,
                config=generate_config
            )

            return response.parsed 

        except Exception as e:
            # Log lỗi chi tiết ở đây nếu cần
            raise Exception(f"Gemini Provider Error: {str(e)}")
        
def get_gemini_provider(api_key: str, model: str) -> GeminiProvider:
    return GeminiProvider(api_key=api_key, model=model)