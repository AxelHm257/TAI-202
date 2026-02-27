from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="API Biblioteca Digital UPQ")

# MODELOS (Pydantic)
class Libro(BaseModel):
    id: int
    titulo: str = Field(..., min_length=2, max_length=100)
    autor: str
    paginas: int = Field(..., gt=1) # 
    anio: int = Field(..., gt=1450, le=datetime.now().year) 
    estado: str = Field("disponible", pattern="^(disponible|prestado)$") 

class Prestamo(BaseModel):
    id_prestamo: int
    libro_id: int
    usuario_nombre: str
    usuario_correo: EmailStr 

# BASE DE DATOS TEMPORAL
libros = []
prestamos = []

# ENDPOINTS
@app.post("/libros/", status_code=status.HTTP_201_CREATED, tags=["Libros"]) 
async def registrar_libro(libro: Libro):
    if any(l["id"] == libro.id for l in libros):
        raise HTTPException(status_code=400, detail="ID de libro ya registrado")
    libros.append(libro.model_dump())
    return {"mensaje": "Libro registrado exitosamente", "libro": libro}

@app.get("/libros/", tags=["Libros"]) # 
async def listar_libros():
    return libros

@app.get("/libros/buscar", tags=["Libros"]) 
async def buscar_libro(nombre: str):
    resultado = [l for l in libros if nombre.lower() in l["titulo"].lower()]
    return resultado

@app.post("/prestamos/", status_code=201, tags=["Prestamos"])
async def registrar_prestamo(p: Prestamo):
    # Buscar el libro
    libro = next((l for l in libros if l["id"] == p.libro_id), None)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    if libro["estado"] == "prestado":
        raise HTTPException(status_code=409, detail="El libro ya está prestado") # 
    
    libro["estado"] = "prestado"
    prestamos.append(p.model_dump())
    return {"mensaje": "Préstamo registrado", "prestamo": p}

@app.put("/libros/devolver/{libro_id}", status_code=200, tags=["Prestamos"]) 
async def devolver_libro(libro_id: int):
    libro = next((l for l in libros if l["id"] == libro_id), None)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    libro["estado"] = "disponible"
    return {"mensaje": "Libro devuelto exitosamente"}

@app.delete("/prestamos/{id_prestamo}", tags=["Prestamos"])
async def eliminar_prestamo(id_prestamo: int):
    global prestamos
    # Verificar si el préstamo existe antes de intentar borrarlo
    prestamo_existente = next((p for p in prestamos if p["id_prestamo"] == id_prestamo), None)
    
    if not prestamo_existente:
        raise HTTPException(status_code=409, detail="El registro de préstamo ya no existe") 
    
    prestamos = [p for p in prestamos if p["id_prestamo"] != id_prestamo]
    return {"mensaje": "Registro de préstamo eliminado"}