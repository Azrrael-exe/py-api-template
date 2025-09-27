from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
import json
from src.presentation.dependencies.container import Container
from src.presentation.controllers.http.health_check_controller import get_health_check_controller
from src.presentation.controllers.http.flip_word_controller import get_flip_word_controller
from src.presentation.controllers.http.repository_controller import get_repository_controller
from src.presentation.controllers.mqtt.repository_controller import controller_on_message_handler
from fastapi_mqtt.config import MQTTConfig
from fastapi_mqtt.fastmqtt import FastMQTT

fast_mqtt = FastMQTT(config=MQTTConfig(
    host="broker.hivemq.com",
    port=1883,
    keepalive=60,
))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación FastAPI.
    Se ejecuta al inicio y al final de la aplicación.
    """
    # Código de inicio - se ejecuta al iniciar la aplicación
    print("🚀 Iniciando aplicación...")
    
    # Aquí puedes agregar:
    # - Conexiones a base de datos
    # - Carga de modelos de ML
    # - Configuración de recursos compartidos
    # - Inicialización de servicios externos
    container = Container()
    app.include_router(router=get_health_check_controller(container), prefix="/api")
    app.include_router(router=get_flip_word_controller(container), prefix="/api")
    app.include_router(router=get_repository_controller(container), prefix="/api")

    print("🚀 Iniciando FastMQTT...")

    @fast_mqtt.on_connect()
    def connect(client, flags, rc, properties):
        fast_mqtt.client.subscribe("/SDA_2025/#") #subscribing mqtt topic
        print("Connected: ", client, flags, rc, properties)


    @fast_mqtt.on_message()
    async def message(client, topic, payload, qos, properties):
        print("Received message: ",topic, payload.decode(), qos, properties)
        controller_on_message_handler(client=client, topic=topic, payload=payload, container=container)

    await fast_mqtt.mqtt_startup()
    
    yield
    
    # Código de limpieza - se ejecuta al cerrar la aplicación
    print("🛑 Cerrando aplicación...")
    await fast_mqtt.mqtt_shutdown()
    
    # Aquí puedes agregar:
    # - Cierre de conexiones de base de datos
    # - Limpieza de recursos
    # - Guardado de estado
    # - Cierre de servicios externos


# Inicializar la aplicación FastAPI
app = FastAPI(
    title="py-api-template",
    description="A modern Python API template using FastAPI",
    version="0.1.0",
    lifespan=lifespan
)


def main():
    """Función principal para ejecutar el servidor"""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )


if __name__ == "__main__":
    main()
