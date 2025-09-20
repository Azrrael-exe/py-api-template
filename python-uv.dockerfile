# Usamos una imagen oficial de Python como base
FROM python:3.13-bullseye

# Configuramos el directorio de trabajo
WORKDIR /app

# Instalamos dependencias necesarias del sistema
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Instalamos UV usando pip (más confiable)
RUN pip install uv

# Verificamos que UV funcione
RUN uv --version

# Comando por defecto: abrir Python
CMD ["python3"]