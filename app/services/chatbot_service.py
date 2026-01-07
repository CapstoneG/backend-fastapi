import os
import asyncio
from typing import List, Dict, Optional
from pydantic import BaseModel
from app.core.ai_provider import get_gemini_provider
# Note: we will use the provider's plain text `generate_text` for main responses
from app.services.lightrag_service import rag_service
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', '')


class ClassifyResponse(BaseModel):
    category: str
    reason: Optional[str] = None


class ChatbotService:
    """Simple routing pipeline:
    - Classify question as 'chat'|'grammar'|'vocab' via Gemini
    - For 'vocab': call `rag_service.query(...)` then pass its text to Gemini
    - For others: call Gemini directly
    All public calls return a plain `str` (the assistant reply).
    """

    def __init__(self, api_key: str = GEMINI_API_KEY, model: str = GEMINI_MODEL):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = get_gemini_provider(api_key, model)

    def _classify_question(self, question: str) -> str:
        system_instruction = (
            "You are a classifier. Classify the user's single question into one of:"
            " 'chat', 'grammar', 'vocab'. Return strict JSON with field 'category'."
        )

        history = [{"role": "user", "content": question}]

        parsed = self.client.generate_chat_response(
            history=history,
            system_instruction=system_instruction,
            response_schema=ClassifyResponse,
        )
        return parsed.category.lower().strip()

    def _build_system_prompt(self, task: str, context: Optional[str] = None) -> str:
        # Minimal system prompt: follow user's request directly.
        base = (
            "You are an AI English Tutor. Follow the user's request and answer directly."
            " Be concise, natural and helpful."
        )

        if task == "grammar":
            base = "(Focus on grammar corrections.) " + base
        elif task == "vocab":
            base = "(Focus on vocabulary; use provided context if available.) " + base

        if context:
            base += f"\nCONTEXT:\n{context}\n"

        return base

    def _call_gemini(self, history: List[Dict[str, str]], system_instruction: str) -> str:
        # Compose a single text prompt from the system instruction and history,
        # then call provider.generate_text and return the raw text.
        parts = [system_instruction, "\nConversation history:"]
        for m in history:
            role = m.get("role", "user")
            content = m.get("content", "")
            parts.append(f"{role.upper()}: {content}")

        prompt = "\n".join(parts)
        return self.client.generate_text(prompt)

    def _rag_query_sync(self, question: str, mode: str = "local") -> str:
        # Deprecated: kept for compatibility but not used in async flow
        return asyncio.run(rag_service.query(question, mode=mode))

    async def process_question(self, history: List[Dict[str, str]], user_message: str) -> str:
        """Main entrypoint (async): returns assistant reply as plain string.

        This function is async so it can `await` `rag_service.query` directly
        when `category == 'vocab'`.
        """
        category = self._classify_question(user_message)
        print("Classified question as:", category)

        if category == "vocab":
            # Await the LightRAG async query directly
            rag_result = await rag_service.query(user_message, mode="local")
            context_text = str(rag_result)
            system_instruction = self._build_system_prompt(task="vocab", context=context_text)
            history_payload = history + [{"role": "user", "content": user_message}]
            return self._call_gemini(history_payload, system_instruction)

        if category == "grammar":
            system_instruction = self._build_system_prompt(task="grammar")
            history_payload = history + [{"role": "user", "content": user_message}]
            return self._call_gemini(history_payload, system_instruction)

        # default: chat
        system_instruction = self._build_system_prompt(task="chat")
        history_payload = history + [{"role": "user", "content": user_message}]
        return self._call_gemini(history_payload, system_instruction)


# singleton
chatbot_service = ChatbotService()
