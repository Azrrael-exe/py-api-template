## Índice

1. [Introducción a Docker](#1-introducción-a-docker)  
2. [Primeros pasos con Docker](#2-primeros-pasos-con-docker)  
3. [Creación de imágenes personalizadas con Dockerfile](#3-creación-de-imágenes-personalizadas-con-dockerfile)  
4. [Volúmenes, puertos y variables de entorno](#4-volúmenes-puertos-y-variables-de-entorno)  
5. [Despliegue de una aplicación Python simple (FastAPI + UV)](#5-despliegue-de-una-aplicación-python-simple-fastapi--uv)  
6. [Buenas prácticas y recursos adicionales](#6-buenas-prácticas-y-recursos-adicionales)  
7. [Uso de Docker Compose (FastAPI + Redis)](#7-uso-de-docker-compose)  

## 1. Introducción a Docker

### ¿Qué es Docker?
Docker es una plataforma que permite empaquetar aplicaciones y todos sus componentes (librerías, dependencias, configuraciones) dentro de un **contenedor**.  
Un contenedor es como una pequeña "caja" aislada que se ejecuta en cualquier sistema que tenga Docker instalado, sin importar el sistema operativo o las configuraciones locales.  
Esto resuelve el clásico problema de: *“en mi máquina funciona, pero en la tuya no”*.

---

### Motivaciones e importancia de Docker en el software moderno
Antes de Docker, los desarrolladores tenían que lidiar con entornos muy distintos entre sus equipos, los servidores de pruebas y los servidores de producción.  
Esto generaba incompatibilidades, errores difíciles de replicar y largas configuraciones manuales.

Docker cambió este panorama al permitir:
- **Portabilidad**: la misma aplicación corre igual en cualquier máquina con Docker.
- **Rapidez**: levantar un contenedor tarda segundos, mucho menos que iniciar una máquina virtual.
- **Escalabilidad**: en arquitecturas modernas (microservicios, cloud), es posible correr decenas o cientos de contenedores distribuidos.
- **Estandarización**: equipos de desarrollo, pruebas y operaciones usan las mismas imágenes, reduciendo errores.
- **Productividad**: los desarrolladores se enfocan en el código y no en configurar entornos complicados.

Hoy en día, Docker es una de las bases del **despliegue de software moderno en la nube**.  
Se integra con plataformas como **Kubernetes, AWS, Azure y GCP**, permitiendo que las aplicaciones sean más fáciles de distribuir, escalar y mantener.

---

### Contenedores vs Máquinas Virtuales

**Máquinas Virtuales (VMs)**
- Simulan un sistema operativo completo (incluyendo el kernel).
- Requieren más recursos (RAM, CPU, disco).
- Son más lentas de iniciar.

**Contenedores**
- Comparten el kernel del sistema anfitrión.
- Mantienen aislamiento de procesos y librerías.
- Son mucho más livianos y rápidos de arrancar.

---

### Diagrama Conceptual

Contenedor vs Máquina Virtual:

| Máquina Virtual                        | Contenedor                                      |
|----------------------------------------|-------------------------------------------------|
| Sistema Operativo invitado (kernel + librerías) | Aplicación + dependencias                        |
| Hipervisor                             | Aislado, comparte kernel con el sistema anfitrión |
| Hardware físico                        | Hardware físico                                  |

### Conceptos clave de Docker
- **Imagen**: plantilla de solo lectura con todo lo necesario para ejecutar una aplicación (ejemplo: Ubuntu con Python).
- **Contenedor**: instancia en ejecución de una imagen. Puede iniciarse, detenerse o eliminarse en segundos.
- **Dockerfile**: archivo de instrucciones que define cómo se construye una imagen.
- **Docker Hub**: repositorio público (como GitHub, pero para imágenes) donde se pueden encontrar y compartir imágenes listas para usar.

---

### Ejemplo conceptual
- Una **imagen** es como una receta de cocina.  
- Un **contenedor** es el plato ya preparado.  
- El **Dockerfile** es la lista de pasos detallados para cocinar.  
- **Docker Hub** es un recetario gigante compartido por la comunidad.

# 2) Primeros Pasos con Docker

En esta sección aprenderemos a manejar los **comandos básicos** de Docker y a construir nuestra **primera imagen personalizada** usando un `Dockerfile`.

---

## Comandos Básicos de Docker

**Listar contenedores activos**
```bash
docker ps
```
Listar todos los contenedores (incluidos detenidos)

```bash
docker ps -a
```
Descargar una imagen desde Docker Hub

```bash
docker pull ubuntu
```
Ejecutar un contenedor en segundo plano

```bash
docker run -d ubuntu sleep 60
```
👉 Este comando ejecuta un contenedor de Ubuntu que simplemente "duerme" por 60 segundos.

Detener un contenedor

```bash
docker stop <ID_DEL_CONTENEDOR>
```
Eliminar un contenedor

```bash
docker rm <ID_DEL_CONTENEDOR>
```
Eliminar una imagen

```bash
docker rmi ubuntu
```
Construyendo una Imagen con Dockerfile
En lugar de usar solo imágenes existentes, podemos crear las nuestras.

1. Crear una aplicación sencilla
Creamos un archivo llamado app.py:

```python
print("Hola, soy una app dentro de un contenedor 🚀")
```
2. Escribir un Dockerfile
Creamos un archivo llamado Dockerfile en el mismo directorio:

```dockerfile
# Usamos una imagen base de Python
FROM python:3.10-slim

# Copiamos el archivo app.py al contenedor
COPY app.py /app/app.py

# Definimos el directorio de trabajo
WORKDIR /app

# Comando por defecto al iniciar el contenedor
CMD ["python", "app.py"]
```
3. Construir la imagen
```bash
docker build -t mi-primera-app .
```
4. Ejecutar el contenedor
```bash
docker run mi-primera-app
```
👉 Al ejecutar el contenedor verás el mensaje en pantalla:

```bash
Hola, soy una app dentro de un contenedor 🚀
```
## Ideas Clave
- Docker no solo sirve para ejecutar imágenes existentes (como Ubuntu o Nginx), también permite empaquetar nuestras propias aplicaciones.

- El Dockerfile es la receta que asegura que cualquier persona (o servidor) pueda construir el mismo entorno.

- Con docker build y docker run, pasamos de un simple archivo Python a una aplicación contenedorizada y portable.```

---

## 2. Primeros pasos con Docker

### Verificación de la instalación
Lo primero es asegurarse de que Docker está correctamente instalado en tu máquina.  
Abre la terminal y ejecuta:

```bash
docker --version
```
Esto debería mostrar la versión instalada de Docker.
Si no lo hace, significa que la instalación no se completó correctamente.

Descargar e iniciar un contenedor de Ubuntu
Ejecutemos un contenedor interactivo de Ubuntu:

```bash
docker run -it ubuntu
```
run: crea y ejecuta un contenedor.

-it: abre una terminal interactiva.

ubuntu: es la imagen base que se descargará de Docker Hub si no la tienes localmente.

Esto te llevará a un prompt similar a:

```bash
root@<id_contenedor>:/#
```
Aquí estás dentro del contenedor, como si fuera un pequeño sistema operativo aislado.

Probar el funcionamiento del contenedor
Dentro del contenedor puedes ejecutar comandos básicos de Linux:

```bash

ls
pwd
echo "Hola desde Docker"
```
Si quieres instalar una utilidad y usarla, por ejemplo curl:

```bash
apt-get update
apt-get install -y curl
curl https://www.google.com
```
Esto mostrará el HTML de la página de Google, confirmando que tienes conectividad desde el contenedor.

⚠️ Nota: si eliminas este contenedor, los cambios (como la instalación de curl) no persistirán, porque cada contenedor es efímero.

Comandos básicos para gestionar contenedores
Listar contenedores en ejecución

```bash
docker ps
```
Listar todos los contenedores (incluidos los detenidos)

```bash
docker ps -a
```
Detener un contenedor

```bash
docker stop <id_o_nombre>
```
Eliminar un contenedor detenido

```bash
docker rm <id_o_nombre>
```
Ver imágenes descargadas en tu máquina

```bash
docker images
```
Ejecutar un comando directamente en Ubuntu sin entrar al contenedor
Si solo quieres correr un comando y salir:

```bash
docker run ubuntu echo "Hola desde un contenedor"
```
Esto creará un contenedor de Ubuntu, ejecutará el comando y luego se cerrará automáticamente.

Entrar a un contenedor en ejecución
Si quieres acceder a un contenedor ya iniciado:

```bash
docker exec -it <id_o_nombre> bash
```
## Idea clave
- Cada contenedor es un entorno aislado y desechable.
- Puedes iniciar múltiples contenedores de Ubuntu, probar cosas dentro, detenerlos y borrarlos, sin que esto afecte a tu sistema operativo principal.

---

## 3. Creación de imágenes personalizadas con Dockerfile

### ¿Qué es un Dockerfile?
Un **Dockerfile** es un archivo de texto con instrucciones para construir una imagen personalizada.  
En lugar de configurar manualmente un contenedor cada vez, usamos un Dockerfile para definir los pasos de instalación, lo que permite reproducir siempre el mismo entorno.

---

### Ejemplo: crear una imagen de Python con UV
Supongamos que queremos preparar una imagen de **Python 3.12** lista para proyectos modernos, y que incluya **UV**, una herramienta rápida de gestión de entornos y dependencias.

1. Crea un archivo llamado `Dockerfile` en una carpeta vacía.  
2. Escribe lo siguiente dentro:

```dockerfile
# Usamos una imagen oficial de Python como base
FROM python:3.13-bullseye

# Configuramos el directorio de trabajo
WORKDIR /app

# Instalamos dependencias necesarias del sistema
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Instalamos UV usando pip (más confiable)
RUN pip install uv

# Comando por defecto: abrir Python
CMD ["python3"]
```
Construir la imagen
En la terminal, estando en la carpeta del Dockerfile, ejecuta:

```bash
docker build -t python-uv .
```
-t python-uv: asigna el nombre a la nueva imagen.

. indica que el contexto de construcción es la carpeta actual.

Ejecutar un contenedor desde esta imagen
Inicia un contenedor interactivo con:

```bash
docker run -it python-uv
```
Dentro podrás verificar que Python y UV están disponibles:

```bash
python --version
uv --version
```
## Ventajas de este enfoque
- La imagen ya tiene Python y UV listos, evitando configuraciones manuales.

- Cualquier persona del equipo puede usar la misma imagen, asegurando consistencia.

- Sienta la base para construir aplicaciones Python más complejas dentro de contenedores.

---

## 4. Volúmenes, puertos y variables de entorno

### Introducción
Hasta ahora hemos trabajado con contenedores aislados, pero en proyectos reales necesitamos:
- **Guardar datos** para que no se pierdan al detener el contenedor.
- **Exponer servicios** al exterior para poder acceder desde el navegador u otras apps.
- **Configurar parámetros** de forma flexible sin tener que reconstruir la imagen.

Docker resuelve esto con **volúmenes**, **puertos** y **variables de entorno**.

---

### 1. Volúmenes: persistencia de datos
Los contenedores son efímeros: si eliminas uno, sus datos desaparecen.  
Con volúmenes podemos montar carpetas de tu máquina dentro del contenedor.

Ejemplo: montar la carpeta actual en `/app` dentro del contenedor:

```bash
docker run -it -v $(pwd):/app python-uv bash
```
Ahora, cualquier archivo que crees en tu máquina dentro de la carpeta actual aparecerá también dentro del contenedor en /app, y viceversa.
Esto es útil para desarrollo, porque puedes editar archivos en tu editor favorito y ejecutarlos dentro del contenedor.

2. Puertos: exponer servicios
Por defecto, los servicios dentro de un contenedor no son accesibles desde fuera.
Debemos mapear puertos con -p.

Ejemplo: si tenemos una aplicación que corre dentro del contenedor en el puerto 5000, la exponemos en el puerto 8080 de la máquina local:

```bash
docker run -p 8080:5000 python-uv-app
```
Con esto, puedes abrir tu navegador en http://localhost:8080 y acceder al servicio del contenedor.

3. Variables de entorno: configuración flexible
En lugar de hardcodear configuraciones dentro del código, podemos usar variables de entorno.

Ejemplo: ejecutar un contenedor y pasarle una variable de entorno:

```bash
docker run -e APP_MODE=development python-uv bash
```
Dentro del contenedor, esa variable estará disponible como:

```bash
echo $APP_MODE
```
Esto permite que la misma imagen se comporte de forma distinta según el entorno (desarrollo, pruebas, producción).

Ejemplo combinado
Podemos unir las tres características en un solo comando:

```bash
docker run -it \
  -v $(pwd):/app \
  -p 8080:5000 \
  -e APP_MODE=development \
  python-uv-app
```
Este comando:

Monta tu carpeta actual dentro del contenedor.

Expone el puerto 5000 del contenedor en el 8080 de tu máquina.

Define la variable de entorno APP_MODE=development.

## Idea clave
- Volúmenes, puertos y variables de entorno son los tres pilares para trabajar con contenedores en proyectos reales:

- Volúmenes: persistencia de datos.

- Puertos: acceso desde fuera del contenedor.

- Variables de entorno: configuración flexible sin modificar la imagen.
---

## 5. Despliegue de una aplicación Python simple (FastAPI + UV)

### Objetivo
Desplegar una **API con FastAPI** dentro de un contenedor Docker.  
El script principal (`src/main.py`) usará **uv** para ejecutar `uvicorn` desde el propio script, manteniendo un flujo moderno y reproducible.

---

**Paso 1:** Crear el Dockerfile
Crea un archivo Dockerfile en la misma carpeta:

```dockerfile
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

COPY . .

# Comando por defecto: ejecutar el script con uv
CMD ["uv", "run", "src/main.py"]
```
**Paso 2:** Construir la imagen
En la terminal, estando en la carpeta donde se encuentran Dockerfile y app.py:

```bash
docker build -t py-api-template .
```
**Paso 4:** Ejecutar la aplicación
Ejecuta el contenedor y expón el puerto 5000 en el 8080 local:

```bash
docker run -p 8000:8000 py-api-template
```
Abre en tu navegador:
http://localhost:8080/api/healt

La respuesta será un JSON similar a:

```json
{
    "app_name":"py-api-template",
    "env":"local",
    "running_time":13.42814
}
```

## Ideas clave
- El contenedor empaqueta la aplicación FastAPI y sus dependencias.
- El script usa uv directamente para lanzar uvicorn.

## 6. Buenas prácticas y recursos adicionales

### Objetivo
Ahora que ya sabes cómo crear y ejecutar contenedores, es importante conocer algunas buenas prácticas para trabajar de forma eficiente y evitar problemas comunes.

---

### 1. Organización de imágenes y etiquetas
- Usa nombres descriptivos y etiquetas (`tags`) claros para identificar versiones.  
  Ejemplo:

  ```bash
  docker build -t miapp:1.0 .
  ```
- Evita usar solo latest, ya que puede causar confusión si la imagen cambia.

2. Uso de .dockerignore
Crea un archivo .dockerignore en el mismo directorio que tu Dockerfile para excluir archivos innecesarios (logs, cache, venv, etc.).
Esto reduce el tamaño de la imagen y acelera la construcción.

Ejemplo de .dockerignore:

```bash
__pycache__/
*.pyc
*.log
.env
.vscode/
```

3. Minimizar el tamaño de las imágenes
Usa imágenes base ligeras (por ejemplo python:3.12-slim en lugar de python:3.12).

Elimina archivos temporales y caches después de instalar dependencias:

```bash
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
```
Evita instalar dependencias que no necesitas en producción.

4. Separar desarrollo y producción
Durante el desarrollo puedes usar volúmenes para montar tu código y probar cambios rápidamente.

En producción, genera una imagen más cerrada, con el código incluido dentro de la imagen y sin exponer volúmenes.

Usa variables de entorno para configurar el comportamiento sin modificar la imagen.

5. Seguridad básica
No ejecutes contenedores como root si no es necesario.

Mantén tus imágenes actualizadas.

Descarga imágenes solo de fuentes confiables (Docker Hub oficial u organizaciones verificadas).

6. Debugging: cómo inspeccionar contenedores
Cuando algo falla, Docker ofrece varias herramientas útiles:

Ver logs de un contenedor

```bash
docker logs <id_o_nombre>
```

Útil para revisar la salida de tu aplicación.

Ejecutar un comando dentro de un contenedor

```bash
docker exec -it <id_o_nombre> bash
```
Permite abrir una shell dentro del contenedor y revisar su estado.

Inspeccionar configuración completa de un contenedor

```bash
docker inspect <id_o_nombre>
```
Devuelve información en JSON (puertos, volúmenes, variables de entorno, etc.).

Ver recursos consumidos

```bash
docker stats
```
Muestra uso de CPU, RAM y red en tiempo real.

7. Recursos para seguir aprendiendo
Documentación oficial de Docker

- Play with Docker – laboratorio online gratuito para practicar.
- FastAPI Docs – documentación oficial de FastAPI.
- UV – Astral – documentación de UV, herramienta para entornos Python.
- Docker Hub – repositorio público de imágenes listas para usar.

## Idea clave
- Usar buenas prácticas desde el inicio hace que tus proyectos sean más portables, seguros y fáciles de mantener.
- Además, conocer los comandos de debugging básicos te ayudará a resolver problemas rápidamente.

---

## 7. Uso de Docker Compose

### Objetivo
Coordinar múltiples servicios con **Docker Compose**.  
Ejemplo: una aplicación FastAPI que guarda y lee datos desde Redis.

---

### 1. ¿Qué es Docker Compose?
Docker Compose es una herramienta que permite definir aplicaciones multi-contenedor en un archivo YAML.  
En lugar de ejecutar varios comandos `docker run`, puedes declarar tus servicios y cómo se conectan entre sí en un solo archivo.

---

### 2. Ejemplo práctico: FastAPI + Redis

#### Paso 1: Código de la aplicación
Crea un archivo `app.py` con este contenido:

```python
from fastapi import FastAPI
import redis
import os

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/set/{key}/{value}")
def set_value(key: str, value: str):
    r.set(key, value)
    return {"message": f"Key {key} set with value {value}"}

@app.get("/get/{key}")
def get_value(key: str):
    value = r.get(key)
    if value:
        return {"key": key, "value": value}
    return {"error": f"Key {key} not found"}
```
Esta app permite guardar y obtener valores en Redis usando rutas HTTP.

Paso 2: Dockerfile de la app
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Dependencias básicas
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Instalar uv (Astral)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Copiar aplicación
COPY app.py /app/app.py

# Instalar dependencias de Python
RUN uv pip install fastapi uvicorn redis

# Exponer puerto
EXPOSE 5000

# Ejecutar con uv
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]

```
Paso 3: Crear docker-compose.yml
```yaml
version: "3.9"

services:
  web:
    build: .
    container_name: fastapi_app
    ports:
      - "8080:5000"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis

  redis:
    image: redis:7
    container_name: redis_db
    ports:
      - "6379:6379"
```
Paso 4: Levantar la aplicación
Ejecuta en la carpeta del proyecto:

```bash

docker-compose up --build
```
Esto levantará:

fastapi_app → aplicación FastAPI.

redis_db → servicio Redis.

Paso 5: Probar la aplicación
Guardar un valor:

```bash
http://localhost:8080/set/mykey/helloworld
```
Respuesta:

```json
{"message": "Key mykey set with value helloworld"}
```
Recuperar el valor:

```bash
http://localhost:8080/get/mykey
```
Respuesta:

```json
{"key": "mykey", "value": "helloworld"}
```
3. Comandos útiles de Docker Compose
Levantar servicios (construir si es necesario):

```bash
docker-compose up --build
```
Detener y eliminar contenedores:

```bash
docker-compose down
```
Ver logs de todos los servicios:

```bash
docker-compose logs -f
```
Listar servicios en ejecución:

```bash
docker-compose ps
```
## Idea clave
- Con Docker Compose es muy sencillo definir múltiples servicios y conectarlos entre sí.
- En este ejemplo, con un solo comando levantamos una aplicación FastAPI y un Redis listos para usarse en conjunto.