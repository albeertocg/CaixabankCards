# Documentación de API

Base URL: `http://localhost:8000`

Docs interactivos (Swagger): `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`

## Auth — `/api/auth`

### `POST /api/auth/register`
Registra un nuevo usuario.

**Request body** (`UserCreate`):
```json
{
  "national_id": "12345678A",
  "first_name": "Ana",
  "last_name": "García",
  "email": "ana@ejemplo.com",
  "password": "Secreta123!",
  "phone": "+34600000000",
  "birth_date": "1990-01-01T00:00:00Z",
  "address": "Calle Mayor 1",
  "city": "Madrid",
  "postal_code": "28001",
  "province": "Madrid",
  "annual_income": 35000,
  "employment_status": "EMPLOYED",
  "education_level": "UNIVERSITY",
  "marital_status": "SINGLE",
  "num_dependents": 0,
  "customer_tenure_months": 24,
  "contracted_products": [],
  "average_balance": 5000,
  "credit_score": 720,
  "has_debts": false,
  "debt_amount": 0
}
```

**Respuesta** `200`: `{ "user": UserResponse }`
**Errores**: `409` email o DNI duplicado.

### `POST /api/auth/login`
Autentica al usuario y devuelve un JWT.

**Request body**:
```json
{ "email": "ana@ejemplo.com", "password": "Secreta123!" }
```

**Respuesta** `200`:
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "user": {
    "id": "<mongo_id>",
    "email": "ana@ejemplo.com",
    "first_name": "Ana",
    "last_name": "García"
  }
}
```

**Errores**: `401` credenciales incorrectas.

## Cards — `/api/cards`

### `GET /api/cards/catalog`
Devuelve el catálogo estático de tarjetas (15 tarjetas en 5 categorías).

**Respuesta** `200`: `list[Card]` — ver `app/agent/data/card_catalog.py`.

## Chat — `/api/chat`

### `POST /api/chat/session`
Crea una sesión de chat con saludo inicial.

**Query param**: `user_id: str`
**Respuesta** `200`: `{ "session_id": "...", "greeting": "..." }`

### `POST /api/chat/message`
Envía un mensaje al agente.

**Request body**:
```json
{
  "session_id": "<opcional, se crea si es null>",
  "user_id": "<mongo_id>",
  "message": "¿Qué tarjeta me recomiendas?"
}
```

**Respuesta** `200`: `{ "session_id": "...", "response": "..." }`

### `GET /api/chat/history/{session_id}`
Devuelve el historial de una sesión.

**Respuesta** `200`: `{ "session_id": "...", "messages": [...] }`

### `WebSocket /api/chat/ws/{user_id}`
Canal en tiempo real para el chat. Es el transporte usado por el frontend.

**Query param opcional**: `session_id` — si se pasa, se reenvía el histórico.

**Mensajes del servidor** (JSON):
- Saludo inicial:
  ```json
  { "type": "greeting", "session_id": "...", "response": "Hola..." }
  ```
- Replay de histórico (uno por mensaje, si `session_id` está en la query):
  ```json
  { "type": "history", "role": "user" | "assistant", "text": "..." }
  ```
- Respuestas a mensajes del usuario:
  ```json
  { "type": "message", "session_id": "...", "response": "..." }
  ```

**Mensajes del cliente**: texto plano (el cuerpo del mensaje del usuario).

## Códigos de error comunes

| Código | Significado |
|--------|-------------|
| `401` | Credenciales inválidas en login |
| `409` | Email o DNI ya registrado |
| `422` | Error de validación de Pydantic (body malformado) |
| `500` | Error interno en chat (p. ej. Gemini devolvió 503) |
