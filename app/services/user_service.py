from fastapi import HTTPException, status
from google.cloud.firestore_v1.client import Client
from typing import List, Optional

from app.schemas.user import UserCreate, UserInDB, UserResponse
from app.utils.security import get_password_hash
from app.db.firebase import firebase_db

COLLECTION_NAME = "users"

def _get_db() -> Client:
    return firebase_db.get_db()

def get_user_by_email(email: str) -> Optional[dict]:
    """Busca un usuario por correo electrónico para evitar duplicados."""
    db = _get_db()
    users_ref = db.collection(COLLECTION_NAME)
    # Busca donde el correo coincida, usando argumentos posicionales simples
    query = users_ref.where("correo_electronico", "==", email).limit(1).stream()
    
    for doc in query:
        return doc.to_dict()
    return None

def create_user(user_in: UserCreate) -> UserResponse:
    """Crea un nuevo usuario en Firestore, guardando la contraseña encriptada."""
    # 1. Verificar que el correo no exista
    if get_user_by_email(user_in.correo_electronico):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )
    
    # 2. Hashear la contraseña y preparar el diccionario de datos
    db_user = UserInDB(
        **user_in.model_dump(exclude={"password"}),
        hashed_password=get_password_hash(user_in.password)
    )
    
    db = _get_db()
    # 3. Guardar en Firestore. Firestore autogenerará el ID.
    _, doc_ref = db.collection(COLLECTION_NAME).add(db_user.to_dict())
    
    # 4. Retornar los datos públicos con el ID autogenerado
    return UserResponse(**db_user.model_dump(), id=doc_ref.id)

def get_user(user_id: str) -> UserResponse:
    """Obtiene un usuario por su ID de Firestore."""
    db = _get_db()
    doc_ref = db.collection(COLLECTION_NAME).document(user_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Combinar los datos del documento con su ID real
    user_data = doc.to_dict()
    user_data["id"] = doc.id
    return UserResponse(**user_data)

def get_users() -> List[UserResponse]:
    """Obtiene todos los usuarios de la base de datos."""
    db = _get_db()
    users_ref = db.collection(COLLECTION_NAME)
    docs = users_ref.stream()
    
    users = []
    for doc in docs:
        user_data = doc.to_dict()
        user_data["id"] = doc.id
        users.append(UserResponse(**user_data))
        
    return users
