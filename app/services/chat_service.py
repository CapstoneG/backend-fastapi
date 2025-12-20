from app.repositories.chat_repository import ChatRepository
from app.schemas.request.create_session_request import CreateSessionRequest
from datetime import datetime
from app.core.ai_provider import get_gemini_provider
import os
from dotenv import load_dotenv
from app.schemas.conversation_response import ConversationResponse
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.variant_repository import VariantRepository

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', '')

class ChatService:
    def __init__(self):
        self.chatRepository = ChatRepository()
        self.scenarioRepository = ScenarioRepository()
        self.variantRepository = VariantRepository()
        self.client = get_gemini_provider(GEMINI_API_KEY, GEMINI_MODEL)

    def create_new_session(self, req: CreateSessionRequest):
        new_session = {
            "user_id": req.user_id,
            "variant_id": req.variant_id,
            "scenario_id": req.scenario_id,
            "context_id": req.context_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "messages": [] # Bắt đầu với mảng rỗng
        }

        result = self.chatRepository.create_new_session(new_session=new_session)

        return {
            "status": "success",
            "session_id": str(result.inserted_id)
        }
    
    def check_health(self):
        return self.client.check_health()
    
    def process_chat_message(self, session_id: str, user_message: str):
        # 1. Lấy Session & Lịch sử từ Repo
        session = self.chatRepository.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        # 2. Lấy 10 tin nhắn gần nhất để làm context
        # Convert model DB sang format {'role': '...', 'content': '...'}
        history_context = self._format_history(session.messages[-10:])

        variant_instruction = self.variantRepository.get_variant_instruction(session.variant_id)
        scenario_name, context_desc = self.scenarioRepository.get_scenario_context_details(
            session.scenario_id, 
            session.context_id
        )
        
        # 3. Thêm tin nhắn mới của user vào context gửi đi
        history_context.append({"role": "user", "content": user_message})

        # 4. Xây dựng System Prompt (Dynamic theo Scenario của session)
        system_instruction = self._build_enhanced_prompt(
            scenario_name=scenario_name,
            context_desc=context_desc,
            variant_instruction=variant_instruction
        )

        # 5. Gọi AI Provider (Trả về Pydantic Object)
        ai_response_model = self.client.generate_chat_response(
            history=history_context,
            system_instruction=system_instruction,
            response_schema=ConversationResponse 
        )

        # 6. Lưu xuống DB (Repo)
        # Lưu tin nhắn User (kèm analysis từ AI)
        self.chatRepository.add_user_message(
            session_id, 
            content=user_message, 
            analysis=ai_response_model.analysis
        )
        
        # Lưu tin nhắn AI
        self.chatRepository.add_ai_message(
            session_id, 
            content=ai_response_model.response
        )

        return ai_response_model

    def _format_history(self, db_messages):
        return [{"role": m.role, "content": m.content} for m in db_messages]

    def _build_enhanced_prompt(self, scenario_name, context_desc, variant_instruction):
        """
        Prompt chi tiết, ép AI trả về đúng format giáo dục.
        """
        return f"""
        You are an AI English Tutor role-playing a character.

        **SCENARIO SETTING:**
        - Location/Scenario: {scenario_name}
        - Specific Situation: {context_desc}
        
        **YOUR PERSONA:**
        - Accent/Dialect Instruction: {variant_instruction}
        - Tone: Natural, helpful, staying in character.
        
        **USER INFO:**
        - Proficiency Level: BEGINER (Adjust your vocabulary difficulty accordingly).

        **YOUR TASKS:**
        1. **Response:** Reply naturally to the user's message as your character. Keep the conversation going.
        2. **Analysis:** Check the user's grammar and vocabulary.
           - If there's an error, identify the topic (e.g., 'Past Tense') and provide a correction.
           - If correct, leave analysis fields null or empty.
        3. **Alternatives:** Provide 2 better ways to say what the user just said:
           - One Formal/Polite version.
           - One Casual/Native version.
        4. **Translation:** Translate your *response* (Task 1) into Vietnamese.

        **OUTPUT FORMAT:**
        Return a JSON object matching the requested schema strictly.
        """