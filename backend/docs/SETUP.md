# Guía de Instalación y Setup

## Requisitos Previos

- **Python:** 3.12+
- **MongoDB:** local o Atlas
- **Google API key** (para el agente Gemini)
- **Node.js 18+** (solo si también vas a correr el frontend)

## Pasos de Instalación (Backend)

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd CaixabankCards
```

### 2. Crear y activar virtual environment

Desde la raíz del repo:

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
cd backend
pip install -r requirements.txt
# o, equivalente:
make install
```

### 4. Configurar variables de entorno

Copia `.env.example` a `.env` dentro de `backend/`:

```bash
cp .env.example .env
```

Variables reales esperadas (ver `backend/.env.example`):

```env
# MongoDB
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/caixabank_cards
MONGO_DB_NAME=caixabank_cards

# JWT
JWT_SECRET_KEY=tu_clave_secreta_aqui
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# Google (agente Gemini)
GOOGLE_API_KEY=tu_api_key_aqui

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```

### 5. (Opcional) Sembrar usuarios de prueba

Para disponer de 5 perfiles de usuario con transacciones:

```bash
python -m scripts.seed_test_users
```

Todos comparten la contraseña `Test1234!`. Ejemplos:
- `test.viajero@ejemplo.com`
- `test.shopper@ejemplo.com`
- `test.foodie@ejemplo.com`
- `test.jubilado@ejemplo.com`
- `test.estudiante@ejemplo.com`

### 6. Ejecutar la aplicación

```bash
fastapi dev app/main.py
# o:
make dev
```

- API: **http://localhost:8000**
- Swagger: **http://localhost:8000/docs**
- ReDoc: **http://localhost:8000/redoc**

### 7. (Opcional) Lanzar la ADK Web UI

```bash
make adk
```
UI del agente en `http://localhost:8765`.

## Frontend

```bash
cd frontend
npm install
npm run dev
```
Disponible en **http://localhost:3000**.

## Verificar Instalación

```bash
python --version      # 3.12+
pip list              # comprobar fastapi, motor, google-adk, chromadb...
```

## Siguiente Paso

Consulta [CONTRIBUTING.md](./CONTRIBUTING.md) para empezar a contribuir.
