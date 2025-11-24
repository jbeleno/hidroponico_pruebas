# Sistema Hidropónico - Base de Datos y API

Sistema completo de gestión para un proyecto hidropónico, con base de datos PostgreSQL, API REST (FastAPI) y frontend web.

## 📋 Requisitos

- Docker
- Docker Compose

## 🚀 Inicio Rápido

### 1. Iniciar todos los servicios

```bash
docker-compose up -d
```

Esto iniciará:
- **PostgreSQL** en el puerto 5437
- **Python** (para scripts de base de datos)
- **Backend FastAPI** en el puerto 8000

### 2. Crear la base de datos desde JSON

```bash
docker-compose exec python python create_database.py
```

### 3. Ejecutar pruebas de la base de datos

```bash
docker-compose exec python python test_database.py
```

### 4. Ejecutar pruebas automatizadas

```bash
# Instalar dependencias de testing
pip install -r requirements.txt

# Ejecutar todas las pruebas
pytest tests/

# Solo pruebas unitarias
pytest tests/ -m unit

# Solo pruebas de integración (requiere Chrome)
pytest tests/ -m integration
```

### 5. Acceder a la aplicación

- **Frontend**: Abre `frontend/index.html` en tu navegador
- **API Backend**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5437

## 📁 Estructura del Proyecto

```
.
├── backend/
│   ├── __init__.py
│   ├── models.py          # Modelos SQLAlchemy
│   ├── schemas.py         # Esquemas Pydantic
│   ├── database.py        # Configuración de BD
│   └── main.py            # API FastAPI
├── frontend/
│   ├── index.html         # Interfaz web
│   ├── styles.css         # Estilos
│   └── app.js             # Lógica JavaScript
├── tests/                 # Pruebas automatizadas
│   ├── conftest.py       # Configuración pytest
│   ├── test_unit_*.py    # Pruebas unitarias
│   └── test_integration_*.py  # Pruebas de integración
├── JSON.json              # Modelo de base de datos
├── create_database.py     # Script de creación de BD
├── test_database.py       # Script de pruebas
├── docker-compose.yml     # Configuración Docker
├── Dockerfile             # Imagen Docker
├── requirements.txt       # Dependencias Python
└── README.md             # Este archivo
```

## 🔧 API Endpoints

La API incluye endpoints CRUD para todas las entidades:

- `/api/empresas`
- `/api/personas`
- `/api/sedes`
- `/api/bloques`
- `/api/tipos-espacio`
- `/api/espacios`
- `/api/tipos-estructura`
- `/api/estructuras`
- `/api/usuarios`
- `/api/roles`
- `/api/usuarios-roles`
- `/api/metodos-acceso`
- `/api/accesos-espacio`
- `/api/tipos-cultivo`
- `/api/cultivos`
- `/api/variedades-cultivo`
- `/api/fases-produccion`
- `/api/cultivos-fases`
- `/api/nutrientes`
- `/api/fases-nutriente`

Cada endpoint soporta:
- `GET /api/{entidad}` - Listar todos
- `GET /api/{entidad}/{id}` - Obtener uno
- `POST /api/{entidad}` - Crear
- `PUT /api/{entidad}/{id}` - Actualizar
- `DELETE /api/{entidad}/{id}` - Eliminar

## 🎨 Frontend

El frontend es una aplicación web simple (HTML/CSS/JS) que permite:
- Ver todas las entidades en tabs
- Listar registros en tablas
- Crear nuevos registros
- Editar registros existentes
- Eliminar registros

**Nota**: Abre `frontend/index.html` directamente en tu navegador (no necesita servidor).

## 🛠️ Comandos Útiles

### Ver logs
```bash
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Reiniciar servicios
```bash
docker-compose restart backend
```

### Detener todo
```bash
docker-compose down
```

### Eliminar todo (incluyendo volúmenes)
```bash
docker-compose down -v
```

### Conectarse a PostgreSQL
```bash
docker-compose exec postgres psql -U www-admin -d hidroponico
```

### Acceder al contenedor backend
```bash
docker-compose exec backend bash
```

## 📊 Modelo de Datos

El modelo incluye 20 entidades organizadas en:

- **Organización**: empresa, sede, bloque, espacio
- **Usuarios**: persona, usuario, rol, usuario_rol, metodo_acceso, acceso_espacio
- **Infraestructura**: tipo_espacio, tipo_estructura, estructura
- **Cultivos**: tipo_cultivo, cultivo, variedad_cultivo
- **Producción**: fase_produccion, cultivo_fase
- **Nutrición**: nutriente, fase_nutriente

## 🔐 Configuración

Las variables de entorno se configuran en `docker-compose.yml`:

- `DB_HOST`: postgres (dentro de Docker) o localhost (fuera)
- `DB_PORT`: 5432
- `DB_NAME`: hidroponico
- `DB_USER`: www-admin
- `DB_PASSWORD`: hello!

## 📝 Notas

- El frontend se abre directamente desde el archivo HTML (no necesita servidor)
- La API está disponible en http://localhost:8000
- La documentación interactiva de la API está en http://localhost:8000/docs
- Los datos de PostgreSQL se persisten en un volumen de Docker

## 🐛 Solución de Problemas

### Error: "No se puede conectar a la API"
- Verifica que el backend esté corriendo: `docker-compose ps`
- Revisa los logs: `docker-compose logs backend`
- Asegúrate de que el puerto 8000 no esté ocupado

### Error: "CORS" en el frontend
- Si abres el HTML desde `file://`, puede haber problemas de CORS
- Considera usar un servidor local simple o configurar CORS en FastAPI

### Error al crear/editar registros
- Verifica que los campos requeridos estén completos
- Revisa las foreign keys (deben existir los registros relacionados)

## 🧪 Pruebas Automatizadas

El proyecto incluye pruebas automatizadas usando pytest y Selenium:

### Pruebas Unitarias

- **Modelos** (`test_unit_models.py`): Pruebas para los modelos de SQLAlchemy
- **Schemas** (`test_unit_schemas.py`): Pruebas para los esquemas de Pydantic
- **API** (`test_unit_api.py`): Pruebas para los endpoints de FastAPI

### Pruebas de Integración

- **Selenium** (`test_integration_selenium.py`): Pruebas end-to-end del frontend

### Ejecutar Pruebas

```bash
# Todas las pruebas
pytest tests/

# Solo pruebas unitarias
pytest tests/ -m unit

# Solo pruebas de integración
pytest tests/ -m integration

# Con cobertura
pytest tests/ --cov=backend --cov-report=html
```

Para más información, consulta `tests/README.md`.

## 📄 Licencia

Este proyecto es para fines educativos y de prueba.
