#Importaciones
from fastapi import FastAPI
from app.routers import usuario, misc
from app.data.db import engine, Base
from app.data import usuarios  # Importamos el módulo para registrar el modelo

# Crear las tablas en la base de datos al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mi API con FastAPI",
    description="Axel Santiago Horta Martínez",
    version="1.0.0"
)

# Incluir routers correctamente usando los módulos importados
app.include_router(usuario.router)
app.include_router(misc.router)
