from fastapi import APIRouter, status
from typing import List

from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate):
    """
    Crea un nuevo usuario validando el formato de fecha (DD/MM/YYYY) y
    almacenando el hash de la contraseña en Firestore.
    """
    return user_service.create_user(user)

@router.post("/login", response_model=UserResponse)
def login_user(login_data: UserLogin):
    """
    Inicia sesión verificando el correo electrónico y la contraseña.
    """
    return user_service.authenticate_user(login_data)

@router.get("", response_model=List[UserResponse])
def get_all_users():
    """
    Obtiene la lista de todos los usuarios registrados (sin devolver la contraseña).
    """
    return user_service.get_users()

@router.get("/{user_id}", response_model=UserResponse)
def get_single_user(user_id: str):
    """
    Obtiene los datos públicos de un usuario específico mediante su ID.
    """
    return user_service.get_user(user_id)
