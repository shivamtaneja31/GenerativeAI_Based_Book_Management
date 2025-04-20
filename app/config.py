import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Intelligent Book Management System"
    
    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    
    @property
    def DATABASE_URL(self) -> str:
        """Get the database connection string"""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # JWT Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI Model settings
    LLAMA_MODEL_PATH: str
    LLAMA_MODEL_HOST: str = "localhost"
    LLAMA_MODEL_PORT: int = 8080
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()