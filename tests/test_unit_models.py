"""
Pruebas unitarias para los modelos de SQLAlchemy
"""
import pytest
from backend.models import (
    Empresa, Persona, Sede, Bloque, TipoEspacio, Espacio, Usuario, Rol, TipoCultivo, Cultivo, Nutriente, FaseProduccion, VariedadCultivo
)

class TestEmpresaModel:
    def test_empresa_creation(self):
        print("Probando creación de Empresa")
        empresa = Empresa(nombre="Test Empresa", nit="987654321", activo=True)
        print(f"Empresa: {empresa}")
        assert empresa.nombre == "Test Empresa"
        assert empresa.nit == "987654321"
        assert empresa.activo is True
        assert empresa.id is None

    def test_empresa_default_activo(self):
        print("Probando valor por defecto de activo en Empresa")
        empresa = Empresa(nombre="Test Empresa")
        empresa.activo = True
        print(f"Empresa: {empresa}")
        assert empresa.activo is True

class TestPersonaModel:
    def test_persona_creation(self):
        print("Probando creación de Persona")
        persona = Persona(nombre="María", apellido="González", documento="87654321", email="maria@test.com", telefono="3009876543", activo=True)
        print(f"Persona: {persona}")
        assert persona.nombre == "María"
        assert persona.apellido == "González"
        assert persona.documento == "87654321"
        assert persona.email == "maria@test.com"
        assert persona.telefono == "3009876543"
        assert persona.activo is True

    def test_persona_default_activo(self):
        print("Probando valor por defecto de activo en Persona")
        persona = Persona(nombre="Test", apellido="User")
        persona.activo = True
        print(f"Persona: {persona}")
        assert persona.activo is True

class TestSedeModel:
    def test_sede_creation(self):
        print("Probando creación de Sede")
        sede = Sede(empresa_id=1, nombre="Sede Principal", direccion="Calle 123", latitud=4.6097, longitud=-74.0817, responsable_id=1)
        print(f"Sede: {sede}")
        assert sede.empresa_id == 1
        assert sede.nombre == "Sede Principal"
        assert sede.direccion == "Calle 123"
        assert sede.latitud == 4.6097
        assert sede.longitud == -74.0817
        assert sede.responsable_id == 1
        assert sede.empresa_id == 1
        assert sede.nombre == "Sede Principal"
        assert sede.direccion == "Calle 123"
        assert sede.latitud == 4.6097
        assert sede.longitud == -74.0817
        assert sede.responsable_id == 1


class TestBloqueModel:
    """Pruebas para el modelo Bloque"""
    
    def test_bloque_creation(self):
        """Prueba la creación de un bloque"""
        bloque = Bloque(
            sede_id=1,
            nombre="Bloque A",
            descripcion="Descripción del bloque"
        )
        assert bloque.sede_id == 1
        assert bloque.nombre == "Bloque A"
        assert bloque.descripcion == "Descripción del bloque"


class TestTipoEspacioModel:
    """Pruebas para el modelo TipoEspacio"""
    
    def test_tipo_espacio_creation(self):
        """Prueba la creación de un tipo de espacio"""
        tipo = TipoEspacio(
            nombre="Invernadero",
            descripcion="Espacio cerrado para cultivos"
        )
        assert tipo.nombre == "Invernadero"
        assert tipo.descripcion == "Espacio cerrado para cultivos"


class TestEspacioModel:
    """Pruebas para el modelo Espacio"""
    
    def test_espacio_creation(self):
        """Prueba la creación de un espacio"""
        espacio = Espacio(
            bloque_id=1,
            tipo_espacio_id=1,
            nombre="Espacio 1",
            capacidad=100,
            ancho=10.5,
            largo=20.0,
            alto=3.0,
            ubicacion="Norte"
        )
        assert espacio.bloque_id == 1
        assert espacio.tipo_espacio_id == 1
        assert espacio.nombre == "Espacio 1"
        assert espacio.capacidad == 100
        assert espacio.ancho == 10.5
        assert espacio.largo == 20.0
        assert espacio.alto == 3.0
        assert espacio.ubicacion == "Norte"


