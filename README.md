# CaixabankCards

## 1. Problema y solución

CaixaBank detectó una tasa de abandono del 90 % en su proceso de alta de tarjetas de crédito online. El flujo tradicional resulta tedioso, genérico y poco orientado al cliente, lo que provoca que la mayoría de usuarios abandone antes de completar la contratación.

El objetivo del proyecto es reducir esa tasa al 70 % mediante un rediseño completo del servicio, centrado en dos ejes:

- **Asistente virtual conversacional** — Un agente de IA guía al usuario a lo largo del proceso de contratación en lenguaje natural, resuelve sus dudas en tiempo real y elimina la fricción de los formularios tradicionales.
- **Personalización basada en el perfil del cliente** — El sistema analiza la información disponible del usuario (perfil financiero, historial de transacciones y categorías de gasto dominantes) para recomendar la tarjeta más adecuada de forma individualizada, presentando beneficios, comisiones y requisitos concretos.

---

## 2. Tecnologías utilizadas

### Backend

| Tecnología | Uso |
|---|---|
| **FastAPI** | Framework principal de la API REST. Proporciona validación automática con Pydantic, documentación OpenAPI y soporte nativo async. |
| **Google ADK** | Orquestador del agente conversacional. Gestiona el ciclo de vida de la sesión, el flujo de herramientas (tools) y la comunicación con el modelo LLM. |
| **Gemini 2.5 Flash** | Modelo LLM que impulsa el asistente virtual. Se eligió por su equilibrio entre velocidad, coste,  capacidad de razonamiento en castellano y su versión gratuita. |
| **MongoDB Atlas** | Base de datos principal. Almacena los perfiles de usuario, transacciones y el historial de conversaciones. |
| **ChromaDB** | Base de datos vectorial persistente en disco. Almacena los embeddings de la documentación de tarjetas y permite búsqueda semántica en el pipeline RAG. |
| **Distancia de Gower** *(gower-exp)* | Métrica de similitud para variables heterogéneas (numéricas + categóricas + booleanas). Se usa para encontrar las tarjetas más similares al perfil ideal del usuario, combinando atributos como cuota anual, cashback, límite de crédito, seguros o tipo de tarjeta en una única puntuación de similitud (0 = idéntica, 1 = muy diferente). |
| **JWT + bcrypt** | Autenticación stateless con tokens y almacenamiento seguro de contraseñas. |

### Frontend

| Tecnología | Uso |
|---|---|
| **Next.js 16** | Framework React con SSR/SSG para la interfaz web del asistente. |
| **Tailwind CSS 4** | Estilos utilitarios para la UI. |
| **react-markdown** | Renderizado del markdown que devuelve el agente en la interfaz del chat. |

---

## 3. RAG y embeddings

El sistema implementa un pipeline RAG para garantizar que el agente responde con información real y actualizada sobre las tarjetas, sin alucinaciones.

### Fuente de conocimiento

La base de conocimiento son 5 archivos Markdown (uno por categoría de tarjeta: viajes, compras online, supermercado, restauración/ocio y clásicas) que documentan en detalle las 15 tarjetas disponibles: beneficios, comisiones, requisitos, comparativas y preguntas frecuentes.

### Chunking

Los documentos se dividen por cabeceras de nivel 2 (`## `). Cada *chunk* recibe metadatos estructurados: nombre de tarjeta, categoría, *tier*, fichero de origen y tipo de fragmento (`card_detail`, `comparison`, `faq`, `guide`).

### Modelo de embeddings

Se usa el modelo **`gemini-embedding-001`** de Google GenAI para vectorizar tanto los chunks de documentación (en el proceso de indexación) como las consultas del usuario en tiempo real.

### Almacenamiento y recuperación

Los vectores persisten en **ChromaDB** (colección `caixabank_cards`) con distancia coseno. La recuperación combina dos estrategias:

