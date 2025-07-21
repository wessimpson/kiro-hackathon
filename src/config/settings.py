"""
Configuration settings for AI Job Application Assistant
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    app_name: str = "AI Job Application Assistant"
    debug: bool = False
    
    # Database URLs
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"
    
    postgresql_url: str = "postgresql://user:password@localhost:5432/job_assistant"
    redis_url: str = "redis://localhost:6379"
    
    # Vector Database
    pinecone_api_key: Optional[str] = None
    pinecone_environment: str = "us-west1-gcp-free"
    pinecone_index_name: str = "job-assistant-vectors"
    
    # AI Services
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    # Authentication
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # External APIs
    linkedin_api_key: Optional[str] = None
    github_token: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()