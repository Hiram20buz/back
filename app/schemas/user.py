import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserBase(BaseModel):
    nombre: str = Field(..., min_length=2, example="Juan")
    apellido: str = Field(..., min_length=2, example="Pérez")
    fecha_de_nacimiento: str = Field(..., example="25/12/1990")
    estado: str = Field(..., example="Jalisco")
    ciudad: str = Field(..., example="Guadalajara")
    correo_electronico: EmailStr = Field(..., example="juan.perez@email.com")
    role: str = Field(default="user", example="user")

    @field_validator("fecha_de_nacimiento")
    def validate_date_format(cls, v):
        # Validar el formato DD/MM/YYYY con una expresión regular sencilla
        pattern = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/\d{4}$"
        if not re.match(pattern, v):
            raise ValueError("La fecha de nacimiento debe estar en formato DD/MM/YYYY")
        
        # Opcional: Validar que sea una fecha real usando datetime
        try:
            datetime.strptime(v, "%d/%m/%Y")
        except ValueError:
            raise ValueError("La fecha ingresada no es una fecha válida en el calendario")
        
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="contraseñaSegura123")

class UserLogin(BaseModel):
    correo_electronico: EmailStr = Field(..., example="juan.perez@email.com")
    password: str = Field(..., example="contraseñaSegura123")

class UserInDB(UserBase):
    hashed_password: str
    
    def to_dict(self):
        """Convierte el modelo a un diccionario apto para Firestore"""
        return self.model_dump()

class UserResponse(UserBase):
    id: str
    
    class Config:
        from_attributes = True
