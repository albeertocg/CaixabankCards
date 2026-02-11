# Guía de Testing

## Tests con IA

Los tests se generan y mantienen con IA. Usamos **pytest** como framework de testing.

## Framework

- **Testing:** pytest
- **Generación:** Con asistencia de IA

## Estructura

```
src/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
```

## Ejecutar Tests

```bash
pytest                    # Todos los tests
pytest --watch           # Modo observación
pytest --cov            # Con cobertura
pytest -v               # Verbose
```

## Convenciones

- Nombre de archivos: `test_*.py`
- Nombre de funciones: `test_*`
- Fixtures en `conftest.py`

## Coverage

- **Mínimo:** 80%
- **Objetivo:** 90%
- **Crítico:** 100% en servicios y utilidades
