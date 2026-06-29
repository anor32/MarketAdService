import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5434/ads_db"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic_ads: str = "ads"
    auth_service_url: str = "http://localhost:8000"



print('=== еременные окружения ===')
print('DATABASE_URL:', os.environ.get('DATABASE_URL'))
print('POSTGRES_CONNECTION_STRING:', os.environ.get('POSTGRES_CONNECTION_STRING'))
print()

settings = Settings()
print('=== начения из Settings ===')
print('database_url:', settings.database_url)
print('kafka_bootstrap_servers:', settings.kafka_bootstrap_servers)
print('auth_service_url:', settings.auth_service_url)
