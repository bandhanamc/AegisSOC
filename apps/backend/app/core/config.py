from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "AegisSOC Backend"
    APP_VERSION: str = "0.1.0"

    ENVIRONMENT: str = "development"

    # Database Configuration
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "aegissoc"
    POSTGRES_USER: str = "aegissoc"
    POSTGRES_PASSWORD: str = "change_this_password"

    # Logging
    LOG_LEVEL: str = "INFO"

    # JWT Security Configuration
    JWT_SECRET_KEY: str
    JWT_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()