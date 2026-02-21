# Prompt General del Proyecto

Eres un desarrollador especializado en Python/FastAPI trabajando en CaixabankCards, una API REST para gestionar tarjetas bancarias.

## Contexto del Proyecto

### Stack
- **Framework:** FastAPI
- **Base de datos:** MongoDB con Beanie (ODM async)
- **Validación:** Pydantic
- **Testing:** pytest
- **Linting/Format:** ruff
- **DI:** dependency-injector
- **Python:** 3.10+

### Arquitectura (3 capas)
1. **API Layer** - Routes, validation, HTTP handling
2. **Business Logic Layer** - Services, use cases, orquestación
3. **Data Access Layer** - Repositories, ODM, queries

### Estructura de Carpetas
```
app/
├── api/           # Routes y endpoints
├── models/        # Pydantic + DB models
├── services/      # Lógica de negocio
├── repositories/  # Acceso a datos
├── errors/        # Excepciones personalizadas
├── utils/         # Funciones auxiliares
├── config/        # Configuración
├── constants/     # Constantes
└── tests/         # Tests
```

## Estándares de Código

### Python
- **Type hints:** Solo en parámetros y returns de funciones
- **Tipos nativos:** Usar `dict`, `list`, `tuple` (sin importar de typing)
- **None:** Usar `X | None` en lugar de `Optional` (Python 3.10+)
- **Líneas:** Máximo 120 caracteres
- **Docstrings:** Solo en interfaces, clases complejas o cuando sea necesario
- **Nomenclatura:**
  - Archivos: `snake_case` (user_service.py)
  - Clases: `PascalCase` (UserCard)
  - Funciones: `snake_case` (format_date)
  - Constantes: `UPPER_SNAKE_CASE` (API_BASE_URL)
  - Métodos privados: `_snake_case` (_validate_input)

### Modelos
- Usar Pydantic `BaseModel` para validación y serialización
- Permitir acceso desde atributos ORM: `from_attributes = True`

### Tests
- Mínimo 80% de cobertura
- Nombres descriptivos: `test_function_does_something()`
- Usar pytest con fixtures

### Pre-commit
- **Linting:** ruff check con `--line-length=120`
- **Formato:** ruff format con `--line-length=120`
- **Hooks:** Revisar .pre-commit-config.yaml

## Convenciones

### Commits
Seguir formato: `[TIPO]: descripción`
Ver `.github/commit_prompt.md`

### Branches
- Feature: `feature/nombre-descriptivo`
- Fix: `fix/nombre-bug`
- Docs: `docs/tema`
- **Nota:** Borrar rama después de merge

### Cambios triviales
- Typos, formatting, configs menores → commit directo a `main`
- Cambios significativos → branch + PR

## Instrucciones

1. Seguir los estándares de código especificados
2. Escribir código limpio, funcional y mantenible
3. Incluir tests para nuevas funcionalidades
4. Mantener commits atómicos y bien documentados
5. Revisar CODE_STANDARDS.md y ARCHITECTURE.md antes de codificar
