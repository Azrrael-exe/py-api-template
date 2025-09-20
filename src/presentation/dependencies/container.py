from src.domain.entities.app_config import AppConfig
from src.application.use_cases.healt_check_use_case import HealthCheckUseCase
from src.application.use_cases.flip_word_use_case import FlipWordUseCase
from src.application.use_cases.repository_use_case import SaveKeyUseCase, GetKeyUseCase, DeleteKeyUseCase
from src.infrastructure.repositories.in_memory import InMemoryStorage
from src.infrastructure.repositories.redis_repository import RedisRepository

import os
from datetime import datetime

class Container:
    def __init__(self):
        self.app_config = AppConfig()
        self.running_since = datetime.now()
        
        # Configurar storage basado en variables de entorno
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_db = int(os.getenv('REDIS_DB', '0'))
        
        # Intentar conectar a Redis, si falla usar InMemoryStorage como fallback
        try:
            self.storage = RedisRepository(
                host=redis_host,
                port=redis_port,
                db=redis_db
            )
            print(f"✅ Usando Redis como storage: {redis_host}:{redis_port}")
        except Exception as e:
            print(f"⚠️  Error conectando a Redis: {e}")
            print("🔄 Usando InMemoryStorage como fallback")
            self.storage = InMemoryStorage()

    def get_app_config(self):
        return self.app_config
    
    def get_health_check_use_case(self):
        return HealthCheckUseCase(app_config=self.app_config, running_since=self.running_since)

    def get_flip_word_use_case(self):
        return FlipWordUseCase()
    
    def get_save_key_use_case(self):
        return SaveKeyUseCase(storage=self.storage)
    
    def get_get_key_use_case(self):
        return GetKeyUseCase(storage=self.storage)
    
    def get_delete_key_use_case(self):
        return DeleteKeyUseCase(storage=self.storage)