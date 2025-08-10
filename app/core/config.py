import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # App config
    APP_NAME: str = "Resume Ranking System"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # Database
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017/resume_ranking")
    
    # AI Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # File upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"


settings = Settings()