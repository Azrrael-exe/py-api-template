from src.domain.entities.app_config import AppConfig
from src.application.use_cases.healt_check_use_case import HealthCheckUseCase
from src.application.use_cases.flip_word_use_case import FlipWordUseCase

from datetime import datetime

class Container:
    def __init__(self):
        self.app_config = AppConfig()
        self.running_since = datetime.now()

    def get_app_config(self):
        return self.app_config
    
    def get_health_check_use_case(self):
        return HealthCheckUseCase(app_config=self.app_config, running_since=self.running_since)

    def get_flip_word_use_case(self):
        return FlipWordUseCase()