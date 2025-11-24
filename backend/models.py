"""
Modelos SQLAlchemy para todas las entidades del sistema hidropónico
"""
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Empresa(Base):
    __tablename__ = "empresa"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    nit = Column(String(50), unique=True)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    sedes = relationship("Sede", back_populates="empresa")
    usuarios = relationship("Usuario", back_populates="empresa")


class Persona(Base):
    __tablename__ = "persona"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento = Column(String(50), unique=True)
    email = Column(String(150), unique=True)
    telefono = Column(String(20))
    activo = Column(Boolean, default=True)
    
    # Relaciones
    sedes_responsable = relationship("Sede", back_populates="responsable")
    usuarios = relationship("Usuario", back_populates="persona")


class Sede(Base):
    __tablename__ = "sede"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresa.id"), nullable=False)
    nombre = Column(String(150), nullable=False)
    direccion = Column(String(200))
    latitud = Column(Float)
    longitud = Column(Float)
    responsable_id = Column(Integer, ForeignKey("persona.id"))
    
    # Relaciones
    empresa = relationship("Empresa", back_populates="sedes")
    responsable = relationship("Persona", back_populates="sedes_responsable")
    bloques = relationship("Bloque", back_populates="sede")


class Bloque(Base):
    __tablename__ = "bloque"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sede_id = Column(Integer, ForeignKey("sede.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    
    # Relaciones
    sede = relationship("Sede", back_populates="bloques")
    espacios = relationship("Espacio", back_populates="bloque")


class TipoEspacio(Base):
    __tablename__ = "tipo_espacio"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    
    # Relaciones
    espacios = relationship("Espacio", back_populates="tipo_espacio")


class Espacio(Base):
    __tablename__ = "espacio"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    bloque_id = Column(Integer, ForeignKey("bloque.id"), nullable=False)
    tipo_espacio_id = Column(Integer, ForeignKey("tipo_espacio.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    capacidad = Column(Integer)
    ancho = Column(Float)
    largo = Column(Float)
    alto = Column(Float)
    ubicacion = Column(String(200))
    
    # Relaciones
    bloque = relationship("Bloque", back_populates="espacios")
    tipo_espacio = relationship("TipoEspacio", back_populates="espacios")
    estructuras = relationship("Estructura", back_populates="espacio")
    accesos = relationship("AccesoEspacio", back_populates="espacio")


class TipoEstructura(Base):
    __tablename__ = "tipo_estructura"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    
    # Relaciones
    estructuras = relationship("Estructura", back_populates="tipo_estructura")


class Estructura(Base):
    __tablename__ = "estructura"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    espacio_id = Column(Integer, ForeignKey("espacio.id"), nullable=False)
    tipo_estructura_id = Column(Integer, ForeignKey("tipo_estructura.id"), nullable=False)
    codigo = Column(String(50), unique=True)
    nombre = Column(String(100))
    capacidad = Column(Integer)
    ancho = Column(Float)
    largo = Column(Float)
    posicion_x = Column(Float)
    posicion_y = Column(Float)
    
    # Relaciones
    espacio = relationship("Espacio", back_populates="estructuras")
    tipo_estructura = relationship("TipoEstructura", back_populates="estructuras")


class Usuario(Base):
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    persona_id = Column(Integer, ForeignKey("persona.id"), nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresa.id"), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    auto_registro = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    ultimo_cambio_clave = Column(DateTime)
    
    # Relaciones
    persona = relationship("Persona", back_populates="usuarios")
    empresa = relationship("Empresa", back_populates="usuarios")
    roles = relationship("UsuarioRol", back_populates="usuario")
    metodos_acceso = relationship("MetodoAcceso", back_populates="usuario")
    accesos = relationship("AccesoEspacio", back_populates="usuario")


class Rol(Base):
    __tablename__ = "rol"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    
    # Relaciones
    usuarios = relationship("UsuarioRol", back_populates="rol")


class UsuarioRol(Base):
    __tablename__ = "usuario_rol"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    rol_id = Column(Integer, ForeignKey("rol.id"), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="roles")
    rol = relationship("Rol", back_populates="usuarios")


class MetodoAcceso(Base):
    __tablename__ = "metodo_acceso"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    tipo = Column(String(50), nullable=False)
    dato_biometrico = Column(String(500))
    activo = Column(Boolean, default=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="metodos_acceso")


class AccesoEspacio(Base):
    __tablename__ = "acceso_espacio"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    espacio_id = Column(Integer, ForeignKey("espacio.id"), nullable=False)
    fecha_acceso = Column(DateTime, default=datetime.utcnow)
    metodo_acceso = Column(String(50))
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="accesos")
    espacio = relationship("Espacio", back_populates="accesos")


class TipoCultivo(Base):
    __tablename__ = "tipo_cultivo"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    
    # Relaciones
    cultivos = relationship("Cultivo", back_populates="tipo_cultivo")


class Cultivo(Base):
    __tablename__ = "cultivo"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_cultivo_id = Column(Integer, ForeignKey("tipo_cultivo.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    nombre_cientifico = Column(String(150))
    descripcion = Column(String(255))
    
    # Relaciones
    tipo_cultivo = relationship("TipoCultivo", back_populates="cultivos")
    variedades = relationship("VariedadCultivo", back_populates="cultivo")


class VariedadCultivo(Base):
    __tablename__ = "variedad_cultivo"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cultivo_id = Column(Integer, ForeignKey("cultivo.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    caracteristicas = Column(String(500))
    
    # Relaciones
    cultivo = relationship("Cultivo", back_populates="variedades")
    fases = relationship("CultivoFase", back_populates="variedad_cultivo")


class FaseProduccion(Base):
    __tablename__ = "fase_produccion"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    duracion_estimada_dias = Column(Integer)
    descripcion = Column(String(255))
    
    # Relaciones
    cultivos_fases = relationship("CultivoFase", back_populates="fase_produccion")


class CultivoFase(Base):
    __tablename__ = "cultivo_fase"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    variedad_cultivo_id = Column(Integer, ForeignKey("variedad_cultivo.id"), nullable=False)
    fase_produccion_id = Column(Integer, ForeignKey("fase_produccion.id"), nullable=False)
    orden = Column(Integer)
    duracion_dias = Column(Integer)
    
    # Relaciones
    variedad_cultivo = relationship("VariedadCultivo", back_populates="fases")
    fase_produccion = relationship("FaseProduccion", back_populates="cultivos_fases")
    nutrientes = relationship("FaseNutriente", back_populates="cultivo_fase")


class Nutriente(Base):
    __tablename__ = "nutriente"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    formula_quimica = Column(String(100))
    descripcion = Column(String(255))
    
    # Relaciones
    fases = relationship("FaseNutriente", back_populates="nutriente")


class FaseNutriente(Base):
    __tablename__ = "fase_nutriente"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cultivo_fase_id = Column(Integer, ForeignKey("cultivo_fase.id"), nullable=False)
    nutriente_id = Column(Integer, ForeignKey("nutriente.id"), nullable=False)
    cantidad = Column(Float)
    unidad_medida = Column(String(20))
    frecuencia = Column(String(50))
    
    # Relaciones
    cultivo_fase = relationship("CultivoFase", back_populates="nutrientes")
    nutriente = relationship("Nutriente", back_populates="fases")

