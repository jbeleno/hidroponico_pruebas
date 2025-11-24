"""
Pruebas unitarias para los endpoints de la API
"""
import pytest
from fastapi import status


@pytest.mark.unit
class TestEmpresaAPI:
    """Pruebas para los endpoints de Empresa"""
    
    def test_get_empresas_empty(self, client):
        """Prueba obtener lista de empresas cuando está vacía"""
        response = client.get("/api/empresas")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
    
    def test_create_empresa(self, client, sample_empresa_data):
        """Prueba crear una empresa"""
        response = client.post("/api/empresas", json=sample_empresa_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nombre"] == sample_empresa_data["nombre"]
        assert data["nit"] == sample_empresa_data["nit"]
        assert data["activo"] == sample_empresa_data["activo"]
        assert "id" in data
    
    def test_get_empresa_by_id(self, client, sample_empresa_data):
        """Prueba obtener una empresa por ID"""
        # Crear empresa primero
        create_response = client.post("/api/empresas", json=sample_empresa_data)
        empresa_id = create_response.json()["id"]
        
        # Obtener empresa
        response = client.get(f"/api/empresas/{empresa_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == empresa_id
        assert data["nombre"] == sample_empresa_data["nombre"]
    
    def test_get_empresa_not_found(self, client):
        """Prueba obtener una empresa que no existe"""
        response = client.get("/api/empresas/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_empresa(self, client, sample_empresa_data):
        """Prueba actualizar una empresa"""
        # Crear empresa primero
        create_response = client.post("/api/empresas", json=sample_empresa_data)
        empresa_id = create_response.json()["id"]
        
        # Actualizar empresa
        update_data = {"nombre": "Empresa Actualizada"}
        response = client.put(f"/api/empresas/{empresa_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nombre"] == "Empresa Actualizada"
        assert data["nit"] == sample_empresa_data["nit"]  # No cambió
    
    def test_delete_empresa(self, client, sample_empresa_data):
        """Prueba eliminar una empresa"""
        # Crear empresa primero
        create_response = client.post("/api/empresas", json=sample_empresa_data)
        empresa_id = create_response.json()["id"]
        
        # Eliminar empresa
        response = client.delete(f"/api/empresas/{empresa_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Empresa eliminada"
        
        # Verificar que fue eliminada
        get_response = client.get(f"/api/empresas/{empresa_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.unit
class TestPersonaAPI:
    """Pruebas para los endpoints de Persona"""
    
    def test_create_persona(self, client, sample_persona_data):
        """Prueba crear una persona"""
        response = client.post("/api/personas", json=sample_persona_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nombre"] == sample_persona_data["nombre"]
        assert data["apellido"] == sample_persona_data["apellido"]
        assert data["email"] == sample_persona_data["email"]
        assert "id" in data
    
    def test_get_personas(self, client, sample_persona_data):
        """Prueba obtener lista de personas"""
        # Crear una persona primero
        client.post("/api/personas", json=sample_persona_data)
        
        # Obtener lista
        response = client.get("/api/personas")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


@pytest.mark.unit
class TestTipoCultivoAPI:
    """Pruebas para los endpoints de TipoCultivo"""
    
    def test_create_tipo_cultivo(self, client, sample_tipo_cultivo_data):
        """Prueba crear un tipo de cultivo"""
        response = client.post("/api/tipos-cultivo", json=sample_tipo_cultivo_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nombre"] == sample_tipo_cultivo_data["nombre"]
        assert "id" in data
    
    def test_get_tipo_cultivo_by_id(self, client, sample_tipo_cultivo_data):
        """Prueba obtener un tipo de cultivo por ID"""
        # Crear tipo de cultivo primero
        create_response = client.post("/api/tipos-cultivo", json=sample_tipo_cultivo_data)
        tipo_id = create_response.json()["id"]
        
        # Obtener tipo de cultivo
        response = client.get(f"/api/tipos-cultivo/{tipo_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == tipo_id


@pytest.mark.unit
class TestNutrienteAPI:
    """Pruebas para los endpoints de Nutriente"""
    
    def test_create_nutriente(self, client, sample_nutriente_data):
        """Prueba crear un nutriente"""
        response = client.post("/api/nutrientes", json=sample_nutriente_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nombre"] == sample_nutriente_data["nombre"]
        assert data["formula_quimica"] == sample_nutriente_data["formula_quimica"]
        assert "id" in data
    
    def test_get_nutrientes(self, client, sample_nutriente_data):
        """Prueba obtener lista de nutrientes"""
        # Crear un nutriente primero
        client.post("/api/nutrientes", json=sample_nutriente_data)
        
        # Obtener lista
        response = client.get("/api/nutrientes")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


@pytest.mark.unit
class TestRootEndpoint:
    """Pruebas para el endpoint raíz"""
    
    def test_root_endpoint(self, client):
        """Prueba el endpoint raíz"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "docs" in data


@pytest.mark.unit
class TestAPIValidation:
    """Pruebas de validación de la API"""
    
    def test_create_empresa_missing_required_field(self, client):
        """Prueba crear empresa sin campo requerido"""
        response = client.post("/api/empresas", json={"nit": "123"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_persona_missing_required_fields(self, client):
        """Prueba crear persona sin campos requeridos"""
        response = client.post("/api/personas", json={"nombre": "Juan"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_update_nonexistent_empresa(self, client):
        """Prueba actualizar una empresa que no existe"""
        response = client.put("/api/empresas/99999", json={"nombre": "Nueva"})
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_nonexistent_empresa(self, client):
        """Prueba eliminar una empresa que no existe"""
        response = client.delete("/api/empresas/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

