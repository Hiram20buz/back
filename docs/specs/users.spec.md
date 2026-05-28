# Feature Spec: Users

## 1. Descripción
Este feature maneja el registro, consulta y listado de usuarios del sistema. Funciona interactuando con Google Cloud Firestore como base de datos NoSQL.

## 2. Modelos (Pydantic Schemas)

Los datos de entrada y salida son validados estrictamente por Pydantic. No existen modelos ORM (como SQLAlchemy).

### 2.1. Modelo Base (Campos comunes)
- `nombre` (string, min_length: 2)
- `apellido` (string, min_length: 2)
- `fecha_de_nacimiento` (string): Estrictamente validado mediante RegEx para coincidir con el formato `DD/MM/YYYY`.
- `estado` (string)
- `ciudad` (string)
- `correo_electronico` (string, EmailStr): Formato de correo válido.

### 2.2. UserCreate (Input para POST)
- Hereda del Modelo Base.
- `password` (string, min_length: 6): Contraseña en texto plano que envía el cliente.

### 2.3. UserInDB (Almacenamiento Interno)
- Hereda del Modelo Base.
- **NO** contiene `password`.
- `hashed_password` (string): El hash generado usando `bcrypt`.

### 2.4. UserResponse (Output hacia el cliente)
- Hereda del Modelo Base.
- `id` (string): El identificador único del documento auto-generado por Firestore.
- **NO** contiene el password ni el hash.

## 3. Endpoints (API V1)

Todos los endpoints están prefijados bajo `/api/v1/users`.

### 3.1. POST `/`
- **Descripción**: Crea un nuevo usuario.
- **Input**: `UserCreate` (JSON)
- **Output**: `UserResponse` (JSON, status: 201 Created)
- **Lógica**:
  1. Verifica que el `correo_electronico` no esté registrado previamente en Firestore. Si existe, lanza un HTTP 400.
  2. Genera el hash de la contraseña plana.
  3. Almacena el documento en la colección `users` de Firestore.

### 3.2. GET `/`
- **Descripción**: Lista todos los usuarios registrados.
- **Output**: Array de `UserResponse` (JSON, status: 200 OK)

### 3.3. GET `/{user_id}`
- **Descripción**: Obtiene los detalles públicos de un usuario específico.
- **Path Parameter**: `user_id` (string) correspondiente al ID del documento en Firestore.
- **Output**: `UserResponse` (JSON, status: 200 OK)
- **Errores**: HTTP 404 si el documento no existe.

## 4. Reglas de Negocio y Seguridad
- **Criptografía**: Las contraseñas NUNCA se guardan en texto plano ni se desencriptan. Se utiliza la librería `bcrypt` de manera directa para hashear y verificar.
- **Base de Datos**: Se utiliza un Singleton (`app.db.firebase.FirebaseDB`) para interactuar con Firebase Admin.
