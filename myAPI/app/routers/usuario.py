from fastapi import APIRouter, HTTPException, Depends
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)

@router.get("/")
async def leer_usuarios():
    return{
        "total":len(usuarios),
        "usuarios":usuarios,
        "status": "200"
    }

@router.post("/")
async def agregar_usuarios(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id: 
            raise HTTPException(
                status_code=400,
                detail="El usuario con este ID ya existe"
            )
    usuarios.append(usuario.dict())
    return {
        "mensaje":"Usuario Agregado",
        "Datos nuevos":usuario
    }

@router.put("/")
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

@router.patch("/")
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

@router.delete("/")
async def eliminar_usuario(usuario_id: int,usuarioAuth:str=Depends(verificar_peticion)):
    for i, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuarios.pop(i)
            return{
                "mensaje": f"Usuario Eliminado por {usuarioAuth}",
                "id eliminado": usuario_id,
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )