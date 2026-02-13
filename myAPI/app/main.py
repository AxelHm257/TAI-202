from fastapi import FastAPI
import asyncio

app = FastAPI(title="Práctica de Documentación")

@app.get("/")
async def inicio():
    return {"mensaje": "Funcionando"}

@app.get("/Bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {"mensaje": "Hola Mundo FastAPI", "estatus": "200"}

@app.get("/usuario/detalles")
async def detalles(nombre: str, edad: int):
    return {"nombre": nombre, "edad": edad}