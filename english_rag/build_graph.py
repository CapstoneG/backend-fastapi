"""
LightRAG Demo with Google Gemini Models

This example demonstrates how to use LightRAG with Google's Gemini 2.0 Flash model
for text generation and the text-embedding-004 model for embeddings.

Prerequisites:
    1. Set GEMINI_API_KEY environment variable:
       export GEMINI_API_KEY='your-actual-api-key'

    2. Prepare a text file named 'book.txt' in the current directory
       (or modify BOOK_FILE constant to point to your text file)

Usage:
    python examples/lightrag_gemini_demo.py
"""

import os
import asyncio
import nest_asyncio
import numpy as np

from lightrag import LightRAG, QueryParam
from lightrag.llm.gemini import gemini_model_complete, gemini_embed
from lightrag.utils import wrap_embedding_func_with_attrs, EmbeddingFunc
from functools import partial

nest_asyncio.apply()

WORKING_DIR = "./rag_storage_new"
BOOK_FILE = "./book.txt"

# Validate API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set. "
        "Please set it with: export GEMINI_API_KEY='your-api-key'"
    )

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


# --------------------------------------------------
# LLM function
# --------------------------------------------------
async def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
    return await gemini_model_complete(
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=GEMINI_API_KEY,
        model_name="gemini-2.5-flash",
        **kwargs,
    )


# --------------------------------------------------
# Embedding function
# --------------------------------------------------
embedding_func = EmbeddingFunc(
    embedding_dim=768,
    max_token_size=2048,
    func=partial(
        gemini_embed.func,
        api_key=GEMINI_API_KEY,
        model="models/text-embedding-004"
    )
)


# --------------------------------------------------
# Initialize RAG
# --------------------------------------------------
async def initialize_rag():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=llm_model_func,
        embedding_func=embedding_func,
        llm_model_name="gemini-2.5-flash",
    )

    # 🔑 REQUIRED
    await rag.initialize_storages()
    return rag


# --------------------------------------------------
# Main
# --------------------------------------------------
def main():
    # Validate book file exists

    rag = asyncio.run(initialize_rag())

    # DATASET_DIR = "./reading_topic"
    # files = [f for f in os.listdir(DATASET_DIR) if f.endswith(".txt")]
    # files = files[:3]
    # print(f"📂 Tìm thấy {len(files)} tài liệu. Bắt đầu nạp...")
    # for filename in files:
    #     file_path = os.path.join(DATASET_DIR, filename)
    #     if not os.path.exists(file_path): continue
    #     print(f"⏳ Đang nạp: {filename} ...")
    #     try:
    #         with open(file_path, "r", encoding="utf-8") as f:
    #             content = f.read()
    #         rag.insert(content)
    #         print(f"✅ Xong: {filename}")
    #     except Exception as e:

    #         print(f"❌ Lỗi file {filename}: {e}")

    # DATASET_DIR = "./reading_output"
    # files = [f for f in os.listdir(DATASET_DIR) if f.endswith(".txt")]
    # files = files[:3]
    # print(f"📂 Tìm thấy {len(files)} tài liệu để truy vấn.")
    # for filename in files:
    #     file_path = os.path.join(DATASET_DIR, filename)
    #     if not os.path.exists(file_path): continue
    #     print(f"⏳ Đang nạp: {filename} ...")
    #     try:
    #         with open(file_path, "r", encoding="utf-8") as f:
    #             content = f.read()
    #         rag.insert(content)
    #         print(f"✅ Xong: {filename}")
    #     except Exception as e:

    #         print(f"❌ Lỗi file {filename}: {e}")

    # print("📚 Nạp tài liệu hoàn tất.")


    query = "gợi ý tôi khi nói về môi trường thì nói về các mục nào"

    print("\nNaive Search:")
    print(rag.query(query, param=QueryParam(mode="naive")))

    print("\nLocal Search:")
    print(rag.query(query, param=QueryParam(mode="local")))

    print("\nGlobal Search:")
    print(rag.query(query, param=QueryParam(mode="global")))

    print("\nHybrid Search:")
    print(rag.query(query, param=QueryParam(mode="hybrid")))

    print("\nMixed Search:")
    print(rag.query(query, param=QueryParam(mode="mix")))


if __name__ == "__main__":
    main()