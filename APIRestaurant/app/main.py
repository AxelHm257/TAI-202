from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(title="API de Reservas del Restaurante")
security = HTTPBasic()

# Base de datos en memoria para las reservas
reservas_db = []

# Pydantic models
class Reserva(BaseModel):
    id: int = Field(..., gt=0, description="ID de la reserva", example=1)
    nombre_cliente: str = Field(..., min_length=3, max_length=50, description="Nombre del cliente", example="Juan Pérez")
    fecha_reserva: str = Field(..., description="Fecha de la reserva en formato YYYY-MM-DD", example="2024-07-01")
    numero_personas: int = Field(..., gt=0, description="Número de personas para la reserva", example=4)
    confirmada: bool = Field(default=False, description="Estado de confirmación de la reserva")

@app.get("/", tags=['General'])
async def home():
    return {"mensaje": "Bienvenido a la API de Reservas del Restaurante"}

def verficar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "rest123")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.post("/reservas/crear", tags=['Reservas'], response_model=Reserva, status_code=status.HTTP_201_CREATED)
async def crear_reserva(reserva: Reserva):
    # Verificar si la reserva con el mismo ID ya existe
    if any(r.id == reserva.id for r in reservas_db):
        raise HTTPException(status_code=400, detail=f"La reserva con ID {reserva.id} ya existe")
    
    reservas_db.append(reserva)
    return reserva

@app.get("/reservas/listar", tags=['Reservas'], response_model=List[Reserva])
async def listar_reservas(username: str = Depends(verficar_usuario)):
    return reservas_db

@app.get("/reservas/consultar/{reserva_id}", tags=['Reservas'], response_model=Reserva)
async def consultar_por_id(reserva_id: int, username: str = Depends(verficar_usuario)):
    for reserva in reservas_db:
        if reserva.id == reserva_id:
            return reserva
    raise HTTPException(status_code=404, detail=f"Reserva con ID {reserva_id} no encontrada")

@app.put("/reservas/confirmar/{reserva_id}", tags=['Reservas'], response_model=Reserva)
async def confirmar_reserva(reserva_id: int):
    for reserva in reservas_db:
        if reserva.id == reserva_id:
            reserva.confirmada = True
            return reserva
    raise HTTPException(status_code=404, detail=f"Reserva con ID {reserva_id} no encontrada")

@app.delete("/reservas/cancelar/{reserva_id}", tags=['Reservas'])
async def cancelar_reserva(reserva_id: int):
    for i, reserva in enumerate(reservas_db):
        if reserva.id == reserva_id:
            del reservas_db[i]
            return {"mensaje": f"Reserva con ID {reserva_id} cancelada exitosamente"}
    raise HTTPException(status_code=404, detail=f"Reserva con ID {reserva_id} no encontrada")

@app.get("/usuarios/seguro", tags=['Usuarios'])
async def usuario_seguro(username: str = Depends(verficar_usuario)):
    return {
        "mensaje": f"Bienvenido, {username}. Has accedido a una ruta segura."
    }