1. **Búsqueda exacta por metadatos** (`card_name`) — para recuperar la ficha completa de una tarjeta conocida.
2. **Búsqueda semántica** — para consultas en lenguaje natural donde no se conoce el nombre exacto.

### Indexación al arranque

Al iniciar el servidor, el `lifespan` de FastAPI ejecuta `ensure_indexed()` de forma no bloqueante: comprueba si la colección ya tiene documentos y, si no, vectoriza e indexa todos los chunks automáticamente.

---

## 4. Guardrails

El sistema implementa 3 capas de protección independientes para prevenir inyección de prompts, consultas fuera de ámbito y contenido dañino.

### Capa 1 — Detección de inyección de prompts por expresiones regulares

El módulo `sanitizer.py` aplica más de 10 patrones regex sobre cada mensaje entrante antes de procesarlo:

- Comandos de redirección: *"ignora las instrucciones"*, *"olvida"*, *"ignore"*, *"forget"*
- Suplantación de rol: *"eres"*, *"actúa como"*, *"you are"*, *"act as"*
- Inyecciones de sistema: `[INST]`, `[SYS]`, `<|system|>`
- Técnicas de jailbreak: *"jailbreak"*, *"DAN"*, *"do anything now"*, *"developer mode"*

Si se detecta un patrón, el texto se sanea eliminando las coincidencias antes de pasar al siguiente paso.

### Capa 2 — Guardrail semántico basado en RAG

`GuardrailService` vectoriza el mensaje del usuario con `gemini-embedding-001` y lo compara semánticamente contra la base de conocimiento de tarjetas en ChromaDB. Si la distancia coseno al chunk más cercano supera un umbral (0,35 para el primer mensaje, 0,42 para los siguientes), el sistema considera la consulta fuera de ámbito y devuelve una respuesta predefinida redirigiendo al usuario hacia la ayuda sobre tarjetas, sin invocar al LLM.

### Capa 3 — Filtros de seguridad de Gemini

Todas las llamadas al modelo LLM llevan configurados los filtros de seguridad de Google con el nivel más estricto (`BLOCK_LOW_AND_ABOVE`) para las cuatro categorías de daño: `HATE_SPEECH`, `HARASSMENT`, `SEXUALLY_EXPLICIT` y `DANGEROUS_CONTENT`. Si Gemini bloquea una respuesta, el servicio de chat detecta la razón de finalización (`SAFETY`, `PROHIBITED_CONTENT`, `SPII`, `BLOCKLIST`) y devuelve un mensaje de error controlado.

Además, el propio **prompt de sistema del agente** incluye instrucciones explícitas para que nunca revele sus instrucciones internas, el nombre de las herramientas ni detalles de implementación, e ignore cualquier intento de cambiar su comportamiento o asumir otro rol.

---

## 5. Guía de despliegue

### Requisitos previos

- Python 3.12+
- Node.js 20+
- Cuenta en MongoDB Atlas con una base de datos `caixabank_cards`
- Google API Key con acceso a Gemini y `gemini-embedding-001`

### Configuración del entorno

Copia el fichero de ejemplo y rellena las variables:

```bash
cp .env.example .env
```

```env
MONGO_URI=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/caixabank_cards
MONGO_DB_NAME=caixabank_cards
JWT_SECRET_KEY=<clave_secreta>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
GOOGLE_API_KEY=<tu_google_api_key>
CORS_ORIGINS=["http://localhost:3000"]
```

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
fastapi dev app/main.py
```

La API queda disponible en `http://localhost:8000`. La documentación interactiva en `http://localhost:8000/docs`.

Al arrancar, el sistema indexa automáticamente la documentación de tarjetas en ChromaDB si la colección está vacía.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

La aplicación queda disponible en `http://localhost:3000`.

### Docker (solo backend)

```bash
cd backend
docker build -t caixabank-backend .
docker run -p 8000:8000 --env-file ../.env caixabank-backend
```

### Tests

```bash
cd backend
pytest app/tests/ -v
```