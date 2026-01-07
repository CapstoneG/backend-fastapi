import os
import nest_asyncio
from functools import partial
from lightrag import LightRAG, QueryParam
from lightrag.llm.gemini import gemini_model_complete, gemini_embed
from lightrag.utils import EmbeddingFunc
from dotenv import load_dotenv


# Patch asyncio để tránh lỗi conflict event loop trong môi trường server
nest_asyncio.apply()

class LightRAGService:
    def __init__(self, working_dir: str = "./rag_storage_new", api_key: str = None):
        self.working_dir = working_dir
        self.rag_instance = None
        
        # Cấu hình API Key
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
            
        # Kiểm tra thư mục
        if not os.path.exists(self.working_dir):
            os.mkdir(self.working_dir)

        print(self.api_key)

    async def _llm_model_func(self, prompt, system_prompt=None, history_messages=[], **kwargs):
        return await gemini_model_complete(
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key=self.api_key,
            model_name="gemini-2.5-flash", # Model bạn đang dùng
            **kwargs,
        )

    def _get_embedding_func(self):
        return EmbeddingFunc(
            embedding_dim=768,
            max_token_size=2048,
            func=partial(
                gemini_embed.func,
                api_key=self.api_key,
                model="models/text-embedding-004"
            )
        )

    async def initialize(self):
        """Khởi tạo LightRAG và load storage. Hàm này cần chạy khi Start App."""
        print("⏳ Đang khởi tạo LightRAG Service...")
        self.rag_instance = LightRAG(
            working_dir=self.working_dir,
            llm_model_func=self._llm_model_func,
            embedding_func=self._get_embedding_func(),
            llm_model_name="gemini-2.5-flash",
        )
        await self.rag_instance.initialize_storages()
        print("✅ LightRAG Service đã sẵn sàng!")

    async def insert_content(self, content: str):
        """Hàm nạp dữ liệu vào RAG"""
        if not self.rag_instance:
            await self.initialize()
        return await self.rag_instance.insert(content)

    async def query(self, question: str, mode: str = "local"):
        """
        Hàm gọi query từ bên ngoài.
        mode: 'naive', 'local', 'global', 'hybrid', 'mix'
        """
        if not self.rag_instance:
            # Nếu chưa init thì init (phòng hờ, nhưng tốt nhất nên init lúc start app)
            await self.initialize()
            
        print(f"🔍 Đang truy vấn RAG với mode: {mode}")
        
        # LightRAG query có thể block, nên cẩn thận nếu nó không phải async native hoàn toàn
        # Tuy nhiên hàm query của LightRAG thường trả về kết quả trực tiếp
        result = self.rag_instance.query(question, param=QueryParam(mode=mode))
        return result

# Tạo một biến global instance để dùng dạng Singleton (tiết kiệm ram)
rag_service = LightRAGService()