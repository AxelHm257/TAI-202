from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone

# --- NUEVOS IMPORTS PARA SEGURIDAD ---
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

# --- CONFIGURACIÓN JWT ---
SECRET_KEY = "mi_clave_secreta_super_segura_123" # En producción usa variables de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Requisito: Límite máx 30 min

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos simulada
usuarios = [
    {"id": 1, "nombre": "Fany", "edad": 21},
    {"id": 2, "nombre": "Ali", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21},
]

# Usuario para pruebas de login (Simulado)
USER_DB = {"admin": "12345"} 

# --- FUNCIONES DE APOYO (Lógica JWT) ---

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

# --- RUTA PARA GENERAR TOKEN ---

@app.post("/token", tags=['Seguridad'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_pass = USER_DB.get(form_data.username)
    if not user_pass or form_data.password != user_pass:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- ENDPOINTS EXISTENTES ---

@app.get("/")
async def holamundo(): 
    return {"mensaje": "Hola mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido(): 
    await asyncio.sleep(5)
    return {"mensaje": "Bienvenido a FastAPI"}

@app.get("/usuario/detalles")
async def detalles(nombre: str, edad: int):
    return {"nombre": nombre, "edad": edad}

@app.get("/v1/usuarios/", tags=['HTTP CRUD'])
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }

class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario") 
    nombre: str = Field(..., min_length=3, max_length=50, example="Nombre")
    edad: int = Field(..., gt=1, le=123, description="Edad ", example=30)

@app.post("/v1/usuarios/", tags=['HTTP CRUD'])
async def agregar_usuarios(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id: 
            raise HTTPException(status_code=400, detail="El usuario con este ID ya existe")
    usuarios.append(usuario.dict())
    return {"mensaje": "Usuario Agregado", "Datos nuevos": usuario}

# --- ENDPOINTS PROTEGIDOS (Requisito d) ---

@app.put("/v1/usuarios/", tags=['HTTP CRUD'])
async def actualizar_usuario(usuario_id: int, usuario: dict, token: str = Depends(get_current_user)):
    for usr in usuarios:
        if usr["id"] == usuario_id:
            usr.update(usuario)
            return {"mensaje": "Usuario Actualizado (Autorizado)", "Datos actualizados": usr}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.patch("/v1/usuarios/", tags=['HTTP CRUD'])
async def modificar_usuario(usuario_id: int, usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario_id:
            usr.update(usuario)
            return {"mensaje": "Usuario Modificado", "Datos modificados": usr}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/", tags=['HTTP CRUD'])
async def eliminar_usuario(usuario_id: int, token: str = Depends(get_current_user)):
    for i, usr in enumerate(usuarios):
        if usr["id"] == usuario_id:
            usuarios.pop(i)
            return {"mensaje": "Usuario Eliminado (Autorizado)", "id eliminado": usuario_id}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")