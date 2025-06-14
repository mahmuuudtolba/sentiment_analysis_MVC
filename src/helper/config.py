from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    GITHUB_TOKEN:str
    APP_VERSION:str
    APP_NAME:str


    model_config = SettingsConfigDict(env_file=".env")


def get_settings():
    return Settings()