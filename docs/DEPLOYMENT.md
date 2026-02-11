# Guía de Deployment

## Ambientes

| Ambiente | URL | Trigger |
|----------|-----|---------|
| Development | localhost:5000 | Local |
| Staging | https://staging.caixabankcards.com | Push a `develop` |
| Production | https://caixabankcards.com | Release tag |

## Pre-deployment Checklist

- [ ] Tests pasando (`pytest`)
- [ ] Linting OK (`ruff check .`)
- [ ] Código formateado (`ruff format .`)
- [ ] Changelog actualizado
- [ ] Versión bumpeada en `pyproject.toml`

## Deploy a Staging

```bash
git push origin develop
```

## Deploy a Production

```bash
# Crear release tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

## Variables de Entorno

### Staging (.env.staging)
```
API_URL=https://api-staging.caixabankcards.com
LOG_LEVEL=DEBUG
```

### Production (.env.production)
```
API_URL=https://api.caixabankcards.com
LOG_LEVEL=ERROR
```

## Rollback

```bash
git revert <commit-hash>
git push origin main
```

## Monitoreo Post-Deploy

1. Verificar health check: `/api/health`
2. Revisar logs de la aplicación
3. Monitorear errores
