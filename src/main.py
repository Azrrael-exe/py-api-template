from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from src.presentation.dependencies.container import Container
from src.presentation.controllers.http.health_check_controller import get_health_check_controller
from src.presentation.controllers.http.flip_word_controller import get_flip_word_controller


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
    
    yield
    
    # Código de limpieza - se ejecuta al cerrar la aplicación
    print("🛑 Cerrando aplicación...")
    
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
        reload=True
    )


if __name__ == "__main__":
    main()
