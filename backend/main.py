"""
API FastAPI para el sistema hidropónico
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import backend.database as db
from backend import models, schemas

app = FastAPI(title="Sistema Hidropónico API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== EMPRESA ====================
@app.get("/api/empresas", response_model=List[schemas.Empresa])
def get_empresas(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    empresas = db_session.query(models.Empresa).offset(skip).limit(limit).all()
    return empresas

@app.get("/api/empresas/{empresa_id}", response_model=schemas.Empresa)
def get_empresa(empresa_id: int, db_session: Session = Depends(db.get_db)):
    empresa = db_session.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa

@app.post("/api/empresas", response_model=schemas.Empresa)
def create_empresa(empresa: schemas.EmpresaCreate, db_session: Session = Depends(db.get_db)):
    db_empresa = models.Empresa(**empresa.dict())
    db_session.add(db_empresa)
    db_session.commit()
    db_session.refresh(db_empresa)
    return db_empresa

@app.put("/api/empresas/{empresa_id}", response_model=schemas.Empresa)
def update_empresa(empresa_id: int, empresa: schemas.EmpresaUpdate, db_session: Session = Depends(db.get_db)):
    db_empresa = db_session.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    for key, value in empresa.dict(exclude_unset=True).items():
        setattr(db_empresa, key, value)
    db_session.commit()
    db_session.refresh(db_empresa)
    return db_empresa

@app.delete("/api/empresas/{empresa_id}")
def delete_empresa(empresa_id: int, db_session: Session = Depends(db.get_db)):
    db_empresa = db_session.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    db_session.delete(db_empresa)
    db_session.commit()
    return {"message": "Empresa eliminada"}

# ==================== PERSONA ====================
@app.get("/api/personas", response_model=List[schemas.Persona])
def get_personas(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    personas = db_session.query(models.Persona).offset(skip).limit(limit).all()
    return personas

@app.get("/api/personas/{persona_id}", response_model=schemas.Persona)
def get_persona(persona_id: int, db_session: Session = Depends(db.get_db)):
    persona = db_session.query(models.Persona).filter(models.Persona.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@app.post("/api/personas", response_model=schemas.Persona)
def create_persona(persona: schemas.PersonaCreate, db_session: Session = Depends(db.get_db)):
    db_persona = models.Persona(**persona.dict())
    db_session.add(db_persona)
    db_session.commit()
    db_session.refresh(db_persona)
    return db_persona

@app.put("/api/personas/{persona_id}", response_model=schemas.Persona)
def update_persona(persona_id: int, persona: schemas.PersonaUpdate, db_session: Session = Depends(db.get_db)):
    db_persona = db_session.query(models.Persona).filter(models.Persona.id == persona_id).first()
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    for key, value in persona.dict(exclude_unset=True).items():
        setattr(db_persona, key, value)
    db_session.commit()
    db_session.refresh(db_persona)
    return db_persona

@app.delete("/api/personas/{persona_id}")
def delete_persona(persona_id: int, db_session: Session = Depends(db.get_db)):
    db_persona = db_session.query(models.Persona).filter(models.Persona.id == persona_id).first()
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    db_session.delete(db_persona)
    db_session.commit()
    return {"message": "Persona eliminada"}

# ==================== SEDE ====================
@app.get("/api/sedes", response_model=List[schemas.Sede])
def get_sedes(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    sedes = db_session.query(models.Sede).offset(skip).limit(limit).all()
    return sedes

@app.get("/api/sedes/{sede_id}", response_model=schemas.Sede)
def get_sede(sede_id: int, db_session: Session = Depends(db.get_db)):
    sede = db_session.query(models.Sede).filter(models.Sede.id == sede_id).first()
    if not sede:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return sede

@app.post("/api/sedes", response_model=schemas.Sede)
def create_sede(sede: schemas.SedeCreate, db_session: Session = Depends(db.get_db)):
    db_sede = models.Sede(**sede.dict())
    db_session.add(db_sede)
    db_session.commit()
    db_session.refresh(db_sede)
    return db_sede

@app.put("/api/sedes/{sede_id}", response_model=schemas.Sede)
def update_sede(sede_id: int, sede: schemas.SedeUpdate, db_session: Session = Depends(db.get_db)):
    db_sede = db_session.query(models.Sede).filter(models.Sede.id == sede_id).first()
    if not db_sede:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    for key, value in sede.dict(exclude_unset=True).items():
        setattr(db_sede, key, value)
    db_session.commit()
    db_session.refresh(db_sede)
    return db_sede

@app.delete("/api/sedes/{sede_id}")
def delete_sede(sede_id: int, db_session: Session = Depends(db.get_db)):
    db_sede = db_session.query(models.Sede).filter(models.Sede.id == sede_id).first()
    if not db_sede:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    db_session.delete(db_sede)
    db_session.commit()
    return {"message": "Sede eliminada"}

# ==================== BLOQUE ====================
@app.get("/api/bloques", response_model=List[schemas.Bloque])
def get_bloques(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    bloques = db_session.query(models.Bloque).offset(skip).limit(limit).all()
    return bloques

@app.get("/api/bloques/{bloque_id}", response_model=schemas.Bloque)
def get_bloque(bloque_id: int, db_session: Session = Depends(db.get_db)):
    bloque = db_session.query(models.Bloque).filter(models.Bloque.id == bloque_id).first()
    if not bloque:
        raise HTTPException(status_code=404, detail="Bloque no encontrado")
    return bloque

@app.post("/api/bloques", response_model=schemas.Bloque)
def create_bloque(bloque: schemas.BloqueCreate, db_session: Session = Depends(db.get_db)):
    db_bloque = models.Bloque(**bloque.dict())
    db_session.add(db_bloque)
    db_session.commit()
    db_session.refresh(db_bloque)
    return db_bloque

@app.put("/api/bloques/{bloque_id}", response_model=schemas.Bloque)
def update_bloque(bloque_id: int, bloque: schemas.BloqueUpdate, db_session: Session = Depends(db.get_db)):
    db_bloque = db_session.query(models.Bloque).filter(models.Bloque.id == bloque_id).first()
    if not db_bloque:
        raise HTTPException(status_code=404, detail="Bloque no encontrado")
    for key, value in bloque.dict(exclude_unset=True).items():
        setattr(db_bloque, key, value)
    db_session.commit()
    db_session.refresh(db_bloque)
    return db_bloque

@app.delete("/api/bloques/{bloque_id}")
def delete_bloque(bloque_id: int, db_session: Session = Depends(db.get_db)):
    db_bloque = db_session.query(models.Bloque).filter(models.Bloque.id == bloque_id).first()
    if not db_bloque:
        raise HTTPException(status_code=404, detail="Bloque no encontrado")
    db_session.delete(db_bloque)
    db_session.commit()
    return {"message": "Bloque eliminado"}

# ==================== TIPO_ESPACIO ====================
@app.get("/api/tipos-espacio", response_model=List[schemas.TipoEspacio])
def get_tipos_espacio(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    tipos = db_session.query(models.TipoEspacio).offset(skip).limit(limit).all()
    return tipos

@app.get("/api/tipos-espacio/{tipo_id}", response_model=schemas.TipoEspacio)
def get_tipo_espacio(tipo_id: int, db_session: Session = Depends(db.get_db)):
    tipo = db_session.query(models.TipoEspacio).filter(models.TipoEspacio.id == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de espacio no encontrado")
    return tipo

@app.post("/api/tipos-espacio", response_model=schemas.TipoEspacio)
def create_tipo_espacio(tipo: schemas.TipoEspacioCreate, db_session: Session = Depends(db.get_db)):
    db_tipo = models.TipoEspacio(**tipo.dict())
    db_session.add(db_tipo)
    db_session.commit()
    db_session.refresh(db_tipo)
    return db_tipo

@app.put("/api/tipos-espacio/{tipo_id}", response_model=schemas.TipoEspacio)
def update_tipo_espacio(tipo_id: int, tipo: schemas.TipoEspacioUpdate, db_session: Session = Depends(db.get_db)):
    db_tipo = db_session.query(models.TipoEspacio).filter(models.TipoEspacio.id == tipo_id).first()
    if not db_tipo:
        raise HTTPException(status_code=404, detail="Tipo de espacio no encontrado")
    for key, value in tipo.dict(exclude_unset=True).items():
        setattr(db_tipo, key, value)
    db_session.commit()
    db_session.refresh(db_tipo)
    return db_tipo

@app.delete("/api/tipos-espacio/{tipo_id}")
def delete_tipo_espacio(tipo_id: int, db_session: Session = Depends(db.get_db)):
    db_tipo = db_session.query(models.TipoEspacio).filter(models.TipoEspacio.id == tipo_id).first()
    if not db_tipo:
        raise HTTPException(status_code=404, detail="Tipo de espacio no encontrado")
    db_session.delete(db_tipo)
    db_session.commit()
    return {"message": "Tipo de espacio eliminado"}

# ==================== ESPACIO ====================
@app.get("/api/espacios", response_model=List[schemas.Espacio])
def get_espacios(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    espacios = db_session.query(models.Espacio).offset(skip).limit(limit).all()
    return espacios

@app.get("/api/espacios/{espacio_id}", response_model=schemas.Espacio)
def get_espacio(espacio_id: int, db_session: Session = Depends(db.get_db)):
    espacio = db_session.query(models.Espacio).filter(models.Espacio.id == espacio_id).first()
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    return espacio

@app.post("/api/espacios", response_model=schemas.Espacio)
def create_espacio(espacio: schemas.EspacioCreate, db_session: Session = Depends(db.get_db)):
    db_espacio = models.Espacio(**espacio.dict())
    db_session.add(db_espacio)
    db_session.commit()
    db_session.refresh(db_espacio)
    return db_espacio

@app.put("/api/espacios/{espacio_id}", response_model=schemas.Espacio)
def update_espacio(espacio_id: int, espacio: schemas.EspacioUpdate, db_session: Session = Depends(db.get_db)):
    db_espacio = db_session.query(models.Espacio).filter(models.Espacio.id == espacio_id).first()
    if not db_espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    for key, value in espacio.dict(exclude_unset=True).items():
        setattr(db_espacio, key, value)
    db_session.commit()
    db_session.refresh(db_espacio)
    return db_espacio

@app.delete("/api/espacios/{espacio_id}")
def delete_espacio(espacio_id: int, db_session: Session = Depends(db.get_db)):
    db_espacio = db_session.query(models.Espacio).filter(models.Espacio.id == espacio_id).first()
    if not db_espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    db_session.delete(db_espacio)
    db_session.commit()
    return {"message": "Espacio eliminado"}

# ==================== TIPO_ESTRUCTURA ====================
@app.get("/api/tipos-estructura", response_model=List[schemas.TipoEstructura])
def get_tipos_estructura(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    tipos = db_session.query(models.TipoEstructura).offset(skip).limit(limit).all()
    return tipos

@app.get("/api/tipos-estructura/{tipo_id}", response_model=schemas.TipoEstructura)
def get_tipo_estructura(tipo_id: int, db_session: Session = Depends(db.get_db)):
    tipo = db_session.query(models.TipoEstructura).filter(models.TipoEstructura.id == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de estructura no encontrado")
    return tipo

@app.post("/api/tipos-estructura", response_model=schemas.TipoEstructura)
def create_tipo_estructura(tipo: schemas.TipoEstructuraCreate, db_session: Session = Depends(db.get_db)):
    db_tipo = models.TipoEstructura(**tipo.dict())
    db_session.add(db_tipo)
    db_session.commit()
    db_session.refresh(db_tipo)
    return db_tipo

@app.put("/api/tipos-estructura/{tipo_id}", response_model=schemas.TipoEstructura)
def update_tipo_estructura(tipo_id: int, tipo: schemas.TipoEstructuraUpdate, db_session: Session = Depends(db.get_db)):
    db_tipo = db_session.query(models.TipoEstructura).filter(models.TipoEstructura.id == tipo_id).first()
    if not db_tipo:
        raise HTTPException(status_code=404, detail="Tipo de estructura no encontrado")
    for key, value in tipo.dict(exclude_unset=True).items():
        setattr(db_tipo, key, value)
    db_session.commit()
    db_session.refresh(db_tipo)
    return db_tipo

@app.delete("/api/tipos-estructura/{tipo_id}")
def delete_tipo_estructura(tipo_id: int, db_session: Session = Depends(db.get_db)):
    db_tipo = db_session.query(models.TipoEstructura).filter(models.TipoEstructura.id == tipo_id).first()
    if not db_tipo:
        raise HTTPException(status_code=404, detail="Tipo de estructura no encontrado")
    db_session.delete(db_tipo)
    db_session.commit()
    return {"message": "Tipo de estructura eliminado"}

# ==================== ESTRUCTURA ====================
@app.get("/api/estructuras", response_model=List[schemas.Estructura])
def get_estructuras(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    estructuras = db_session.query(models.Estructura).offset(skip).limit(limit).all()
    return estructuras

@app.get("/api/estructuras/{estructura_id}", response_model=schemas.Estructura)
def get_estructura(estructura_id: int, db_session: Session = Depends(db.get_db)):
    estructura = db_session.query(models.Estructura).filter(models.Estructura.id == estructura_id).first()
    if not estructura:
        raise HTTPException(status_code=404, detail="Estructura no encontrada")
    return estructura

@app.post("/api/estructuras", response_model=schemas.Estructura)
def create_estructura(estructura: schemas.EstructuraCreate, db_session: Session = Depends(db.get_db)):
    db_estructura = models.Estructura(**estructura.dict())
    db_session.add(db_estructura)
    db_session.commit()
    db_session.refresh(db_estructura)
    return db_estructura

@app.put("/api/estructuras/{estructura_id}", response_model=schemas.Estructura)
def update_estructura(estructura_id: int, estructura: schemas.EstructuraUpdate, db_session: Session = Depends(db.get_db)):
    db_estructura = db_session.query(models.Estructura).filter(models.Estructura.id == estructura_id).first()
    if not db_estructura:
        raise HTTPException(status_code=404, detail="Estructura no encontrada")
    for key, value in estructura.dict(exclude_unset=True).items():
        setattr(db_estructura, key, value)
    db_session.commit()
    db_session.refresh(db_estructura)
    return db_estructura

@app.delete("/api/estructuras/{estructura_id}")
def delete_estructura(estructura_id: int, db_session: Session = Depends(db.get_db)):
    db_estructura = db_session.query(models.Estructura).filter(models.Estructura.id == estructura_id).first()
    if not db_estructura:
        raise HTTPException(status_code=404, detail="Estructura no encontrada")
    db_session.delete(db_estructura)
    db_session.commit()
    return {"message": "Estructura eliminada"}

# ==================== USUARIO ====================
@app.get("/api/usuarios", response_model=List[schemas.Usuario])
def get_usuarios(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    usuarios = db_session.query(models.Usuario).offset(skip).limit(limit).all()
    return usuarios

@app.get("/api/usuarios/{usuario_id}", response_model=schemas.Usuario)
def get_usuario(usuario_id: int, db_session: Session = Depends(db.get_db)):
    usuario = db_session.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.post("/api/usuarios", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db_session: Session = Depends(db.get_db)):
    db_usuario = models.Usuario(**usuario.dict())
    db_session.add(db_usuario)
    db_session.commit()
    db_session.refresh(db_usuario)
    return db_usuario

@app.put("/api/usuarios/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioUpdate, db_session: Session = Depends(db.get_db)):
    db_usuario = db_session.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in usuario.dict(exclude_unset=True).items():
        setattr(db_usuario, key, value)
    db_session.commit()
    db_session.refresh(db_usuario)
    return db_usuario

@app.delete("/api/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int, db_session: Session = Depends(db.get_db)):
    db_usuario = db_session.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_session.delete(db_usuario)
    db_session.commit()
    return {"message": "Usuario eliminado"}

# ==================== ROL ====================
@app.get("/api/roles", response_model=List[schemas.Rol])
def get_roles(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    roles = db_session.query(models.Rol).offset(skip).limit(limit).all()
    return roles

@app.get("/api/roles/{rol_id}", response_model=schemas.Rol)
def get_rol(rol_id: int, db_session: Session = Depends(db.get_db)):
    rol = db_session.query(models.Rol).filter(models.Rol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@app.post("/api/roles", response_model=schemas.Rol)
def create_rol(rol: schemas.RolCreate, db_session: Session = Depends(db.get_db)):
    db_rol = models.Rol(**rol.dict())
    db_session.add(db_rol)
    db_session.commit()
    db_session.refresh(db_rol)
    return db_rol

@app.put("/api/roles/{rol_id}", response_model=schemas.Rol)
def update_rol(rol_id: int, rol: schemas.RolUpdate, db_session: Session = Depends(db.get_db)):
    db_rol = db_session.query(models.Rol).filter(models.Rol.id == rol_id).first()
    if not db_rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    for key, value in rol.dict(exclude_unset=True).items():
        setattr(db_rol, key, value)
    db_session.commit()
    db_session.refresh(db_rol)
    return db_rol

@app.delete("/api/roles/{rol_id}")
def delete_rol(rol_id: int, db_session: Session = Depends(db.get_db)):
    db_rol = db_session.query(models.Rol).filter(models.Rol.id == rol_id).first()
    if not db_rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db_session.delete(db_rol)
    db_session.commit()
    return {"message": "Rol eliminado"}

# ==================== USUARIO_ROL ====================
@app.get("/api/usuarios-roles", response_model=List[schemas.UsuarioRol])
def get_usuarios_roles(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    usuarios_roles = db_session.query(models.UsuarioRol).offset(skip).limit(limit).all()
    return usuarios_roles

@app.get("/api/usuarios-roles/{usuario_rol_id}", response_model=schemas.UsuarioRol)
def get_usuario_rol(usuario_rol_id: int, db_session: Session = Depends(db.get_db)):
    usuario_rol = db_session.query(models.UsuarioRol).filter(models.UsuarioRol.id == usuario_rol_id).first()
    if not usuario_rol:
        raise HTTPException(status_code=404, detail="Usuario-Rol no encontrado")
    return usuario_rol

@app.post("/api/usuarios-roles", response_model=schemas.UsuarioRol)
def create_usuario_rol(usuario_rol: schemas.UsuarioRolCreate, db_session: Session = Depends(db.get_db)):
    db_usuario_rol = models.UsuarioRol(**usuario_rol.dict())
    db_session.add(db_usuario_rol)
    db_session.commit()
    db_session.refresh(db_usuario_rol)
    return db_usuario_rol

@app.put("/api/usuarios-roles/{usuario_rol_id}", response_model=schemas.UsuarioRol)
def update_usuario_rol(usuario_rol_id: int, usuario_rol: schemas.UsuarioRolUpdate, db_session: Session = Depends(db.get_db)):
    db_usuario_rol = db_session.query(models.UsuarioRol).filter(models.UsuarioRol.id == usuario_rol_id).first()
    if not db_usuario_rol:
        raise HTTPException(status_code=404, detail="Usuario-Rol no encontrado")
    for key, value in usuario_rol.dict(exclude_unset=True).items():
        setattr(db_usuario_rol, key, value)
    db_session.commit()
    db_session.refresh(db_usuario_rol)
    return db_usuario_rol

@app.delete("/api/usuarios-roles/{usuario_rol_id}")
def delete_usuario_rol(usuario_rol_id: int, db_session: Session = Depends(db.get_db)):
    db_usuario_rol = db_session.query(models.UsuarioRol).filter(models.UsuarioRol.id == usuario_rol_id).first()
    if not db_usuario_rol:
        raise HTTPException(status_code=404, detail="Usuario-Rol no encontrado")
    db_session.delete(db_usuario_rol)
    db_session.commit()
    return {"message": "Usuario-Rol eliminado"}

# ==================== METODO_ACCESO ====================
@app.get("/api/metodos-acceso", response_model=List[schemas.MetodoAcceso])
def get_metodos_acceso(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    metodos = db_session.query(models.MetodoAcceso).offset(skip).limit(limit).all()
    return metodos

@app.get("/api/metodos-acceso/{metodo_id}", response_model=schemas.MetodoAcceso)
def get_metodo_acceso(metodo_id: int, db_session: Session = Depends(db.get_db)):
    metodo = db_session.query(models.MetodoAcceso).filter(models.MetodoAcceso.id == metodo_id).first()
    if not metodo:
        raise HTTPException(status_code=404, detail="Método de acceso no encontrado")
    return metodo

@app.post("/api/metodos-acceso", response_model=schemas.MetodoAcceso)
def create_metodo_acceso(metodo: schemas.MetodoAccesoCreate, db_session: Session = Depends(db.get_db)):
    db_metodo = models.MetodoAcceso(**metodo.dict())
    db_session.add(db_metodo)
    db_session.commit()
    db_session.refresh(db_metodo)
    return db_metodo

@app.put("/api/metodos-acceso/{metodo_id}", response_model=schemas.MetodoAcceso)
def update_metodo_acceso(metodo_id: int, metodo: schemas.MetodoAccesoUpdate, db_session: Session = Depends(db.get_db)):
    db_metodo = db_session.query(models.MetodoAcceso).filter(models.MetodoAcceso.id == metodo_id).first()
    if not db_metodo:
        raise HTTPException(status_code=404, detail="Método de acceso no encontrado")
    for key, value in metodo.dict(exclude_unset=True).items():
        setattr(db_metodo, key, value)
    db_session.commit()
    db_session.refresh(db_metodo)
    return db_metodo

@app.delete("/api/metodos-acceso/{metodo_id}")
def delete_metodo_acceso(metodo_id: int, db_session: Session = Depends(db.get_db)):
    db_metodo = db_session.query(models.MetodoAcceso).filter(models.MetodoAcceso.id == metodo_id).first()
    if not db_metodo:
        raise HTTPException(status_code=404, detail="Método de acceso no encontrado")
    db_session.delete(db_metodo)
    db_session.commit()
    return {"message": "Método de acceso eliminado"}

# ==================== ACCESO_ESPACIO ====================
@app.get("/api/accesos-espacio", response_model=List[schemas.AccesoEspacio])
def get_accesos_espacio(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    accesos = db_session.query(models.AccesoEspacio).offset(skip).limit(limit).all()
    return accesos

@app.get("/api/accesos-espacio/{acceso_id}", response_model=schemas.AccesoEspacio)
def get_acceso_espacio(acceso_id: int, db_session: Session = Depends(db.get_db)):
    acceso = db_session.query(models.AccesoEspacio).filter(models.AccesoEspacio.id == acceso_id).first()
    if not acceso:
        raise HTTPException(status_code=404, detail="Acceso a espacio no encontrado")
    return acceso

@app.post("/api/accesos-espacio", response_model=schemas.AccesoEspacio)
def create_acceso_espacio(acceso: schemas.AccesoEspacioCreate, db_session: Session = Depends(db.get_db)):
    db_acceso = models.AccesoEspacio(**acceso.dict())
    db_session.add(db_acceso)
    db_session.commit()
    db_session.refresh(db_acceso)
    return db_acceso

@app.put("/api/accesos-espacio/{acceso_id}", response_model=schemas.AccesoEspacio)
def update_acceso_espacio(acceso_id: int, acceso: schemas.AccesoEspacioUpdate, db_session: Session = Depends(db.get_db)):
    db_acceso = db_session.query(models.AccesoEspacio).filter(models.AccesoEspacio.id == acceso_id).first()
    if not db_acceso:
        raise HTTPException(status_code=404, detail="Acceso a espacio no encontrado")
    for key, value in acceso.dict(exclude_unset=True).items():
        setattr(db_acceso, key, value)
    db_session.commit()
    db_session.refresh(db_acceso)
    return db_acceso

@app.delete("/api/accesos-espacio/{acceso_id}")
def delete_acceso_espacio(acceso_id: int, db_session: Session = Depends(db.get_db)):
    db_acceso = db_session.query(models.AccesoEspacio).filter(models.AccesoEspacio.id == acceso_id).first()
    if not db_acceso:
        raise HTTPException(status_code=404, detail="Acceso a espacio no encontrado")
    db_session.delete(db_acceso)
    db_session.commit()
    return {"message": "Acceso a espacio eliminado"}

# ==================== TIPO_CULTIVO ====================
@app.get("/api/tipos-cultivo", response_model=List[schemas.TipoCultivo])
def get_tipos_cultivo(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    tipos = db_session.query(models.TipoCultivo).offset(skip).limit(limit).all()
    return tipos

@app.get("/api/tipos-cultivo/{tipo_id}", response_model=schemas.TipoCultivo)
def get_tipo_cultivo(tipo_id: int, db_session: Session = Depends(db.get_db)):
    tipo = db_session.query(models.TipoCultivo).filter(models.TipoCultivo.id == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de cultivo no encontrado")
    return tipo

@app.post("/api/tipos-cultivo", response_model=schemas.TipoCultivo)
def create_tipo_cultivo(tipo: schemas.TipoCultivoCreate, db_session: Session = Depends(db.get_db)):
    db_tipo = models.TipoCultivo(**tipo.dict())
    db_session.add(db_tipo)
    db_session.commit()
    db_session.refresh(db_tipo)
    return db_tipo

@app.put("/api/tipos-cultivo/{tipo_id}", response_model=schemas.TipoCultivo)
def update_tipo_cultivo(tipo_id: int, tipo: schemas.TipoCultivoUpdate, db_session: Session = Depends(db.get_db)):
    db_tipo = db_session.query(models.TipoCultivo).filter(models.TipoCultivo.id == tipo_id).first()
    if not db_tipo:
        raise HTTPException(status_code=404, detail="Tipo de cultivo no encontrado")
    for key, value in tipo.dict(exclude_unset=True).items():
        setattr(db_tipo, key, value)
    db_session.commit()
    db_session.refresh(db_tipo)
    return db_tipo

@app.delete("/api/tipos-cultivo/{tipo_id}")
def delete_tipo_cultivo(tipo_id: int, db_session: Session = Depends(db.get_db)):
    db_tipo = db_session.query(models.TipoCultivo).filter(models.TipoCultivo.id == tipo_id).first()
    if not db_tipo:
        raise HTTPException(status_code=404, detail="Tipo de cultivo no encontrado")
    db_session.delete(db_tipo)
    db_session.commit()
    return {"message": "Tipo de cultivo eliminado"}

# ==================== CULTIVO ====================
@app.get("/api/cultivos", response_model=List[schemas.Cultivo])
def get_cultivos(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    cultivos = db_session.query(models.Cultivo).offset(skip).limit(limit).all()
    return cultivos

@app.get("/api/cultivos/{cultivo_id}", response_model=schemas.Cultivo)
def get_cultivo(cultivo_id: int, db_session: Session = Depends(db.get_db)):
    cultivo = db_session.query(models.Cultivo).filter(models.Cultivo.id == cultivo_id).first()
    if not cultivo:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    return cultivo

@app.post("/api/cultivos", response_model=schemas.Cultivo)
def create_cultivo(cultivo: schemas.CultivoCreate, db_session: Session = Depends(db.get_db)):
    db_cultivo = models.Cultivo(**cultivo.dict())
    db_session.add(db_cultivo)
    db_session.commit()
    db_session.refresh(db_cultivo)
    return db_cultivo

@app.put("/api/cultivos/{cultivo_id}", response_model=schemas.Cultivo)
def update_cultivo(cultivo_id: int, cultivo: schemas.CultivoUpdate, db_session: Session = Depends(db.get_db)):
    db_cultivo = db_session.query(models.Cultivo).filter(models.Cultivo.id == cultivo_id).first()
    if not db_cultivo:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    for key, value in cultivo.dict(exclude_unset=True).items():
        setattr(db_cultivo, key, value)
    db_session.commit()
    db_session.refresh(db_cultivo)
    return db_cultivo

@app.delete("/api/cultivos/{cultivo_id}")
def delete_cultivo(cultivo_id: int, db_session: Session = Depends(db.get_db)):
    db_cultivo = db_session.query(models.Cultivo).filter(models.Cultivo.id == cultivo_id).first()
    if not db_cultivo:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    db_session.delete(db_cultivo)
    db_session.commit()
    return {"message": "Cultivo eliminado"}

# ==================== VARIEDAD_CULTIVO ====================
@app.get("/api/variedades-cultivo", response_model=List[schemas.VariedadCultivo])
def get_variedades_cultivo(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    variedades = db_session.query(models.VariedadCultivo).offset(skip).limit(limit).all()
    return variedades

@app.get("/api/variedades-cultivo/{variedad_id}", response_model=schemas.VariedadCultivo)
def get_variedad_cultivo(variedad_id: int, db_session: Session = Depends(db.get_db)):
    variedad = db_session.query(models.VariedadCultivo).filter(models.VariedadCultivo.id == variedad_id).first()
    if not variedad:
        raise HTTPException(status_code=404, detail="Variedad de cultivo no encontrada")
    return variedad

@app.post("/api/variedades-cultivo", response_model=schemas.VariedadCultivo)
def create_variedad_cultivo(variedad: schemas.VariedadCultivoCreate, db_session: Session = Depends(db.get_db)):
    db_variedad = models.VariedadCultivo(**variedad.dict())
    db_session.add(db_variedad)
    db_session.commit()
    db_session.refresh(db_variedad)
    return db_variedad

@app.put("/api/variedades-cultivo/{variedad_id}", response_model=schemas.VariedadCultivo)
def update_variedad_cultivo(variedad_id: int, variedad: schemas.VariedadCultivoUpdate, db_session: Session = Depends(db.get_db)):
    db_variedad = db_session.query(models.VariedadCultivo).filter(models.VariedadCultivo.id == variedad_id).first()
    if not db_variedad:
        raise HTTPException(status_code=404, detail="Variedad de cultivo no encontrada")
    for key, value in variedad.dict(exclude_unset=True).items():
        setattr(db_variedad, key, value)
    db_session.commit()
    db_session.refresh(db_variedad)
    return db_variedad

@app.delete("/api/variedades-cultivo/{variedad_id}")
def delete_variedad_cultivo(variedad_id: int, db_session: Session = Depends(db.get_db)):
    db_variedad = db_session.query(models.VariedadCultivo).filter(models.VariedadCultivo.id == variedad_id).first()
    if not db_variedad:
        raise HTTPException(status_code=404, detail="Variedad de cultivo no encontrada")
    db_session.delete(db_variedad)
    db_session.commit()
    return {"message": "Variedad de cultivo eliminada"}

# ==================== FASE_PRODUCCION ====================
@app.get("/api/fases-produccion", response_model=List[schemas.FaseProduccion])
def get_fases_produccion(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    fases = db_session.query(models.FaseProduccion).offset(skip).limit(limit).all()
    return fases

@app.get("/api/fases-produccion/{fase_id}", response_model=schemas.FaseProduccion)
def get_fase_produccion(fase_id: int, db_session: Session = Depends(db.get_db)):
    fase = db_session.query(models.FaseProduccion).filter(models.FaseProduccion.id == fase_id).first()
    if not fase:
        raise HTTPException(status_code=404, detail="Fase de producción no encontrada")
    return fase

@app.post("/api/fases-produccion", response_model=schemas.FaseProduccion)
def create_fase_produccion(fase: schemas.FaseProduccionCreate, db_session: Session = Depends(db.get_db)):
    db_fase = models.FaseProduccion(**fase.dict())
    db_session.add(db_fase)
    db_session.commit()
    db_session.refresh(db_fase)
    return db_fase

@app.put("/api/fases-produccion/{fase_id}", response_model=schemas.FaseProduccion)
def update_fase_produccion(fase_id: int, fase: schemas.FaseProduccionUpdate, db_session: Session = Depends(db.get_db)):
    db_fase = db_session.query(models.FaseProduccion).filter(models.FaseProduccion.id == fase_id).first()
    if not db_fase:
        raise HTTPException(status_code=404, detail="Fase de producción no encontrada")
    for key, value in fase.dict(exclude_unset=True).items():
        setattr(db_fase, key, value)
    db_session.commit()
    db_session.refresh(db_fase)
    return db_fase

@app.delete("/api/fases-produccion/{fase_id}")
def delete_fase_produccion(fase_id: int, db_session: Session = Depends(db.get_db)):
    db_fase = db_session.query(models.FaseProduccion).filter(models.FaseProduccion.id == fase_id).first()
    if not db_fase:
        raise HTTPException(status_code=404, detail="Fase de producción no encontrada")
    db_session.delete(db_fase)
    db_session.commit()
    return {"message": "Fase de producción eliminada"}

# ==================== CULTIVO_FASE ====================
@app.get("/api/cultivos-fases", response_model=List[schemas.CultivoFase])
def get_cultivos_fases(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    cultivos_fases = db_session.query(models.CultivoFase).offset(skip).limit(limit).all()
    return cultivos_fases

@app.get("/api/cultivos-fases/{cultivo_fase_id}", response_model=schemas.CultivoFase)
def get_cultivo_fase(cultivo_fase_id: int, db_session: Session = Depends(db.get_db)):
    cultivo_fase = db_session.query(models.CultivoFase).filter(models.CultivoFase.id == cultivo_fase_id).first()
    if not cultivo_fase:
        raise HTTPException(status_code=404, detail="Cultivo-Fase no encontrado")
    return cultivo_fase

@app.post("/api/cultivos-fases", response_model=schemas.CultivoFase)
def create_cultivo_fase(cultivo_fase: schemas.CultivoFaseCreate, db_session: Session = Depends(db.get_db)):
    db_cultivo_fase = models.CultivoFase(**cultivo_fase.dict())
    db_session.add(db_cultivo_fase)
    db_session.commit()
    db_session.refresh(db_cultivo_fase)
    return db_cultivo_fase

@app.put("/api/cultivos-fases/{cultivo_fase_id}", response_model=schemas.CultivoFase)
def update_cultivo_fase(cultivo_fase_id: int, cultivo_fase: schemas.CultivoFaseUpdate, db_session: Session = Depends(db.get_db)):
    db_cultivo_fase = db_session.query(models.CultivoFase).filter(models.CultivoFase.id == cultivo_fase_id).first()
    if not db_cultivo_fase:
        raise HTTPException(status_code=404, detail="Cultivo-Fase no encontrado")
    for key, value in cultivo_fase.dict(exclude_unset=True).items():
        setattr(db_cultivo_fase, key, value)
    db_session.commit()
    db_session.refresh(db_cultivo_fase)
    return db_cultivo_fase

@app.delete("/api/cultivos-fases/{cultivo_fase_id}")
def delete_cultivo_fase(cultivo_fase_id: int, db_session: Session = Depends(db.get_db)):
    db_cultivo_fase = db_session.query(models.CultivoFase).filter(models.CultivoFase.id == cultivo_fase_id).first()
    if not db_cultivo_fase:
        raise HTTPException(status_code=404, detail="Cultivo-Fase no encontrado")
    db_session.delete(db_cultivo_fase)
    db_session.commit()
    return {"message": "Cultivo-Fase eliminado"}

# ==================== NUTRIENTE ====================
@app.get("/api/nutrientes", response_model=List[schemas.Nutriente])
def get_nutrientes(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    nutrientes = db_session.query(models.Nutriente).offset(skip).limit(limit).all()
    return nutrientes

@app.get("/api/nutrientes/{nutriente_id}", response_model=schemas.Nutriente)
def get_nutriente(nutriente_id: int, db_session: Session = Depends(db.get_db)):
    nutriente = db_session.query(models.Nutriente).filter(models.Nutriente.id == nutriente_id).first()
    if not nutriente:
        raise HTTPException(status_code=404, detail="Nutriente no encontrado")
    return nutriente

@app.post("/api/nutrientes", response_model=schemas.Nutriente)
def create_nutriente(nutriente: schemas.NutrienteCreate, db_session: Session = Depends(db.get_db)):
    db_nutriente = models.Nutriente(**nutriente.dict())
    db_session.add(db_nutriente)
    db_session.commit()
    db_session.refresh(db_nutriente)
    return db_nutriente

@app.put("/api/nutrientes/{nutriente_id}", response_model=schemas.Nutriente)
def update_nutriente(nutriente_id: int, nutriente: schemas.NutrienteUpdate, db_session: Session = Depends(db.get_db)):
    db_nutriente = db_session.query(models.Nutriente).filter(models.Nutriente.id == nutriente_id).first()
    if not db_nutriente:
        raise HTTPException(status_code=404, detail="Nutriente no encontrado")
    for key, value in nutriente.dict(exclude_unset=True).items():
        setattr(db_nutriente, key, value)
    db_session.commit()
    db_session.refresh(db_nutriente)
    return db_nutriente

@app.delete("/api/nutrientes/{nutriente_id}")
def delete_nutriente(nutriente_id: int, db_session: Session = Depends(db.get_db)):
    db_nutriente = db_session.query(models.Nutriente).filter(models.Nutriente.id == nutriente_id).first()
    if not db_nutriente:
        raise HTTPException(status_code=404, detail="Nutriente no encontrado")
    db_session.delete(db_nutriente)
    db_session.commit()
    return {"message": "Nutriente eliminado"}

# ==================== FASE_NUTRIENTE ====================
@app.get("/api/fases-nutriente", response_model=List[schemas.FaseNutriente])
def get_fases_nutriente(skip: int = 0, limit: int = 100, db_session: Session = Depends(db.get_db)):
    fases_nutriente = db_session.query(models.FaseNutriente).offset(skip).limit(limit).all()
    return fases_nutriente

@app.get("/api/fases-nutriente/{fase_nutriente_id}", response_model=schemas.FaseNutriente)
def get_fase_nutriente(fase_nutriente_id: int, db_session: Session = Depends(db.get_db)):
    fase_nutriente = db_session.query(models.FaseNutriente).filter(models.FaseNutriente.id == fase_nutriente_id).first()
    if not fase_nutriente:
        raise HTTPException(status_code=404, detail="Fase-Nutriente no encontrada")
    return fase_nutriente

@app.post("/api/fases-nutriente", response_model=schemas.FaseNutriente)
def create_fase_nutriente(fase_nutriente: schemas.FaseNutrienteCreate, db_session: Session = Depends(db.get_db)):
    db_fase_nutriente = models.FaseNutriente(**fase_nutriente.dict())
    db_session.add(db_fase_nutriente)
    db_session.commit()
    db_session.refresh(db_fase_nutriente)
    return db_fase_nutriente

@app.put("/api/fases-nutriente/{fase_nutriente_id}", response_model=schemas.FaseNutriente)
def update_fase_nutriente(fase_nutriente_id: int, fase_nutriente: schemas.FaseNutrienteUpdate, db_session: Session = Depends(db.get_db)):
    db_fase_nutriente = db_session.query(models.FaseNutriente).filter(models.FaseNutriente.id == fase_nutriente_id).first()
    if not db_fase_nutriente:
        raise HTTPException(status_code=404, detail="Fase-Nutriente no encontrada")
    for key, value in fase_nutriente.dict(exclude_unset=True).items():
        setattr(db_fase_nutriente, key, value)
    db_session.commit()
    db_session.refresh(db_fase_nutriente)
    return db_fase_nutriente

@app.delete("/api/fases-nutriente/{fase_nutriente_id}")
def delete_fase_nutriente(fase_nutriente_id: int, db_session: Session = Depends(db.get_db)):
    db_fase_nutriente = db_session.query(models.FaseNutriente).filter(models.FaseNutriente.id == fase_nutriente_id).first()
    if not db_fase_nutriente:
        raise HTTPException(status_code=404, detail="Fase-Nutriente no encontrada")
    db_session.delete(db_fase_nutriente)
    db_session.commit()
    return {"message": "Fase-Nutriente eliminada"}

@app.get("/")
def root():
    return {"message": "Sistema Hidropónico API", "docs": "/docs"}

