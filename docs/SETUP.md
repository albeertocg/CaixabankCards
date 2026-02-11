# Guía de Instalación y Setup

## Requisitos Previos

- **Python:** 3.12+
- **MongoDB:** Local o Atlas (cloud)
- **Virtual Environment:** venv

## Pasos de Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/yourusername/CaixabankCards.git
cd CaixabankCards
```

### 2. Crear y activar virtual environment

```bash
# Crear venv
python3 -m venv venv

# Activar venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar `.env.example` a `.env`:

```bash
cp .env.example .env
```

Completar las variables necesarias:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017/caixabank_cards

...
```

### 5. Ejecutar la aplicación

```bash
fastapi dev app/main
```

La API estará disponible en: **http://localhost:8000**

Docs interactivos: **http://localhost:8000/docs**

## Verificar Instalación

```bash
# Debe mostrar Python 3.12.x
python --version

# Debe mostrar pip desde venv/
pip --version

# Ver paquetes instalados
pip list
```

## Siguiente Paso

Consulta [CONTRIBUTING.md](./CONTRIBUTING.md) para empezar a contribuir.
