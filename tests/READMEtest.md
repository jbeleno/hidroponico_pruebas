# Pruebas del Sistema Hidropónico

Este directorio contiene todas las pruebas automatizadas del proyecto.

## Estructura

- `conftest.py`: Configuración y fixtures compartidas para pytest
- `pytest.ini`: Configuración de pytest
- `test_unit_*.py`: Pruebas unitarias
- `test_integration_*.py`: Pruebas de integración

## Tipos de Pruebas

### Pruebas Unitarias

- `test_unit_models.py`: Pruebas para los modelos de SQLAlchemy
- `test_unit_schemas.py`: Pruebas para los esquemas de Pydantic
- `test_unit_api.py`: Pruebas para los endpoints de la API FastAPI

### Pruebas de Integración

- `test_integration_selenium.py`: Pruebas end-to-end del frontend usando Selenium

## Ejecutar las Pruebas

### Todas las pruebas

```bash
pytest tests/
```

### Solo pruebas unitarias

```bash
pytest tests/ -m unit
```

### Solo pruebas de integración

```bash
pytest tests/ -m integration
```

### Pruebas específicas

```bash
pytest tests/test_unit_api.py
pytest tests/test_integration_selenium.py
```

### Con cobertura

```bash
pytest tests/ --cov=backend --cov-report=html
```

## Requisitos

- Docker y Docker Compose deben estar corriendo
- El backend debe estar disponible en `http://localhost:8000`
- Chrome/Chromium debe estar instalado para las pruebas de Selenium
- Las dependencias deben estar instaladas: `pip install -r requirements.txt`

## Notas

- Las pruebas de Selenium requieren que el frontend esté accesible
- Las pruebas unitarias de API usan una base de datos de prueba
- Asegúrate de que la base de datos esté inicializada antes de ejecutar las pruebas

