from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./sitrep_fusion.db"
    sitrep_api_key: str = "change-me"
    openai_api_key: str = ""
    fusion_distance_meters: int = 650
    fusion_time_window_seconds: int = 90

    class Config:
        env_file = ".env"

settings = Settings()
