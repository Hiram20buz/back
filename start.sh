#!/bin/bash
# Script para levantar el servidor backend

# Activar entorno virtual
source venv/bin/activate

# Opción recomendada: Usar python -m para evitar problemas de rutas y cargar el .env internamente
echo "Levantando backend en el puerto configurado en el .env..."
python -m app.main
