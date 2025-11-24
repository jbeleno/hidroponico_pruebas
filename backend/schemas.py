"""
Esquemas Pydantic para FastAPI
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Empresa
class EmpresaBase(BaseModel):
    nombre: str
    nit: Optional[str] = None
    activo: bool = True

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(BaseModel):
    nombre: Optional[str] = None
    nit: Optional[str] = None
    activo: Optional[bool] = None

class Empresa(EmpresaBase):
    id: int
    class Config:
        from_attributes = True


# Persona
class PersonaBase(BaseModel):
    nombre: str
    apellido: str
    documento: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    activo: bool = True

class PersonaCreate(PersonaBase):
    pass

class PersonaUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    documento: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None

class Persona(PersonaBase):
    id: int
    class Config:
        from_attributes = True


# Sede
class SedeBase(BaseModel):
    empresa_id: int
    nombre: str
    direccion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    responsable_id: Optional[int] = None

class SedeCreate(SedeBase):
    pass

class SedeUpdate(BaseModel):
    empresa_id: Optional[int] = None
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    responsable_id: Optional[int] = None

class Sede(SedeBase):
    id: int
    class Config:
        from_attributes = True


# Bloque
class BloqueBase(BaseModel):
    sede_id: int
    nombre: str
    descripcion: Optional[str] = None

class BloqueCreate(BloqueBase):
    pass

class BloqueUpdate(BaseModel):
    sede_id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class Bloque(BloqueBase):
    id: int
    class Config:
        from_attributes = True


# TipoEspacio
class TipoEspacioBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class TipoEspacioCreate(TipoEspacioBase):
    pass

class TipoEspacioUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class TipoEspacio(TipoEspacioBase):
    id: int
    class Config:
        from_attributes = True


# Espacio
class EspacioBase(BaseModel):
    bloque_id: int
    tipo_espacio_id: int
    nombre: str
    capacidad: Optional[int] = None
    ancho: Optional[float] = None
    largo: Optional[float] = None
    alto: Optional[float] = None
    ubicacion: Optional[str] = None

class EspacioCreate(EspacioBase):
    pass

class EspacioUpdate(BaseModel):
    bloque_id: Optional[int] = None
    tipo_espacio_id: Optional[int] = None
    nombre: Optional[str] = None
    capacidad: Optional[int] = None
    ancho: Optional[float] = None
    largo: Optional[float] = None
    alto: Optional[float] = None
    ubicacion: Optional[str] = None

class Espacio(EspacioBase):
    id: int
    class Config:
        from_attributes = True


# TipoEstructura
class TipoEstructuraBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class TipoEstructuraCreate(TipoEstructuraBase):
    pass

class TipoEstructuraUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class TipoEstructura(TipoEstructuraBase):
    id: int
    class Config:
        from_attributes = True


# Estructura
class EstructuraBase(BaseModel):
    espacio_id: int
    tipo_estructura_id: int
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    capacidad: Optional[int] = None
    ancho: Optional[float] = None
    largo: Optional[float] = None
    posicion_x: Optional[float] = None
    posicion_y: Optional[float] = None

class EstructuraCreate(EstructuraBase):
    pass

class EstructuraUpdate(BaseModel):
    espacio_id: Optional[int] = None
    tipo_estructura_id: Optional[int] = None
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    capacidad: Optional[int] = None
    ancho: Optional[float] = None
    largo: Optional[float] = None
    posicion_x: Optional[float] = None
    posicion_y: Optional[float] = None

class Estructura(EstructuraBase):
    id: int
    class Config:
        from_attributes = True


# Usuario
class UsuarioBase(BaseModel):
    persona_id: int
    empresa_id: int
    username: str
    password_hash: str
    auto_registro: bool = False

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    persona_id: Optional[int] = None
    empresa_id: Optional[int] = None
    username: Optional[str] = None
    password_hash: Optional[str] = None
    auto_registro: Optional[bool] = None

class Usuario(UsuarioBase):
    id: int
    fecha_creacion: Optional[datetime] = None
    ultimo_cambio_clave: Optional[datetime] = None
    class Config:
        from_attributes = True


# Rol
class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class Rol(RolBase):
    id: int
    class Config:
        from_attributes = True


# UsuarioRol
class UsuarioRolBase(BaseModel):
    usuario_id: int
    rol_id: int

class UsuarioRolCreate(UsuarioRolBase):
    pass

class UsuarioRolUpdate(BaseModel):
    usuario_id: Optional[int] = None
    rol_id: Optional[int] = None

class UsuarioRol(UsuarioRolBase):
    id: int
    class Config:
        from_attributes = True


# MetodoAcceso
class MetodoAccesoBase(BaseModel):
    usuario_id: int
    tipo: str
    dato_biometrico: Optional[str] = None
    activo: bool = True

class MetodoAccesoCreate(MetodoAccesoBase):
    pass

class MetodoAccesoUpdate(BaseModel):
    usuario_id: Optional[int] = None
    tipo: Optional[str] = None
    dato_biometrico: Optional[str] = None
    activo: Optional[bool] = None

class MetodoAcceso(MetodoAccesoBase):
    id: int
    class Config:
        from_attributes = True


# AccesoEspacio
class AccesoEspacioBase(BaseModel):
    usuario_id: int
    espacio_id: int
    metodo_acceso: Optional[str] = None

class AccesoEspacioCreate(AccesoEspacioBase):
    pass

class AccesoEspacioUpdate(BaseModel):
    usuario_id: Optional[int] = None
    espacio_id: Optional[int] = None
    metodo_acceso: Optional[str] = None

class AccesoEspacio(AccesoEspacioBase):
    id: int
    fecha_acceso: Optional[datetime] = None
    class Config:
        from_attributes = True


# TipoCultivo
class TipoCultivoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class TipoCultivoCreate(TipoCultivoBase):
    pass

class TipoCultivoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class TipoCultivo(TipoCultivoBase):
    id: int
    class Config:
        from_attributes = True


# Cultivo
class CultivoBase(BaseModel):
    tipo_cultivo_id: int
    nombre: str
    nombre_cientifico: Optional[str] = None
    descripcion: Optional[str] = None

class CultivoCreate(CultivoBase):
    pass

class CultivoUpdate(BaseModel):
    tipo_cultivo_id: Optional[int] = None
    nombre: Optional[str] = None
    nombre_cientifico: Optional[str] = None
    descripcion: Optional[str] = None

class Cultivo(CultivoBase):
    id: int
    class Config:
        from_attributes = True


# VariedadCultivo
class VariedadCultivoBase(BaseModel):
    cultivo_id: int
    nombre: str
    descripcion: Optional[str] = None
    caracteristicas: Optional[str] = None

class VariedadCultivoCreate(VariedadCultivoBase):
    pass

class VariedadCultivoUpdate(BaseModel):
    cultivo_id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    caracteristicas: Optional[str] = None

class VariedadCultivo(VariedadCultivoBase):
    id: int
    class Config:
        from_attributes = True


# FaseProduccion
class FaseProduccionBase(BaseModel):
    nombre: str
    duracion_estimada_dias: Optional[int] = None
    descripcion: Optional[str] = None

class FaseProduccionCreate(FaseProduccionBase):
    pass

class FaseProduccionUpdate(BaseModel):
    nombre: Optional[str] = None
    duracion_estimada_dias: Optional[int] = None
    descripcion: Optional[str] = None

class FaseProduccion(FaseProduccionBase):
    id: int
    class Config:
        from_attributes = True


# CultivoFase
class CultivoFaseBase(BaseModel):
    variedad_cultivo_id: int
    fase_produccion_id: int
    orden: Optional[int] = None
    duracion_dias: Optional[int] = None

class CultivoFaseCreate(CultivoFaseBase):
    pass

class CultivoFaseUpdate(BaseModel):
    variedad_cultivo_id: Optional[int] = None
    fase_produccion_id: Optional[int] = None
    orden: Optional[int] = None
    duracion_dias: Optional[int] = None

class CultivoFase(CultivoFaseBase):
    id: int
    class Config:
        from_attributes = True


# Nutriente
class NutrienteBase(BaseModel):
    nombre: str
    formula_quimica: Optional[str] = None
    descripcion: Optional[str] = None

class NutrienteCreate(NutrienteBase):
    pass

class NutrienteUpdate(BaseModel):
    nombre: Optional[str] = None
    formula_quimica: Optional[str] = None
    descripcion: Optional[str] = None

class Nutriente(NutrienteBase):
    id: int
    class Config:
        from_attributes = True


# FaseNutriente
class FaseNutrienteBase(BaseModel):
    cultivo_fase_id: int
    nutriente_id: int
    cantidad: Optional[float] = None
    unidad_medida: Optional[str] = None
    frecuencia: Optional[str] = None

class FaseNutrienteCreate(FaseNutrienteBase):
    pass

class FaseNutrienteUpdate(BaseModel):
    cultivo_fase_id: Optional[int] = None
    nutriente_id: Optional[int] = None
    cantidad: Optional[float] = None
    unidad_medida: Optional[str] = None
    frecuencia: Optional[str] = None

class FaseNutriente(FaseNutrienteBase):
    id: int
    class Config:
        from_attributes = True

