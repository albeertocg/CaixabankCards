from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # MongoDB
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "caixabank_cards"

    # JWT
    jwt_secret_key: str = "clave_secreta_por_defecto"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
