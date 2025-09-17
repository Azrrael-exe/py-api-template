from src.domain.entities.app_config import AppConfig
from datetime import datetime

class HealthCheckUseCase:
    def __init__(self, app_config: AppConfig, running_since: datetime):
        self.app_config = app_config
        self.running_since = running_since

    async def execute(self):
        running_time = (datetime.now() - self.running_since).total_seconds()
        return {
            "app_name": self.app_config.app_name,
            "env": self.app_config.env,
            "running_time": running_time,
        }