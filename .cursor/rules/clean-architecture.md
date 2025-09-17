---
description: 
globs: 
alwaysApply: false
---

# Clean Architecture Template Rules

## Overview

Este repositorio implementa una **Arquitectura Limpia (Clean Architecture)** siguiendo los principios de Robert C. Martin. Úsalo como template para crear nuevos proyectos de cualquier dominio siguiendo estos principios arquitectónicos.

## Estructura de Directorios

```
src/
├── domain/                 # Capa de Dominio - Entidades y Interfaces
│   ├── entities/          # Entidades de negocio
│   ├── value_objects/     # Objetos de valor
│   ├── interfaces/        # Contratos/Interfaces abstractas
│   └── services/          # Servicios de dominio
├── application/           # Capa de Aplicación - Casos de Uso
│   ├── use_cases/         # Casos de uso específicos
│   ├── services/          # Servicios de aplicación
│   └── dto/              # Data Transfer Objects
├── infrastructure/       # Capa de Infraestructura - Implementaciones
│   ├── config/           # Configuración
│   ├── repositories/     # Implementaciones de repositorios
│   ├── external_services/ # Servicios externos
│   ├── database/         # Acceso a datos
│   └── messaging/        # Sistemas de mensajería
└── presentation/        # Capa de Presentación - Interfaces externas
    ├── controllers/      # Controladores (REST, GraphQL, etc.)
    ├── middlewares/      # Middlewares
    ├── validators/       # Validadores de entrada
    ├── mappers/         # Mappers para conversión de datos
    └── dependencies/    # Inyección de dependencias
```

## Principios de Arquitectura Limpia

### 1. Dependencias hacia adentro
- **Domain**: No depende de nada (núcleo puro)
- **Application**: Solo depende de Domain
- **Infrastructure**: Depende de Domain y Application
- **Presentation**: Depende de todas las capas

### 2. Inversión de Dependencias
- Define interfaces abstractas en `domain/interfaces/`
- Implementa en la capa `infrastructure/`
- Inyecta dependencias en `presentation/dependencies/`

### 3. Separación de Responsabilidades
- **Domain**: Lógica de negocio pura, reglas de dominio
- **Application**: Orquestación de casos de uso, flujos de trabajo
- **Infrastructure**: Detalles técnicos (persistencia, APIs externas, frameworks)
- **Presentation**: Interfaz con el mundo exterior (controladores, UI, APIs)

## Guía de Implementación

### 1. Definir Entidades de Dominio

```python
# src/domain/entities/your_entity.py
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class EntityStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

@dataclass
class YourEntity:
    id: str
    name: str
    status: EntityStatus
    
    def is_active(self) -> bool:
        """Lógica de negocio pura"""
        return self.status == EntityStatus.ACTIVE
    
    def can_be_modified(self) -> bool:
        """Reglas de dominio"""
        return self.is_active()
```

### 2. Crear Interfaces de Dominio

```python
# src/domain/interfaces/your_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.your_entity import YourEntity

class IYourRepository(ABC):
    @abstractmethod
    async def find_by_id(self, entity_id: str) -> Optional[YourEntity]:
        pass
    
    @abstractmethod
    async def find_all(self) -> List[YourEntity]:
        pass
    
    @abstractmethod
    async def save(self, entity: YourEntity) -> YourEntity:
        pass
    
    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        pass
```

### 3. Implementar Casos de Uso

```python
# src/application/use_cases/create_entity_use_case.py
from typing import Optional
from ..dto.entity_dto import CreateEntityRequest, EntityResponse
from ...domain.interfaces.your_repository import IYourRepository
from ...domain.entities.your_entity import YourEntity, EntityStatus

class CreateEntityUseCase:
    def __init__(self, repository: IYourRepository):
        self._repository = repository
    
    async def execute(self, request: CreateEntityRequest) -> EntityResponse:
        # Validación de reglas de negocio
        existing = await self._repository.find_by_id(request.id)
        if existing:
            raise ValueError("Entity already exists")
        
        # Crear entidad de dominio
        entity = YourEntity(
            id=request.id,
            name=request.name,
            status=EntityStatus.ACTIVE
        )
        
        # Guardar a través del repositorio
        saved_entity = await self._repository.save(entity)
        
        # Retornar DTO
        return EntityResponse.from_entity(saved_entity)
```

### 4. Crear Implementaciones de Infraestructura

