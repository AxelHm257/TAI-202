from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import Optional
from pydantic import BaseModel,Field 
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

usuarios=[
    {"id":1,"nombre":"Fany","edad":21},
    {"id":2,"nombre":"Ali","edad":21},
    {"id":3,"nombre":"Dulce","edad":21},
]

@app.get("/")
async def holamundo(): 
    return {"mensaje": "Hola mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido(): 
    await asyncio.sleep(5)
    return {"mensaje": "Bienvenido a FastAPI"}


@app.get("/usuario/detalles")
async def detalles(nombre: str, edad: int):
    return {"nombre":nombre, "edad": edad}



@app.get("/v1/usuarios/",tags=['HTTP CRUD'])
async def leer_usuarios():
    return{
        "total":len(usuarios),
        "usuarios":usuarios,
        "status": "200"
    }


class crear_usuario(BaseModel):
    id:int=Field(...,gt=0, description="Identificador de usuario") 
    nombre:str=Field(..., min_length=3, max_length=50, example="Nombre")
    edad:int=Field(..., gt=1, le=123, description="Edad ", example=30)

@app.post("/v1/usuarios/",tags=['HTTP CRUD'])
async def agregar_usuarios(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id: 
            raise HTTPException(
                status_code=400,
                detail="El usuario con este ID ya existe"
            )
    usuarios.append(usuario)
    return {
        "mensaje":"Usuario Agregado",
        "Datos nuevos":usuario
    }


@app.put("/v1/usuarios/",tags=['HTTP CRUD'])
async def actualizar_usuario(usuario_id: int, usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario_id:
            usr.update(usuario)
            return{
                "mensaje": "Usuario Actualizado",
                "Datos actualizados": usr,
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.patch("/v1/usuarios/",tags=['HTTP CRUD'])
async def modificar_usuario(usuario_id: int, usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario_id:
            usr.update(usuario)
            return{
                "mensaje": "Usuario Modificado",
                "Datos modificados": usr,
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuarios/",tags=['HTTP CRUD'])
async def eliminar_usuario(usuario_id: int):
    for i, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuarios.pop(i)
            return{
                "mensaje": "Usuario Eliminado",
                "id eliminado": usuario_id,
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )