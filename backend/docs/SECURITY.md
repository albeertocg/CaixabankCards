# Estándares de Seguridad

## Autenticación

### JWT (JSON Web Tokens)
- Implementado con `python-jose[cryptography]`.
- Emisión en `POST /api/auth/login` (ver [auth_service.py](../app/services/auth_service.py)).
- Payload actual:
  ```json
  { "sub": "<user_id>", "email": "<email>", "exp": <timestamp> }
  ```
- Configurable vía entorno:
  - `JWT_SECRET_KEY` — clave de firma HMAC. **No commitear**.
  - `JWT_ALGORITHM` — por defecto `HS256`.
  - `JWT_EXPIRATION_MINUTES` — por defecto `60`.

> **Nota**: hoy la API no valida el JWT en los endpoints de `cards` ni `chat`. Añadir un `Depends` que verifique el token es una mejora pendiente antes de producción.

### Hashing de contraseñas
- Algoritmo: **bcrypt** (`passlib[bcrypt]` / librería `bcrypt`).
- Hash generado con `bcrypt.gensalt()` por usuario.
- Validación con `bcrypt.checkpw` en `auth_service._verify_password`.
- Política actual: mínimo 6 caracteres (`UserCreate.password: Field(min_length=6)`).

## Validación de entrada

- Todos los bodies se validan con Pydantic v2 (`app/schemas/`, `app/dtos/`).
- `EmailStr` fuerza formato de correo.
- Errores de validación devuelven `422` con detalle de Pydantic.

## CORS

- Configurado vía `CORS_ORIGINS` (lista JSON en `.env`).
- Por defecto en desarrollo: `["http://localhost:3000"]`.
- En producción se debe restringir a los dominios del frontend real.

## Gestión de secretos

- `.env` no debe commitearse (está en `.gitignore`).
- Secretos reales: `MONGO_URI`, `JWT_SECRET_KEY`, `GOOGLE_API_KEY`.
- En un despliegue real, usar el gestor de secretos de la plataforma (p. ej. AWS Secrets Manager, GCP Secret Manager, etc.).

## Errores conocidos / TODO

- [ ] Proteger `/api/cards/*` y `/api/chat/*` con dependencia de validación JWT.
- [ ] Validar `user_id` del WebSocket contra el `sub` del JWT para evitar suplantaciones.
- [ ] Añadir rate limiting en endpoints públicos (`/api/auth/login`, WS de chat).
- [ ] Política de contraseñas más estricta (longitud, complejidad, rotación).
- [ ] Registrar y alertar intentos fallidos de login.

## Dependencias de seguridad

Revisar periódicamente con:

```bash
pip list --outdated
# y, si se añade al proyecto:
pip-audit
```