```python
# src/infrastructure/repositories/your_repository_impl.py
from typing import List, Optional
from ...domain.interfaces.your_repository import IYourRepository
from ...domain.entities.your_entity import YourEntity

class DatabaseYourRepository(IYourRepository):
    def __init__(self, database_client):
        self._db = database_client
    
    async def find_by_id(self, entity_id: str) -> Optional[YourEntity]:
        # Implementación específica para base de datos
        record = await self._db.fetch_one(
            "SELECT * FROM entities WHERE id = ?", entity_id
        )
        return self._map_to_entity(record) if record else None
    
    async def find_all(self) -> List[YourEntity]:
        # Implementación específica
        records = await self._db.fetch_all("SELECT * FROM entities")
        return [self._map_to_entity(record) for record in records]
    
    async def save(self, entity: YourEntity) -> YourEntity:
        # Implementación específica
        await self._db.execute(
            "INSERT OR REPLACE INTO entities (id, name, status) VALUES (?, ?, ?)",
            entity.id, entity.name, entity.status.value
        )
        return entity
    
    def _map_to_entity(self, record) -> YourEntity:
        # Mapeo de datos de infraestructura a entidad de dominio
        pass
```

### 5. Configurar Inyección de Dependencias

```python
# src/presentation/dependencies/container.py
from ...domain.interfaces.your_repository import IYourRepository
from ...infrastructure.repositories.your_repository_impl import DatabaseYourRepository
from ...application.use_cases.create_entity_use_case import CreateEntityUseCase

class Container:
    def __init__(self, database_client):
        self._database_client = database_client
    
    def get_repository(self) -> IYourRepository:
        return DatabaseYourRepository(self._database_client)
    
    def get_create_entity_use_case(self) -> CreateEntityUseCase:
        repository = self.get_repository()
        return CreateEntityUseCase(repository)
```

### 6. Crear Controladores de Presentación

```python
# src/presentation/controllers/entity_controller.py
from typing import Dict, Any
from ..dependencies.container import Container
from ...application.dto.entity_dto import CreateEntityRequest, EntityResponse

class EntityController:
    def __init__(self, container: Container):
        self._container = container
    
    async def create_entity(self, request_data: Dict[str, Any]) -> EntityResponse:
        # Validar y mapear entrada
        request = CreateEntityRequest(**request_data)
        
        # Ejecutar caso de uso
        use_case = self._container.get_create_entity_use_case()
        response = await use_case.execute(request)
        
        return response
    
    async def get_entity(self, entity_id: str) -> EntityResponse:
        # Implementar caso de uso de consulta
        pass
```

## Patrones de Implementación

### 1. Repository Pattern
- Define interfaces en `domain/interfaces/`
- Implementa en `infrastructure/repositories/`
- Abstrae el acceso a datos

### 2. Use Case Pattern
- Un caso de uso por archivo en `application/use_cases/`
- Recibe dependencias por constructor
- Encapsula lógica de aplicación específica

### 3. Dependency Injection Pattern
- Usa un contenedor de dependencias
- Configura en `presentation/dependencies/`
- Permite fácil testing y intercambio de implementaciones

### 4. DTO Pattern
```python
# src/application/dto/entity_dto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateEntityRequest:
    name: str
    description: Optional[str] = None

@dataclass
class EntityResponse:
    id: str
    name: str
    status: str
    
    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=entity.id,
            name=entity.name,
            status=entity.status.value
        )
```

## Integración con Servicios Externos

### 1. External Service Provider
```python
# src/infrastructure/external_services/your_service.py
from ...domain.interfaces.external_service import IExternalService

class YourExternalServiceImpl(IExternalService):
    def __init__(self, api_client, config):
        self._client = api_client
        self._config = config
    
    async def call_external_api(self, data):
        # Implementación específica de la API externa
        response = await self._client.post("/endpoint", data)
        return self._map_response(response)
    
    def _map_response(self, response):
        # Mapear respuesta externa a entidades de dominio
        pass
```

### 2. Configuration Management
```python
# src/infrastructure/config/settings.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    username: str
    password: str

@dataclass
class AppConfig:
    database: DatabaseConfig
    api_key: str
    debug: bool = False
```

## Testing Strategy

