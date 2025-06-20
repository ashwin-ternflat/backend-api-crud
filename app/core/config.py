from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    mongo_db_name: str
    app_name: str = "My Awesome API"

    class Config:
        env_file = ".env"

settings = Settings()
