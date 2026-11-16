from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    OPEN_ROUTER_KEY: str
    OPEN_ROUTER_URL: str
    MODEL: str
    VECTORS_MODEL: str
    SYNC_DB_URL: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def database_url(self) -> str:
        return self.DATABASE_URL


settings = Settings()
