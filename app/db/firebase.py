import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import settings

class FirebaseDB:
    """
    Singleton para manejar la conexión a Firebase Admin.
    Asegura que la aplicación se inicialice una sola vez.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseDB, cls).__new__(cls)
            cls._instance.db = None
        return cls._instance

    def initialize(self):
        """Inicializa Firebase Admin solo si no está inicializado ya."""
        if not firebase_admin._apps:
            print("Inicializando conexión a Firebase...")
            cred = self._get_credentials()
            firebase_admin.initialize_app(cred)
            print("Firebase inicializado correctamente.")
        else:
            print("Firebase ya estaba inicializado.")
            
        # Obtener el cliente de Firestore
        if self.db is None:
            self.db = firestore.client()

    def _get_credentials(self):
        """
        Determina de dónde obtener las credenciales basado en el entorno.
        1. Archivo local (Desarrollo)
        2. Variable de entorno JSON (Producción)
        3. Application Default (Google Cloud)
        """
        # 1. Intentar archivo local
        if os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
            print(f"Usando credenciales desde archivo: {settings.FIREBASE_CREDENTIALS_PATH}")
            return credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        
        # 2. Intentar desde variable de entorno que contiene el JSON completo
        env_cred = os.getenv("FIREBASE_CRED_JSON")
        if env_cred:
            print("Usando credenciales desde variable de entorno FIREBASE_CRED_JSON")
            cred_dict = json.loads(env_cred)
            return credentials.Certificate(cred_dict)
        
        # 3. Caer en Default de Google Cloud
        print("Usando Application Default Credentials")
        return credentials.ApplicationDefault()

    def get_db(self):
        """Retorna el cliente de la base de datos (Firestore)."""
        if self.db is None:
            raise Exception("Firebase no ha sido inicializado. Llama a initialize() primero.")
        return self.db

# Instancia global del Singleton
firebase_db = FirebaseDB()
