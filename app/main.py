import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

# Importar configuración, base de datos y rutas
from app.core.config import settings
from app.db.firebase import firebase_db
from app.api.v1 import users

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    firebase_db.initialize()
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Registrar enrutadores (Rutas de la API)
app.include_router(users.router, prefix="/api/v1")

@app.get("/health", status_code=200, tags=["Health"])
def health_check():
    db = firebase_db.get_db()
    db_status = "conectado" if db else "desconectado"
    return {"status": "vivo", "database": db_status}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
