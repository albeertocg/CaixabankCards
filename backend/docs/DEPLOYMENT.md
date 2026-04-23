# Guía de Deployment

> A fecha de hoy el proyecto se ejecuta **solo en local**. Este documento describe el flujo previsto; los entornos de staging/producción todavía no están provisionados.

## Ambientes (previstos)

| Ambiente     | URL                                  | Trigger          |
|--------------|--------------------------------------|------------------|
| Development  | http://localhost:8000                | Local (`make dev`) |
| Staging      | *pendiente de provisión*             | Push a `develop` |
| Production   | *pendiente de provisión*             | Release tag      |

## Pre-deployment Checklist

- [ ] Tests pasando (`make test`)
- [ ] Linting OK (`make lint`)
- [ ] Código formateado (`make format`)
- [ ] Variables de entorno del entorno destino revisadas
- [ ] Changelog actualizado (si aplica)

## Deploy local (desarrollo)

```bash
cd backend
make dev        # fastapi dev app/main.py
```

Frontend:

```bash
cd frontend
npm run dev
```

## Deploy a Staging / Production

Pendiente de definir pipeline. Cuando exista:

```bash
# Staging
git push origin develop

# Production
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

## Variables de Entorno

Se definen en un `.env` por entorno (nunca commiteado). Ver [SETUP.md](./SETUP.md) para la lista real:

- `MONGO_URI`, `MONGO_DB_NAME`
- `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRATION_MINUTES`
- `GOOGLE_API_KEY`
- `CORS_ORIGINS`

## Rollback

```bash
git revert <commit-hash>
git push origin main
```

## Monitoreo Post-Deploy

1. Revisar logs de la aplicación (`uvicorn` / FastAPI).
2. Verificar que los endpoints principales responden:
   - `POST /api/auth/login`
   - `GET /api/cards/catalog`
   - `WS /api/chat/ws/{user_id}`
3. Confirmar que el WebSocket del chat se conecta y que Gemini responde sin `503 UNAVAILABLE`.

> Nota: actualmente no hay endpoint `/api/health`. Si se requiere para health checks externos, añadir uno en `app/routes/` y documentarlo en [API.md](./API.md).
