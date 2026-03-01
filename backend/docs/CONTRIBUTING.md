# Guía de Contribución

## Nuestros Estándares

### Commits

**Formato:**
```
[TIPO]: descripción breve en minúsculas

feat: agregar nueva funcionalidad
fix: corregir bug
docs: actualizar documentación
style: cambios de formato/linting
refactor: reorganizar código
test: agregar/actualizar tests
```

**Reglas:**
- Mensaje en presente imperativo
- Primera línea máximo 50 caracteres
- Si es necesario, agregar descripción detallada después de línea en blanco

### Branches

Formato: `tipo/descripción-breve`

```
feature/user-authentication
fix/card-validation-bug
docs/api-documentation
```

## Flujo de Trabajo

**Por defecto:**
1. **Crear branch** desde `main`
2. **Hacer commits** pequeños y significativos
3. **Push** y crear Pull Request
4. **Esperar revisión** de al menos 0 miembros del equipo xD
5. **Mergear** en `main` cuando esté aprobado

**Excepción - Cambios triviales directos a main:**
- En estos casos: commit directo a `main` con mensaje claro

**Después del merge:**
- Borrar la rama: `git branch -d nombre-rama`
- Borrar rama remota: `git push origin --delete nombre-rama`


## Pre-commit

Usamos pre-commit con **ruff** para linting y formatting automático.

```bash
# Instalar y configurar
pip install pre-commit
pre-commit install

# Ejecutar manualmente (opcional)
pre-commit run --all-files
```

Los checks corren automáticamente antes de cada commit. Si falla, soluciona y reintenta.
