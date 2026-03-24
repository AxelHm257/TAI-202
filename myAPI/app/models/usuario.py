from pydantic import BaseModel, Field
from typing import Optional

class crear_usuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, example="Nombre")
    edad: int = Field(..., gt=1, le=123, description="Edad ", example=30)

    