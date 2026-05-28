import bcrypt

def get_password_hash(password: str) -> str:
    """
    Recibe una contraseña en texto plano y devuelve un hash seguro usando bcrypt.
    """
    # bcrypt requiere bytes, así que codificamos el string a utf-8
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    
    # Devolvemos el hash como string para poder guardarlo en Firestore
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compara la contraseña en texto plano con el hash guardado en la base de datos.
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

