"""
Configuración y fixtures compartidas para pytest
"""
import pytest
import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from backend.database import get_db
from backend.models import Base
from backend.main import app

# Configuración de base de datos de prueba
TEST_DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5437'),  # Puerto 5437 para Docker
    'database': os.getenv('DB_NAME', 'hidroponico'),
    'user': os.getenv('DB_USER', 'www-admin'),
    'password': os.getenv('DB_PASSWORD', 'hello!')
}

TEST_DATABASE_URL = (
    f"postgresql://{TEST_DB_CONFIG['user']}:{TEST_DB_CONFIG['password']}"
    f"@{TEST_DB_CONFIG['host']}:{TEST_DB_CONFIG['port']}/{TEST_DB_CONFIG['database']}"
)


@pytest.fixture(scope="function")
def db_session():
    """Fixture para crear una sesión de base de datos de prueba"""
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Fixture para crear un cliente de prueba de FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def sample_empresa_data():
    """Datos de ejemplo para una empresa con valores únicos"""
    unique_id = str(uuid.uuid4())[:8].replace('-', '')  # Primeros 8 caracteres del UUID
    return {
        "nombre": f"Empresa de Prueba {unique_id}",
        "nit": f"TEST{unique_id}",
        "activo": True
    }


@pytest.fixture(scope="function")
def sample_persona_data():
    """Datos de ejemplo para una persona con valores únicos"""
    unique_id = str(uuid.uuid4())[:8].replace('-', '')  # Primeros 8 caracteres del UUID
    return {
        "nombre": "Juan",
        "apellido": "Pérez",
        "documento": f"TEST{unique_id}",
        "email": f"juan.perez.{unique_id}@test.com",
        "telefono": f"300{unique_id[-7:]}",
        "activo": True
    }


@pytest.fixture(scope="function")
def sample_tipo_cultivo_data():
    """Datos de ejemplo para un tipo de cultivo con valores únicos"""
    unique_id = str(uuid.uuid4())[:8].replace('-', '')  # Primeros 8 caracteres del UUID
    return {
        "nombre": f"Hortalizas {unique_id}",
        "descripcion": f"Cultivos de hortalizas {unique_id}"
    }


@pytest.fixture(scope="function")
def sample_nutriente_data():
    """Datos de ejemplo para un nutriente con valores únicos"""
    unique_id = str(uuid.uuid4())[:8].replace('-', '')  # Primeros 8 caracteres del UUID
    return {
        "nombre": f"Nitrógeno {unique_id}",
        "formula_quimica": f"N{unique_id[-3:]}",
        "descripcion": f"Nutriente esencial para el crecimiento {unique_id}"
    }

