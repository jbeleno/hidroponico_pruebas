# Sistema Hidropónico — Backend + suite de pruebas automatizadas

[![Python](https://img.shields.io/badge/Python-3.11-3670A0?style=flat-square&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat-square)](https://www.sqlalchemy.org/)
[![Pytest](https://img.shields.io/badge/Pytest-7.4-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://pytest.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15-43B02A?style=flat-square&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)

API REST y frontend para gestión de un sistema hidropónico, **con foco en la suite de pruebas automatizadas**: unit tests sobre modelos SQLAlchemy, schemas Pydantic y endpoints FastAPI; integration tests end-to-end con Selenium; cobertura con `pytest-cov` y reportes HTML/TXT para revisión.

> Proyecto académico de la materia de **Pruebas de Software** en la Universidad Surcolombiana (USCO). El énfasis no está en la lógica de hidroponía, sino en la **estrategia de testing**: cómo cubrir un sistema fullstack con pruebas reproducibles, dockerizadas y reportadas.

---

## Highlights de testing

- **Tres niveles de pruebas unitarias**, una por capa: `models` (ORM), `schemas` (validación Pydantic), `api` (endpoints FastAPI con `TestClient`).
- **Integración end-to-end con Selenium** sobre el frontend HTML/JS, cubriendo el flujo real usuario → API → base de datos.
- **Cobertura con `pytest-cov`** apuntada al paquete `backend/`.
- **Reportes en dos formatos** (`pytest-html` + dump TXT) para entrega y revisión académica.
- **Marcadores `pytest`** (`-m unit`, `-m integration`) para correr subconjuntos según el contexto (CI rápido vs validación completa).
- **Stack reproducible** con Docker Compose: PostgreSQL + Python + Backend en contenedores con health checks.

## Tech stack

| Capa | Tecnología |
|---|---|
| API | FastAPI 0.104 + Uvicorn |
| ORM | SQLAlchemy 2.0 |
| Validación | Pydantic 2.5 |
| Base de datos | PostgreSQL 15 (Alpine) |
| Frontend | HTML / CSS / JavaScript (vanilla) |
| Tests unit | pytest, pytest-asyncio, httpx |
| Tests integración | Selenium 4 + WebDriver Manager |
| Cobertura | pytest-cov |
| Reportes | pytest-html |
| Contenerización | Docker + Docker Compose |

---

## Arquitectura

```
┌──────────────────────────────────────────────┐
│  Frontend (HTML/JS)                          │
│  - Llama a /api/* del backend                │
└──────────────────────────────────────────────┘
                  ↓ HTTP (CORS *)
┌──────────────────────────────────────────────┐
│  Backend FastAPI                             │
│  - Endpoints CRUD                            │
│  - Schemas Pydantic                          │
│  - SQLAlchemy ORM                            │
└──────────────────────────────────────────────┘
                  ↓ SQL
┌──────────────────────────────────────────────┐
│  PostgreSQL 15                               │
│  - Schema cargado desde JSON.json            │
│  - init.sql inicializa estructura            │
└──────────────────────────────────────────────┘
```

### Modelo de datos

Entidades principales: `Empresa`, `Sede`, `Persona`, `Usuario`, y entidades del dominio hidropónico cargadas desde `JSON.json` mediante `create_database.py`.

---

## Quick start

### Requisitos

- Docker + Docker Compose
- Python 3.11+ (solo si vas a correr pruebas fuera de Docker)
- Chrome (para los tests de integración Selenium)

### 1. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales — DB_PASSWORD es obligatorio
```

### 2. Levantar la stack

```bash
docker-compose up -d
```

Esto inicia tres contenedores:

| Servicio | Container | Puerto host | Descripción |
|---|---|---|---|
| `postgres` | `hidroponico_db` | 5437 | PostgreSQL 15 con `init.sql` y healthcheck |
| `python` | `hidroponico_python` | — | Contenedor para scripts (creación BD, tests) |
| `backend` | `hidroponico_backend` | 8000 | API FastAPI con hot reload |

### 3. Cargar la base de datos desde JSON

```bash
docker-compose exec python python create_database.py
```

### 4. Verificar

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Frontend: abrir `frontend/index.html` en el navegador

---

## Testing

### Marcadores

```bash
# Todas las pruebas
pytest tests/

# Solo unit tests (rápido, sin browser)
pytest tests/ -m unit

# Solo integration tests (requiere Chrome corriendo)
pytest tests/ -m integration

# Cobertura sobre el paquete backend/
pytest tests/ --cov=backend --cov-report=html
# Reporte queda en htmlcov/index.html
```

### Reportes con `run_tests_with_txt.py`

```bash
python run_tests_with_txt.py
```

Genera dos reportes en `resultados/`:

- `report_all_tests.html` — Reporte interactivo con filtros por estado y logs por test (vía `pytest-html`).
- `report_all_tests.txt` — Salida completa de pytest (tracebacks, resúmenes, warnings).

### Estructura de pruebas

```
tests/
├── conftest.py                   # Fixtures: client, sample data, db setup
├── pytest.ini                    # Markers, paths
├── test_unit_models.py           # SQLAlchemy: relaciones, defaults, constraints
├── test_unit_schemas.py          # Pydantic: validación, serialización
├── test_unit_api.py              # FastAPI: endpoints CRUD por entidad
└── test_integration_flow.py      # Selenium: flujo usuario → UI → API → DB
```

### Por qué tres archivos de unit tests

Separar por **capa** (no por entidad) permite identificar exactamente dónde está el fallo cuando algo se rompe:

- Falla en `test_unit_models.py` → problema de schema BD o relaciones SQLAlchemy.
- Falla en `test_unit_schemas.py` → problema de validación Pydantic.
- Falla en `test_unit_api.py` → problema de routing, status codes o serialización.

Esto reduce el tiempo de diagnóstico vs tener un archivo gigante por entidad mezclando capas.

---

## API endpoints

API expuesta bajo `/api/`:

- `GET /api/empresas` · `POST /api/empresas` · `GET /api/empresas/{id}` · etc.
- Misma forma CRUD para `sedes`, `personas`, `usuarios` y demás entidades.

Documentación interactiva auto-generada en http://localhost:8000/docs (Swagger UI).

---

## Estructura del proyecto

```
hidroponico_pruebas/
├── backend/
│   ├── __init__.py
│   ├── main.py            # App FastAPI, routes, CORS
│   ├── models.py          # SQLAlchemy ORM
│   ├── schemas.py         # Pydantic schemas
│   └── database.py        # Engine, session, get_db dependency
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/                 # Suite de pruebas (ver sección Testing)
├── resultados/            # Reportes generados (HTML/TXT)
├── assets/                # Recursos para presentación
├── JSON.json              # Definición de schema y datos iniciales
├── init.sql               # Inicialización mínima de BD
├── create_database.py     # Script: lee JSON.json y crea/popula tablas
├── test_database.py       # Script de smoke test contra la BD
├── run_tests_with_txt.py  # Runner de pruebas con doble reporte
├── docker-compose.yml     # PostgreSQL + Python + Backend
├── Dockerfile
├── .env.example           # Plantilla de variables de entorno
├── requirements.txt
├── presentation.html      # Slides de presentación del proyecto
├── GUIA_PRESENTACION.md   # Guion de la presentación académica
└── PRUEBAS.md             # Documentación detallada de la estrategia de pruebas
```

---

## Troubleshooting

### "No se puede conectar a la API"
- `docker-compose ps` para ver el estado de los contenedores.
- `docker-compose logs backend` para revisar errores.
- Verificar que el puerto 8000 (o el definido en `BACKEND_PORT`) esté libre.

### Error de CORS en el frontend
- Si abres `frontend/index.html` con `file://`, algunos navegadores bloquean fetch a `localhost:8000`. Servir el frontend con un server local (`python -m http.server`) o configurar CORS más estricto en producción.

### Selenium no encuentra el navegador
- Asegurarse de tener Chrome instalado.
- `webdriver-manager` debería descargar el driver automáticamente; si no, definir `WDM_LOCAL=1`.

### Las tablas no se crean
- Verificar que el contenedor `postgres` esté `healthy`: `docker-compose ps`.
- Ejecutar manualmente `docker-compose exec python python create_database.py`.

---

## Mejoras pendientes

- Tests de carga sobre la API con `locust` o `k6`.
- CI con GitHub Actions corriendo unit tests en cada push (los integration con Selenium requieren runner con Chrome).
- Mocks de DB para unit tests de modelos (ahora dependen del contenedor real).
- CORS restringido a orígenes específicos en producción (actualmente `allow_origins=["*"]`).

---

## Licencia

Proyecto académico — Universidad Surcolombiana (USCO).

---

**Materia:** Pruebas de Software · **Stack:** FastAPI · PostgreSQL · pytest · Selenium · Docker
