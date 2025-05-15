from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8001
    
    # Scrapper service settings
    SCRAPPER_SERVICE_URL: str = "http://scrapping:9003"
    
    # Database settings
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "text_analyzer"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings() 