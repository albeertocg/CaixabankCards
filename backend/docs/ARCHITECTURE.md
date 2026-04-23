# Arquitectura del Proyecto

## Diagrama General

```
┌─────────────────────────────────────────────┐
│      Cliente (Next.js)                       │
│  HTTP REST + WebSocket (/api/chat/ws/...)    │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│      API Layer (FastAPI)                     │
│  routes/ → schemas (Pydantic)                │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│      Business Logic Layer                    │
│  services/ (auth, chat, gower...)            │
│  agent/   (Google ADK + RAG sobre ChromaDB)  │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│      Data Access Layer                       │
│  repositories/ → motor (async MongoDB)       │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│      MongoDB Atlas                           │
└─────────────────────────────────────────────┘
```

## Estructura de Capas

### 1. API Layer (`app/routes/`)
- Routers de FastAPI (`auth_routes`, `card_routes`, `chat_routes`).
- Validación request/response con Pydantic (`app/schemas/`).
- Manejo de errores HTTP y CORS.
- Endpoint WebSocket para el chat en tiempo real.

### 2. Business Logic Layer (`app/services/`, `app/agent/`)
- Servicios: `auth_service`, `chat_service`, `gower_service`.
- Agente conversacional (Google ADK) con RAG sobre ChromaDB.
- Orquestación de datos y reglas de recomendación de tarjetas.

### 3. Data Access Layer (`app/repositories/`)
- Acceso asíncrono a MongoDB vía `motor`.
- Los repositorios encapsulan las consultas y mappean a/desde los modelos Pydantic.

## Estructura de Carpetas

```
backend/
├── app/
│   ├── main.py            # Entrypoint FastAPI
│   ├── agent/             # Agente Google ADK + RAG (ChromaDB)
│   ├── config/            # Settings (pydantic-settings), DB
│   ├── constants/         # Enums y constantes de dominio
│   ├── dtos/              # DTOs (UserCreate, UserResponse...)
│   ├── errors/            # Excepciones personalizadas
│   ├── models/            # Modelos Pydantic de dominio (User, Transaction)
│   ├── repositories/      # Acceso a MongoDB (motor)
│   ├── routes/            # Routers FastAPI
│   ├── schemas/           # Schemas request/response por endpoint
│   ├── services/          # Lógica de negocio
│   ├── utils/             # Utilidades
│   └── tests/             # Tests (pytest) — ver TESTING.md
├── scripts/               # seed_users.py, seed_test_users.py
├── docs/                  # Esta documentación
├── requirements.txt
└── Makefile
```

## Stack Tecnológico

### Backend
- **Framework:** FastAPI (`fastapi[standard]`)
- **Base de datos:** MongoDB (Atlas)
- **Driver async:** `motor` (no se usa Beanie)
- **Validación:** Pydantic v2 + `pydantic-settings`
- **Autenticación:** JWT con `python-jose[cryptography]`, hashing con `passlib[bcrypt]`
- **Agente IA:** `google-adk` (Google ADK) con Gemini
- **Vector store (RAG):** `chromadb`
- **Testing:** `pytest` + `httpx`
- **Linting/formato:** `ruff`
- **Pre-commit:** `pre-commit` + `ruff`

## Patrones

### Repository Pattern
```
Route → Service → Repository → MongoDB
```
Los servicios no acceden a la base de datos directamente; delegan en repositorios ubicados en `app/repositories/`.

### Inyección de dependencias
El proyecto **no** usa un contenedor DI externo. Los servicios se instancian directamente o a nivel de módulo, y FastAPI cubre la DI de los request params. Ejemplo real (`chat_routes.py`):

```python
router = APIRouter(prefix="/api/chat", tags=["Chat"])
chat_service = ChatService()

@router.post("/message")
async def send_message(request: ChatMessageRequest):
    return await chat_service.send_message(...)
```

### Agente + RAG
El `chat_service` orquesta:
1. Sesión del agente (Google ADK).
2. Recuperación de contexto relevante desde ChromaDB (índice de tarjetas, políticas).
3. Generación de respuesta con Gemini.

## Comunicación en tiempo real

El frontend se conecta a `ws://<host>/api/chat/ws/{user_id}` y recibe mensajes con `type: "greeting" | "history" | "message"`. Ver [API.md](./API.md#chat---apichat) para el protocolo completo.
