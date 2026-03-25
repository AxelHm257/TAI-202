from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.usuario import crear_usuario, actualizar_usuario_schema, usuario_response
from app.data.usuarios import usuario as UsuarioDB
from app.data.db import get_db
from app.security.auth import verificar_peticion
from typing import List

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)

@router.get("/")
async def leer_usuarios(db: Session = Depends(get_db)):
   
    queryUsuarios = db.query(UsuarioDB).all()
    
    return {
        "total": len(queryUsuarios),
        "usuarios": queryUsuarios,
        "status": "200"
    }

@router.get("/{usuario_id}", response_model=usuario_response)
async def leer_usuario_por_id(usuario_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    return db_user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=usuario_response)
async def agregar_usuarios(usuario_in: crear_usuario, db: Session = Depends(get_db)):
    # Crear nueva instancia de base de datos sin pasar el ID
    nuevo_usuario = UsuarioDB(
        nombre=usuario_in.nombre,
        edad=usuario_in.edad
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario

@router.put("/{usuario_id}", response_model=usuario_response)
async def actualizar_usuario(usuario_id: int, usuario_update: actualizar_usuario_schema, db: Session = Depends(get_db)):
    db_user = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    # Actualizar campos
    update_data = usuario_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.delete("/{usuario_id}")
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db), usuarioAuth: str = Depends(verificar_peticion)):
    db_user = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    db.delete(db_user)
    db.commit()
    
    return {
        "mensaje": f"Usuario Eliminado por {usuarioAuth}",
        "id eliminado": usuario_id
    }
