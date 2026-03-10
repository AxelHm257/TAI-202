from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import Optional
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials #<- importando el httpbasic,credentials#
import secrets

app = FastAPI()
security = HTTPBasic()

class crear_reserva(BaseModel):
    id:int=Field(...,gt=0, description="ID de la reserva", example=1) 
    nombre_cliente:str=Field(...,min_length=3, max_length=50, description="Nombre del cliente", example="Juan Pérez")
    fecha_reserva:str=Field(...,description="Fecha de la reserva en formato YYYY-MM-DD", example="2024-07-01")
    numero_personas:int=Field(...,gt=0, description="Número de personas para la reserva", example=4)