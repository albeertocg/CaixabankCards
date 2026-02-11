# Arquitectura del Proyecto

## Diagrama General

```
┌─────────────────────────────────────┐
│      API REST (FastAPI)             │
│  Routes → Controllers → Services    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Business Logic Layer             │
│  Services → Models → Validators      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Data Access Layer               │
│  Repositories → ODM → Database       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         MongoDB Database             │
└─────────────────────────────────────┘
```

## Estructura de Capas

### 1. API Layer (Presentación)
- Routers/Endpoints
- Request/Response validation (Pydantic)
- HTTP error handling
- CORS y seguridad

### 2. Business Logic Layer
- Services (lógica de negocio)
- Use cases
- Validaciones complejas
- Orquestación de datos

### 3. Data Access Layer
- Repositories
- Beanie (ODM async)
- Database models
- Queries

## Estructura de Carpetas

```
app/
├── routes/        # Routes y endpoints
├── models/        # Pydantic models y DB models
├── services/      # Lógica de negocio
├── repositories/  # Acceso a datos
├── errors/        # Excepciones y errores personalizados
├── utils/         # Funciones auxiliares
├── config/        # Configuración
├── constants/     # Constantes
└── tests/         # Tests
```

## Stack Tecnológico Actual

### Backend
- **Framework:** FastAPI
- **Base de datos:** MongoDB
- **ODM:** Beanie (MongoDB async)
- **Validación:** Pydantic
- **DI Container:** dependency-injector
- **Testing:** pytest
- **Linting:** ruff
- **Pre-commit hooks:** pre-commit + ruff

## Patrones

### Repository Pattern
```
Controller → Service → Repository → Database
```

### Dependency Injection con dependency-injector

```python
# TODO: Revisar y ajustar este ejemplo a la implementación real
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    # Repositories
    user_repository = providers.Singleton(UserRepository)
    
    # Services
    user_service = providers.Factory(
        UserService,
        repository=user_repository
    )

# En routers
from fastapi import Depends
from app.config.di import Container

container = Container()

@router.get("/users/{user_id}")
async def get_user(
    user_id: str,
    service: UserService = Depends(container.user_service)
):
    return await service.get(user_id)
```