from functools import lru_cache
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    app_name:str = "Enterprise RAG Agent"
    app_version:str="0.1.0"
    app_env:str="development"
    
    debug:bool = True
    
    log_level:str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    embedding_model:str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    
    qdrant_url:str = "http://localhost:6333"
    qdrant_collection:str ="enterprise_documents"
    
@lru_cache
def get_settings()->Settings:
    return Settings()