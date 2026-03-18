from fastapi import APIRouter
import asyncio
from typing import Optional

router = APIRouter(
    prefix="/v1/misc",
    tags=["Misceláneo"]
)

@router.get("/")
async def holamundo(): 
    return {"mensaje": "Hola mundo FastAPI"}

@router.get("/bienvenido")
async def bienvenido(): 
    await asyncio.sleep(2)
    return {"mensaje": "Bienvenido a FastAPI"}

# Rutas con Parámetros
@router.get("/usuario/detalles")
async def detalles(nombre: str, edad: int):
    return {
        "nombre": nombre, 
        "edad": edad,
        "mensaje": f"Hola {nombre}, tienes {edad} años."
    }

@router.get("/multiplicar/{numero}")
async def multiplicar(numero: int, multiplicador: Optional[int] = 2):
    resultado = numero * multiplicador
    return {
        "numero": numero,
        "multiplicador": multiplicador,
        "resultado": resultado
    }