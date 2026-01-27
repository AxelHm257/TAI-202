#importaciones
from fastapi import FastAPI
import asyncio

#insrancia del servidor
app= FastAPI()

#endpoints
@app.get("/")
async def holamundo():
    return {"mensaje":"Hola Mundo FastAPI"}

@app.get("/Bienvenido")
async def Bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje":"Hola Mundo FastAPI",
        "estatus":"200",
    }
