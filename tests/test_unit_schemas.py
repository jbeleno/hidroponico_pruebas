"""
Pruebas unitarias para los esquemas de Pydantic
"""
import pytest
from backend import schemas
from pydantic import ValidationError

class TestEmpresaSchemas:
    def test_empresa_create_valid(self):
        print("Probando creación de EmpresaCreate")
        empresa = schemas.EmpresaCreate(nombre="Test Empresa", nit="123456789", activo=True)
        print(f"EmpresaCreate: {empresa}")
        assert empresa.nombre == "Test Empresa"
        assert empresa.nit == "123456789"
        assert empresa.activo is True

    def test_empresa_create_default_activo(self):
        print("Probando valor por defecto de activo en EmpresaCreate")
        empresa = schemas.EmpresaCreate(nombre="Test Empresa")
        print(f"EmpresaCreate: {empresa}")
        assert empresa.activo is True

    def test_empresa_create_missing_nombre(self):
        print("Probando error por falta de nombre en EmpresaCreate")
        with pytest.raises(ValidationError):
            schemas.EmpresaCreate(nit="123456789")

    def test_empresa_update_partial(self):
        print("Probando actualización parcial de EmpresaUpdate")
        empresa_update = schemas.EmpresaUpdate(nombre="Nuevo Nombre")
        print(f"EmpresaUpdate: {empresa_update}")
        assert empresa_update.nombre == "Nuevo Nombre"
        assert empresa_update.nit is None
        assert empresa_update.activo is None

class TestPersonaSchemas:
    def test_persona_create_valid(self):
        persona = schemas.PersonaCreate(nombre="Juan", apellido="Pérez", documento="12345678", email="juan@test.com", telefono="3001234567", activo=True)
        assert persona.nombre == "Juan"
        assert persona.apellido == "Pérez"
        assert persona.documento == "12345678"
        assert persona.email == "juan@test.com"
        assert persona.telefono == "3001234567"
        assert persona.activo is True

    def test_persona_create_required_fields(self):
        with pytest.raises(ValidationError):
            schemas.PersonaCreate(nombre="Juan")
        with pytest.raises(ValidationError):
            schemas.PersonaCreate(apellido="Pérez")

class TestSedeSchemas:
    def test_sede_create_valid(self):
        sede = schemas.SedeCreate(
            empresa_id=1,
            nombre="Sede Principal",
            direccion="Calle 123",
            latitud=4.6097,
            longitud=-74.0817,
            responsable_id=1
        )
        assert sede.empresa_id == 1
        assert sede.nombre == "Sede Principal"
        assert sede.direccion == "Calle 123"
        assert sede.latitud == 4.6097
        assert sede.longitud == -74.0817
        assert sede.responsable_id == 1
    
    def test_sede_create_required_fields(self):
        """Prueba que empresa_id y nombre son requeridos"""
        with pytest.raises(ValidationError):
            schemas.SedeCreate(nombre="Sede")
        
        with pytest.raises(ValidationError):
            schemas.SedeCreate(empresa_id=1)


class TestTipoCultivoSchemas:
    """Pruebas para los esquemas de TipoCultivo"""
    
    def test_tipo_cultivo_create_valid(self):
        """Prueba la creación de un esquema TipoCultivoCreate válido"""
        tipo = schemas.TipoCultivoCreate(
            nombre="Hortalizas",
            descripcion="Cultivos de hortalizas"
        )
        assert tipo.nombre == "Hortalizas"
        assert tipo.descripcion == "Cultivos de hortalizas"
    
    def test_tipo_cultivo_create_required_nombre(self):
        """Prueba que nombre es requerido"""
        with pytest.raises(ValidationError):
            schemas.TipoCultivoCreate(descripcion="Descripción")


class TestNutrienteSchemas:
    """Pruebas para los esquemas de Nutriente"""
    
    def test_nutriente_create_valid(self):
        """Prueba la creación de un esquema NutrienteCreate válido"""
        nutriente = schemas.NutrienteCreate(
            nombre="Nitrógeno",
            formula_quimica="N",
            descripcion="Nutriente esencial"
        )
        assert nutriente.nombre == "Nitrógeno"
        assert nutriente.formula_quimica == "N"
        assert nutriente.descripcion == "Nutriente esencial"
    
    def test_nutriente_create_required_nombre(self):
        """Prueba que nombre es requerido"""
        with pytest.raises(ValidationError):
            schemas.NutrienteCreate(formula_quimica="N")


class TestCultivoSchemas:
    """Pruebas para los esquemas de Cultivo"""
    
    def test_cultivo_create_valid(self):
        """Prueba la creación de un esquema CultivoCreate válido"""
        cultivo = schemas.CultivoCreate(
            tipo_cultivo_id=1,
            nombre="Lechuga",
            nombre_cientifico="Lactuca sativa",
            descripcion="Cultivo de lechuga"
        )
        assert cultivo.tipo_cultivo_id == 1
        assert cultivo.nombre == "Lechuga"
        assert cultivo.nombre_cientifico == "Lactuca sativa"
        assert cultivo.descripcion == "Cultivo de lechuga"
    
    def test_cultivo_create_required_fields(self):
        """Prueba que tipo_cultivo_id y nombre son requeridos"""
        with pytest.raises(ValidationError):
            schemas.CultivoCreate(nombre="Lechuga")
        
        with pytest.raises(ValidationError):
            schemas.CultivoCreate(tipo_cultivo_id=1)


class TestUsuarioSchemas:
    """Pruebas para los esquemas de Usuario"""
    
    def test_usuario_create_valid(self):
        """Prueba la creación de un esquema UsuarioCreate válido"""
        usuario = schemas.UsuarioCreate(
            persona_id=1,
            empresa_id=1,
            username="testuser",
            password_hash="hashed_password",
            auto_registro=False
        )
        assert usuario.persona_id == 1
        assert usuario.empresa_id == 1
        assert usuario.username == "testuser"
        assert usuario.password_hash == "hashed_password"
        assert usuario.auto_registro is False
    
    def test_usuario_create_required_fields(self):
        """Prueba que todos los campos principales son requeridos"""
        with pytest.raises(ValidationError):
            schemas.UsuarioCreate(
                persona_id=1,
                empresa_id=1,
                username="test"
                # Falta password_hash
            )


class TestRolSchemas:
    """Pruebas para los esquemas de Rol"""
    
    def test_rol_create_valid(self):
        """Prueba la creación de un esquema RolCreate válido"""
        rol = schemas.RolCreate(
            nombre="Administrador",
            descripcion="Rol con permisos completos"
        )
        assert rol.nombre == "Administrador"
        assert rol.descripcion == "Rol con permisos completos"
    
    def test_rol_create_required_nombre(self):
        """Prueba que nombre es requerido"""
        with pytest.raises(ValidationError):
            schemas.RolCreate(descripcion="Descripción")