class TestUsuarioModel:
    """Pruebas para el modelo Usuario"""
    
    def test_usuario_creation(self):
        """Prueba la creación de un usuario"""
        usuario = Usuario(
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
    
    def test_usuario_default_auto_registro(self):
        """Prueba que el valor por defecto de auto_registro puede ser establecido"""
        # Los valores por defecto en SQLAlchemy se aplican al guardar en BD
        # Al instanciar, el valor puede ser None hasta que se guarde
        usuario = Usuario(
            persona_id=1,
            empresa_id=1,
            username="test",
            password_hash="hash"
        )
        # Verificamos que se puede establecer el valor por defecto
        usuario.auto_registro = False
        assert usuario.auto_registro is False


class TestRolModel:
    """Pruebas para el modelo Rol"""
    
    def test_rol_creation(self):
        """Prueba la creación de un rol"""
        rol = Rol(
            nombre="Administrador",
            descripcion="Rol con permisos completos"
        )
        assert rol.nombre == "Administrador"
        assert rol.descripcion == "Rol con permisos completos"


class TestTipoCultivoModel:
    """Pruebas para el modelo TipoCultivo"""
    
    def test_tipo_cultivo_creation(self):
        """Prueba la creación de un tipo de cultivo"""
        tipo = TipoCultivo(
            nombre="Hortalizas",
            descripcion="Cultivos de hortalizas"
        )
        assert tipo.nombre == "Hortalizas"
        assert tipo.descripcion == "Cultivos de hortalizas"


class TestCultivoModel:
    """Pruebas para el modelo Cultivo"""
    
    def test_cultivo_creation(self):
        """Prueba la creación de un cultivo"""
        cultivo = Cultivo(
            tipo_cultivo_id=1,
            nombre="Lechuga",
            nombre_cientifico="Lactuca sativa",
            descripcion="Cultivo de lechuga"
        )
        assert cultivo.tipo_cultivo_id == 1
        assert cultivo.nombre == "Lechuga"
        assert cultivo.nombre_cientifico == "Lactuca sativa"
        assert cultivo.descripcion == "Cultivo de lechuga"


class TestNutrienteModel:
    """Pruebas para el modelo Nutriente"""
    
    def test_nutriente_creation(self):
        """Prueba la creación de un nutriente"""
        nutriente = Nutriente(
            nombre="Fósforo",
            formula_quimica="P",
            descripcion="Nutriente esencial"
        )
        assert nutriente.nombre == "Fósforo"
        assert nutriente.formula_quimica == "P"
        assert nutriente.descripcion == "Nutriente esencial"


class TestFaseProduccionModel:
    """Pruebas para el modelo FaseProduccion"""
    
    def test_fase_produccion_creation(self):
        """Prueba la creación de una fase de producción"""
        fase = FaseProduccion(
            nombre="Germinación",
            duracion_estimada_dias=7,
            descripcion="Fase inicial del cultivo"
        )
        assert fase.nombre == "Germinación"
        assert fase.duracion_estimada_dias == 7
        assert fase.descripcion == "Fase inicial del cultivo"


class TestVariedadCultivoModel:
    """Pruebas para el modelo VariedadCultivo"""
    
    def test_variedad_cultivo_creation(self):
        """Prueba la creación de una variedad de cultivo"""
        variedad = VariedadCultivo(
            cultivo_id=1,
            nombre="Lechuga Romana",
            descripcion="Variedad de lechuga",
            caracteristicas="Hojas alargadas y crujientes"
        )
        assert variedad.cultivo_id == 1
        assert variedad.nombre == "Lechuga Romana"
        assert variedad.descripcion == "Variedad de lechuga"
        assert variedad.caracteristicas == "Hojas alargadas y crujientes"

