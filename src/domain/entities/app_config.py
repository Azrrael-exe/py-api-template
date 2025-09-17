from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class AppConfig(BaseSettings):

    PORT: int = 8080
    BASE_PATH: str = "app-agent"

    app_name: str = "py-api-template"
    env: str = "local"

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="allow"
    )

