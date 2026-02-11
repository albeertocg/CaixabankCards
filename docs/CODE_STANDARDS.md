# Estándares de Código

## Nomenclatura

| Tipo | Formato | Ejemplo |
|------|---------|---------|
| Archivos | snake_case | `user_service.py` |
| Clases | PascalCase | `UserCard` |
| Funciones | snake_case | `format_date()` |
| Constantes | UPPER_SNAKE_CASE | `API_BASE_URL` |
| Variables | snake_case | `is_loading` |
| Métodos privados | _snake_case | `_validate_input()` |

## Python Type Hints

- Type hints solo en parámetros y return types de funciones
- Usar tipos nativos: `dict`, `list`, `tuple`, `set` (no importar de `typing`)
- Usar `X | None` en lugar de `Optional` (Python 3.10+)
- No saturar: si una variable hereda el tipo del return de una función, no duplicar el type hint

```python
# ✅ Bien
def get_user(user_id: str) -> User:
    pass

user = get_user('123')  # Sin type hint, ya lo tiene del return

def process_data(items: list[str]) -> dict[str, int]:
    result = {}  # Sin type hint, claro por contexto
    return result

# ❌ Evitar (redundante)
user: User = get_user('123')  
result: dict[str, int] = {}
```

## Modelos de Datos (Pydantic)

Usar Pydantic `BaseModel` para definir modelos (ORM y validación):

```python
from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    email: str
    is_active: bool = True

class Card(BaseModel):
    card_number: str
    holder_name: str
    expiry_date: str
```

## Funciones

- Máximo 20 líneas
- Una responsabilidad única
- Docstring solo en interfaces, clases complejas o cuando sea necesario

```python
def validate_email(email: str) -> bool:
    return '@' in email and '.' in email.split('@')[1]

class UserRepository:
    """Gestiona la persistencia de usuarios en base de datos."""
    
    def get_by_id(self, user_id: str) -> dict[str, str] | None:
        """Obtiene un usuario por su ID."""
        pass
```

## Imports

```python
# ✅ Organizar: stdlib, third-party, local
import os
from datetime import datetime

import requests

from app.utils.date import format_date
from app.config import API_URL
```

## Errores y Logging

```python
import logging

logger = logging.getLogger(__name__)

try:
    user_data = fetch_user(user_id)
except Exception as error:
    logger.error(f'Error fetching user {user_id}: {error}')
    raise ValueError('No se pudo cargar el usuario')
```