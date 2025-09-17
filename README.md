# Python Clean Architecture Template

Un template base para crear aplicaciones Python siguiendo los principios de **Clean Architecture** de Robert C. Martin.

## 🏗️ Arquitectura

Este proyecto implementa una arquitectura limpia con **separación clara de responsabilidades** y **inversión de dependencias**, lo que resulta en código más mantenible, testeable y escalable.

### Principios Fundamentales

- **Regla de Dependencias**: Las dependencias siempre apuntan hacia el centro (dominio)
- **Inversión de Dependencias**: Se depende de abstracciones, no de implementaciones concretas
- **Separación de Responsabilidades**: Cada capa tiene una función específica y bien definida
- **Independencia de Frameworks**: El core de negocio es independiente de frameworks externos

## 📁 Estructura de Directorios

```
src/
├── 🏛️ domain/                    # CAPA DE DOMINIO
│   ├── entities/                # Entidades de negocio
│   ├── value_objects/           # Objetos de valor inmutables
│   ├── interfaces/              # Contratos y abstracciones
│   └── services/                # Servicios de dominio
├── 🎯 application/               # CAPA DE APLICACIÓN
│   ├── use_cases/               # Casos de uso específicos
│   ├── services/                # Servicios de aplicación
│   └── dto/                     # Data Transfer Objects
├── 🔧 infrastructure/           # CAPA DE INFRAESTRUCTURA
│   ├── config/                  # Configuración de la aplicación
│   ├── repositories/            # Implementaciones de repositorios
│   ├── external_services/       # Integración con servicios externos
│   ├── database/                # Acceso a datos y persistencia
│   └── messaging/               # Sistemas de mensajería
├── 🌐 presentation/             # CAPA DE PRESENTACIÓN
│   ├── controllers/             # Controladores (REST, GraphQL, CLI)
│   ├── middlewares/             # Middlewares de la aplicación
│   ├── validators/              # Validadores de entrada
│   ├── mappers/                 # Conversión de datos entre capas
│   └── dependencies/            # Inyección de dependencias
└── main.py                      # Punto de entrada de la aplicación
```

## 🔄 Flujo de Dependencias

```
🌐 Presentation → 🎯 Application → 🏛️ Domain
        ↓              ↓
🔧 Infrastructure ←←←←←←←←
```

### Explicación de Capas

#### 🏛️ **Domain (Núcleo de Negocio)**
- **Sin dependencias externas** - Es el corazón de la aplicación
- **Entidades**: Objetos de negocio con identidad única
- **Value Objects**: Objetos inmutables que representan conceptos del dominio
- **Interfaces**: Contratos que definen qué puede hacer el sistema
- **Services**: Lógica de negocio que no pertenece a una entidad específica

#### 🎯 **Application (Casos de Uso)**
- **Depende solo de Domain**
- **Use Cases**: Flujos específicos de la aplicación (Crear Usuario, Procesar Pago, etc.)
- **Services**: Servicios que orquestan múltiples operaciones
- **DTOs**: Objetos para transferir datos entre capas

#### 🔧 **Infrastructure (Detalles Técnicos)**
- **Implementa las interfaces del Domain**
- **Repositories**: Acceso a datos (Base de datos, APIs, archivos)
- **External Services**: Integración con servicios de terceros
- **Database**: Configuración y acceso a persistencia
- **Messaging**: Colas, eventos, notifications

#### 🌐 **Presentation (Interfaz Externa)**
- **Punto de entrada de la aplicación**
- **Controllers**: Manejan requests HTTP, GraphQL, CLI commands
- **Middlewares**: Autenticación, logging, validación global
- **Validators**: Validación de datos de entrada
- **Dependencies**: Configuración de inyección de dependencias

## 🚀 Guía de Implementación

### 1. **Definir tu Dominio**
```python
# src/domain/entities/user.py
@dataclass
class User:
    id: str
    email: str
    name: str
    
    def is_valid_email(self) -> bool:
        # Lógica de negocio pura
        return "@" in self.email
```

### 2. **Crear Interfaces**
```python
# src/domain/interfaces/user_repository.py
class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass
```

### 3. **Implementar Casos de Uso**
```python
# src/application/use_cases/create_user_use_case.py
class CreateUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository
    
    async def execute(self, request: CreateUserRequest) -> UserResponse:
        # Lógica del caso de uso
        user = User(id=generate_id(), email=request.email, name=request.name)
        saved_user = await self._repository.save(user)
        return UserResponse.from_user(saved_user)
```

### 4. **Implementar Infraestructura**
```python
# src/infrastructure/repositories/user_repository_impl.py
class DatabaseUserRepository(IUserRepository):
    def __init__(self, db_client):
        self._db = db_client
    
    async def save(self, user: User) -> User:
        # Implementación específica de base de datos
        await self._db.execute("INSERT INTO users...", user.id, user.email)
        return user
```

### 5. **Configurar Inyección de Dependencias**
```python
# src/presentation/dependencies/container.py
class Container:
    def get_user_repository(self) -> IUserRepository:
        return DatabaseUserRepository(self.get_database())
    
    def get_create_user_use_case(self) -> CreateUserUseCase:
        return CreateUserUseCase(self.get_user_repository())
```

## 🧪 Testing Strategy

- **Unit Tests**: Cada capa se testea independientemente
- **Integration Tests**: Verifican la colaboración entre capas
- **Mocks**: Se usan para aislar dependencias en los tests

```python
# Ejemplo de test unitario
def test_create_user_use_case():
    # Arrange
    mock_repository = Mock()
    use_case = CreateUserUseCase(mock_repository)
    
    # Act
    result = await use_case.execute(CreateUserRequest(email="test@example.com"))
    
    # Assert
    assert result.email == "test@example.com"
    mock_repository.save.assert_called_once()
```

## 📦 Ventajas de esta Arquitectura

- ✅ **Mantenibilidad**: Cambios localizados y predecibles
- ✅ **Testabilidad**: Fácil testing unitario con mocks
- ✅ **Escalabilidad**: Fácil agregar nuevas funcionalidades
- ✅ **Flexibilidad**: Cambiar implementaciones sin afectar el core
- ✅ **Separación de Responsabilidades**: Cada capa tiene un propósito claro
- ✅ **Independencia de Frameworks**: El dominio no depende de tecnologías específicas

## 🛠️ Próximos Pasos

1. **Define tu dominio**: Identifica las entidades principales de tu negocio
2. **Crea interfaces**: Define los contratos en `src/domain/interfaces/`
3. **Implementa casos de uso**: Agrega la lógica de aplicación en `src/application/use_cases/`
4. **Agrega persistencia**: Implementa repositorios en `src/infrastructure/repositories/`
5. **Crea controladores**: Expone tu API en `src/presentation/controllers/`

## 📚 Referencias

- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)

---

**¡Comienza a construir tu aplicación con una arquitectura sólida y mantenible!** 🚀