### 1. Unit Tests - Domain Layer
```python
# tests/unit/domain/entities/test_your_entity.py
from src.domain.entities.your_entity import YourEntity, EntityStatus

def test_entity_creation():
    entity = YourEntity(id="1", name="test", status=EntityStatus.ACTIVE)
    assert entity.id == "1"
    assert entity.is_active() == True

def test_business_rules():
    inactive_entity = YourEntity(id="2", name="test", status=EntityStatus.INACTIVE)
    assert inactive_entity.can_be_modified() == False
```

### 2. Unit Tests - Application Layer
```python
# tests/unit/application/use_cases/test_create_entity_use_case.py
import pytest
from unittest.mock import Mock
from src.application.use_cases.create_entity_use_case import CreateEntityUseCase

@pytest.mark.asyncio
async def test_create_entity_success():
    # Arrange
    mock_repository = Mock()
    mock_repository.find_by_id.return_value = None
    use_case = CreateEntityUseCase(mock_repository)
    
    # Act & Assert
    request = CreateEntityRequest(id="1", name="test")
    response = await use_case.execute(request)
    
    assert response.id == "1"
    mock_repository.save.assert_called_once()
```

### 3. Integration Tests
```python
# tests/integration/test_entity_workflow.py
@pytest.mark.asyncio
async def test_complete_entity_workflow():
    # Test completo del flujo de trabajo
    container = Container(test_database_client)
    controller = EntityController(container)
    
    # Crear entidad
    response = await controller.create_entity({"id": "1", "name": "test"})
    assert response.id == "1"
    
    # Verificar que existe
    retrieved = await controller.get_entity("1")
    assert retrieved.name == "test"
```

## Checklist para Nuevos Proyectos

### Capa de Dominio
- [ ] Definir entidades de negocio en `src/domain/entities/`
- [ ] Crear objetos de valor en `src/domain/value_objects/`
- [ ] Definir interfaces/contratos en `src/domain/interfaces/`
- [ ] Implementar servicios de dominio si es necesario

### Capa de Aplicación
- [ ] Crear DTOs en `src/application/dto/`
- [ ] Implementar casos de uso en `src/application/use_cases/`
- [ ] Definir servicios de aplicación en `src/application/services/`

### Capa de Infraestructura
- [ ] Implementar repositorios en `src/infrastructure/repositories/`
- [ ] Crear servicios externos en `src/infrastructure/external_services/`
- [ ] Configurar acceso a datos en `src/infrastructure/database/`
- [ ] Definir configuración en `src/infrastructure/config/`

### Capa de Presentación
- [ ] Crear controladores en `src/presentation/controllers/`
- [ ] Configurar inyección de dependencias en `src/presentation/dependencies/`
- [ ] Implementar validadores en `src/presentation/validators/`
- [ ] Crear mappers para conversión de datos

### Testing y Documentación
- [ ] Escribir tests unitarios para cada capa
- [ ] Implementar tests de integración
- [ ] Documentar interfaces y casos de uso complejos
- [ ] Configurar variables de entorno
- [ ] Actualizar dependencias del proyecto

## Mejores Prácticas

### Principios Arquitectónicos
1. **Regla de Dependencias**: Las dependencias siempre apuntan hacia adentro (hacia el dominio)
2. **Inversión de Dependencias**: Usa abstracciones, no implementaciones concretas
3. **Separación de Responsabilidades**: Cada capa tiene una responsabilidad específica y bien definida
4. **Principio de Responsabilidad Única**: Cada clase/módulo debe tener una sola razón para cambiar

### Implementación
5. **Interfaces primero**: Define contratos antes que implementaciones
6. **Inyección de dependencias**: Configura dependencias externamente, no dentro de las clases
7. **Inmutabilidad**: Prefiere objetos inmutables cuando sea posible
8. **Validación en capas**: Valida datos en cada frontera de capa

### Testing
9. **Test por capa**: Escribe tests unitarios específicos para cada capa
10. **Mocks para dependencias**: Usa mocks para aislar las unidades bajo prueba
11. **Tests de integración**: Verifica que las capas funcionan correctamente juntas

### Código Limpio
12. **Nomenclatura clara**: Usa nombres descriptivos para clases, métodos y variables
13. **Funciones pequeñas**: Mantén funciones y métodos pequeños y enfocados
14. **Manejo de errores consistente**: Implementa una estrategia uniforme de manejo de errores
15. **Documentación**: Documenta decisiones arquitectónicas importantes y APIs públicas

Esta estructura te permitirá crear aplicaciones escalables, testeables y mantenibles siguiendo los principios de Clean Architecture, aplicable a cualquier dominio de negocio.
