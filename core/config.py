from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    app_name: str = "AI Recipe Wizard"
    env: str = "development"
    debug: bool = True

    openai_api_key: str
    openai_model: str = "gpt-4o-mini"  

    base_dir: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = base_dir / "data"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        extra="ignore"  # or "allow" if you prefer
    )

settings = Settings()
print("DEBUG:: Loaded settings:", settings.model_dump())