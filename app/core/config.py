from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path
import json

from dotenv import load_dotenv
load_dotenv()
import os
from pydantic import Field

class Settings(BaseSettings):
    MONGO_URL: str = Field(...)

    GEMINI_API_KEY: str = Field(...)
    GEMINI_MODEL: str = Field(...)

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()