# Usamos una imagen oficial de Python como base
FROM python:3.13-bullseye

# Configuramos el directorio de trabajo
WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
COPY LICENSE LICENSE
COPY README.md README.md

# Instalamos dependencias necesarias del sistema
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Instalamos UV usando pip (más confiable)
RUN pip install uv

# Verificamos que UV funcione
RUN uv --version

RUN uv sync

COPY . .

# Comando por defecto: ejecutar el script con uv
CMD ["uv", "run", "src/main.py"]