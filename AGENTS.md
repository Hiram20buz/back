# AGENTS.md

Este archivo contiene el contexto vital para cualquier agente de IA (como OpenCode o Copilot) que trabaje en este repositorio. Su objetivo es evitar que los agentes cometan errores comunes y ayudarlos a entender las convenciones y herramientas del proyecto rápidamente.

## 🏗 Metodología: Spec-Driven Development
Este proyecto sigue una metodología guiada por especificaciones. **Antes de implementar o modificar un Feature**, debes:
1. Buscar o crear su archivo `.spec.md` correspondiente dentro del directorio `docs/specs/`.
2. Leer la especificación detalladamente para comprender los modelos, reglas de negocio y endpoints.
3. El código debe escribirse basándose estrictamente en lo definido en el archivo `.spec.md`.

## 🏗 Arquitectura y Convenciones del Repositorio

El proyecto es un backend en **Python** utilizando **FastAPI** y **Firebase/Firestore (NoSQL)**.

- **`app/main.py`**: Es el entrypoint del servidor. Contiene la instanciación de FastAPI y maneja el ciclo de vida de la app (`lifespan`), incluyendo la inicialización del Singleton de la base de datos.
- **`app/api/v1/`**: Controladores de los endpoints. La lógica de negocio **NO** debe ir aquí.
- **`app/services/`**: Aquí reside la lógica de negocio real y las consultas/interacciones con Firestore. Los controladores en `api` llaman a los métodos en `services`.
- **`app/schemas/`**: Puesto que usamos Firestore (NoSQL), no existen modelos ORM (como SQLAlchemy). Toda la validación de entrada/salida se realiza con esquemas de **Pydantic** aquí.
- **`app/utils/`**: Funciones auxiliares, como seguridad (hasheo de contraseñas con bcrypt).
- **`app/db/`**: Patrón Singleton para mantener una única conexión con `firebase-admin`.
- **`app/core/config.py`**: Configuración central utilizando `pydantic-settings` para cargar variables de entorno y defaults.

## 🔑 Base de Datos y Autenticación (Firebase)

- **¡NO SUBAS LAS CLAVES!**: La conexión a Firestore requiere el archivo JSON de cuenta de servicio de Firebase. Este archivo debe llamarse **`firekeys.json`** y ubicarse en la raíz del proyecto. **Nunca debe subirse a Git** (ya está en `.gitignore`).
- **Singleton Inteligente**: El archivo `app/db/firebase.py` está configurado para:
  1. Buscar `firekeys.json` en local.
  2. Leer la variable de entorno `FIREBASE_CRED_JSON` si no hay archivo (para despliegues en producción).
  3. Utilizar Default Credentials si está en Google Cloud.

## 💻 Desarrollo Local

### 1. Activar Entorno Virtual
Siempre trabaja dentro del entorno virtual:
```bash
source venv/bin/activate
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Levantar el Servidor
Utiliza el script de ayuda proporcionado en la raíz para evitar problemas de paths de importación en Python:
```bash
./start.sh
```
*Internamente, el script ejecuta: `python -m app.main` y respeta el `$PORT` (default 8000).*

### 4. Endpoints Importantes
- **Documentación Swagger:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health` (Útil para saber si Firebase conectó bien).

## 🛡️ Detalles Importantes para Agentes

- **Fechas**: La fecha de nacimiento de usuarios se maneja estrictamente en el formato string **`DD/MM/YYYY`** (Validado con RegEx en Pydantic).
- **Seguridad**: Las contraseñas NUNCA se guardan en texto plano ni se "desencriptan". Se hace hash y validación utilizando directamente la librería `bcrypt` en `app/utils/security.py`. No se utiliza `passlib`.
- **Dependencias**: Si agregas una librería, recuerda hacer `pip freeze > requirements.txt` para mantener el archivo actualizado.
