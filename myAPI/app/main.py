from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field # <--- Importamos las validaciones
from typing import Optional 
import asyncio

app = FastAPI(
    title="Mi primer API",
    description="Ivan Isay Guerra L",
    version="1.0"
)

# 1. Definimos el Modelo de Validación (Pydantic)
class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50)
    edad: int = Field(..., ge=1, le=123)

usuarios = [
    {"id": 1, "nombre": "Eros", "edad": 21},
    {"id": 2, "nombre": "Axel", "edad": 20},
    {"id": 3, "nombre": "Carmen", "edad": 21},
]

@app.get("/v1/usuarios/", tags=['HTTP CRUD'])
async def leer_usuarios():
    return {"total": len(usuarios), "usuarios": usuarios}

@app.post("/v1/usuarios/", tags=['HTTP CRUD'], status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuario: crear_usuario): # <--- Usamos el modelo aquí
    # Verificamos si el ID ya existe
    if any(usr["id"] == usuario.id for usr in usuarios):
        raise HTTPException(status_code=400, detail="El id ya existe")
    
    # Convertimos el modelo a diccionario para guardarlo
    usuarios.append(usuario.model_dump()) 
    return {"mensaje": "Usuario Creado", "datos": usuario}

@app.delete("/v1/usuarios/{usuario_id}", tags=['HTTP CRUD'])
async def eliminar_usuario(usuario_id: int):
    for i, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuario_eliminado = usuarios.pop(i)
            return {"mensaje": "Usuario eliminado", "usuario": usuario_eliminado}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# (Tus rutas PUT y PATCH se quedan igual o puedes adaptarlas luego)