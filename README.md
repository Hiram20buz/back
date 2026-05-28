# FastAPI + Firebase (NoSQL) Backend Skeleton

Bienvenido al esqueleto base para el desarrollo de backends en Python utilizando **FastAPI** y **Firebase/Firestore**. Este proyecto está diseñado para ser ligero, seguro y guiado por especificaciones (Spec-Driven Development), ideal para iniciar proyectos robustos rápidamente.

## 🚀 Tecnologías Principales

- **[FastAPI](https://fastapi.tiangolo.com/):** Framework web rápido (alto rendimiento) y moderno.
- **[Firebase Admin (Firestore)](https://firebase.google.com/docs/admin/setup):** Base de datos NoSQL en tiempo real de Google.
- **[Pydantic](https://docs.pydantic.dev/):** Validación de datos y gestión de configuraciones (Schemas).
- **[Bcrypt](https://pypi.org/project/bcrypt/):** Hasheo seguro de contraseñas de última generación.

## 🏗️ Arquitectura del Proyecto

El proyecto sigue un patrón modular limpio adaptado para NoSQL:

```text
.
├── app/
│   ├── api/v1/         # Controladores (Endpoints de FastAPI)
│   ├── core/           # Configuraciones globales y variables de entorno
│   ├── db/             # Conexión Singleton a Firestore
│   ├── schemas/        # Modelos Pydantic (Validación de Input/Output)
│   ├── services/       # Lógica de Negocio y comunicación con Firestore
│   ├── utils/          # Funciones auxiliares (Seguridad, criptografía)
│   └── main.py         # Entrypoint de la aplicación y ciclo de vida (Lifespan)
├── docs/specs/         # Especificaciones de Features (Spec-Driven Development)
├── .env                # Variables de entorno
├── firekeys.json       # (NO INCLUIDO) Credenciales de Firebase Admin
└── start.sh            # Script rápido de inicialización local
```

## 🧠 Metodología: Spec-Driven Development

Este proyecto promueve el **Spec-Driven Development**. Antes de escribir código para una nueva funcionalidad (Feature), se debe documentar primero en la carpeta `docs/specs/`. 

Por ejemplo, revisa `docs/specs/users.spec.md` para ver cómo se estructuran los requerimientos, esquemas y endpoints antes de programar.

## ⚙️ Configuración y Despliegue Local

### 1. Variables de Entorno y Credenciales
El proyecto requiere un archivo `.env` en la raíz (puedes copiar y adaptar el existente) y el archivo de credenciales de tu Service Account de Firebase.

1. Ve a tu consola de Firebase -> Configuración del Proyecto -> Cuentas de Servicio.
2. Genera una nueva clave privada.
3. Renombra el archivo descargado a **`firekeys.json`** y colócalo en la raíz del proyecto. *(Tranquilo, ya está en el `.gitignore` por seguridad).*

### 2. Instalación del Entorno
Es obligatorio el uso de un entorno virtual para mantener las dependencias aisladas.

```bash
# Crear el entorno virtual (solo la primera vez)
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Levantar el Servidor
Para facilitar la inicialización y evitar problemas de rutas relativas con Python, se incluye un script ejecutable:

```bash
./start.sh
```
*Si tienes problemas de permisos con el script, ejecuta `chmod +x start.sh`.*

El servidor levantará por defecto en `http://localhost:8000`.

## 🌐 Endpoints Disponibles (Base)

Una vez que el servidor esté corriendo, puedes acceder a la documentación interactiva (Swagger UI) auto-generada por FastAPI en:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

**Rutas principales (V1):**
* `GET /health` : Verifica el estado del servidor y la conexión a la base de datos.
* `POST /api/v1/users/` : Registro de nuevos usuarios con validación de edad y contraseña cifrada.
* `GET /api/v1/users/` : Lista de todos los usuarios registrados.

## 🛡️ Seguridad y Buenas Prácticas

- **Cifrado Real:** No se usan librerías obsoletas. La validación y encriptación dependen directamente del puerto moderno de `bcrypt`.
- **Inyección de Dependencias:** El uso estricto de Pydantic asegura que datos mal formados (ej. fechas inválidas) sean rechazados antes de que la lógica de negocio se ejecute.
- **Conexión Eficiente:** Firebase se inicializa usando el patrón Singleton durante el *Lifespan* de FastAPI, previniendo cuellos de botella y errores por múltiples inicializaciones.
