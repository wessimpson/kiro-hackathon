"""
Configuration settings for AI Job Application Assistant
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application Settings
    app_name: str = "AI Job Application Assistant"
    debug: bool = False
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database Configuration
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"
    
    postgresql_url: str = "postgresql://user:password@localhost:5432/job_assistant"
    redis_url: str = "redis://localhost:6379"
    
    # Vector Database (Pinecone)
    pinecone_api_key: Optional[str] = None
    pinecone_environment: str = "us-west1-gcp-free"
    pinecone_index_name: str = "job-assistant-vectors"
    
    # AI Services
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    openai_embedding_model: str = "text-embedding-ada-002"
    
    # External APIs
    linkedin_api_key: Optional[str] = None
    github_token: Optional[str] = None
    twitter_bearer_token: Optional[str] = None
    
    # Email Configuration
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Web Scraping Configuration
    user_agent: str = "AI Job Application Assistant Bot 1.0"
    request_delay: int = 1
    max_retries: int = 3
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Development Settings
    reload_on_change: bool = True
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Production Settings
    use_ssl: bool = False
    secure_cookies: bool = False
    
    # CrewAI Configuration
    crewai_verbose: bool = True
    crewai_memory: bool = True
    crewai_max_execution_time: int = 300  # 5 minutes
    
    # Knowledge Graph Configuration
    kg_max_connection_pool_size: int = 50
    kg_connection_timeout: int = 30
    
    # Vector Database Configuration
    vector_dimension: int = 1536  # OpenAI embedding dimension
    vector_metric: str = "cosine"
    
    @property
    def database_url(self) -> str:
        """Alias for postgresql_url for compatibility"""
        return self.postgresql_url
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.debug
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return not self.debug
    
    def validate_required_settings(self) -> List[str]:
        """Validate that required settings are present"""
        missing = []
        
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY")
        
        if not self.pinecone_api_key and not self.is_development:
            missing.append("PINECONE_API_KEY")
        
        if not self.secret_key or self.secret_key == "your-secret-key-change-in-production":
            if self.is_production:
                missing.append("SECRET_KEY")
        
        return missing
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_prefix = ""


# Global settings instance
settings = Settings()

# Validate settings on import
missing_settings = settings.validate_required_settings()
if missing_settings and not os.getenv("SKIP_SETTINGS_VALIDATION"):
    import warnings
    warnings.warn(
        f"Missing required environment variables: {', '.join(missing_settings)}. "
        f"Please check your .env file or environment configuration."
    )