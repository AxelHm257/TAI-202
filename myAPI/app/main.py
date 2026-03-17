from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router.usuario import router as usuario_router
from app.router.misc import router as misc_router

app = FastAPI(
    title="Mi API con FastAPI",
    description="Axel Santiago Horta Martínez",
    version="1.0.0"

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_router)
app.include_router(misc_router)