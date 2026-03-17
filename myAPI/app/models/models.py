from pydantic import BaseModel, Field

class crear_usuario(BaseModel):
    id:int=Field(...,gt=0, description="Identificador de usuario") 
    nombre:str=Field(..., min_length=3, max_length=50, example="Nombre")
    edad:int=Field(..., gt=1, le=123, description="Edad ", example=30)