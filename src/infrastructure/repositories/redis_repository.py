import redis
import logging
from src.domain.interfaces.storeage_interface import IStorageInterface

logger = logging.getLogger(__name__)

class RedisRepository(IStorageInterface):
    """
    Implementación de IStorageInterface usando Redis como backend de almacenamiento.
    """
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, 
                 decode_responses: bool = True, **kwargs):
        """
        Inicializa la conexión a Redis.
        
        Args:
            host: Dirección del servidor Redis
            port: Puerto del servidor Redis
            db: Número de base de datos Redis
            decode_responses: Si decodificar respuestas como strings
            **kwargs: Argumentos adicionales para redis.Redis()
        """
        try:
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=decode_responses,
                **kwargs
            )
            # Verificar conexión
            self.client.ping()
            logger.info(f"Conectado exitosamente a Redis en {host}:{port}")
        except redis.ConnectionError as e:
            logger.error(f"Error conectando a Redis: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado conectando a Redis: {e}")
            raise
    
    def save(self, key: str, value: str) -> None:
        """
        Guarda un valor en Redis con la clave especificada.
        
        Args:
            key: Clave bajo la cual guardar el valor
            value: Valor a guardar
            
        Raises:
            redis.RedisError: Si hay error en la operación Redis
        """
        try:
            result = self.client.set(key, value)
            if not result:
                raise redis.RedisError(f"Falló al guardar clave '{key}'")
            logger.debug(f"Guardado exitosamente: {key}")
        except redis.RedisError as e:
            logger.error(f"Error guardando clave '{key}': {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado guardando clave '{key}': {e}")
            raise redis.RedisError(f"Error inesperado: {e}")
    
    def get(self, key: str) -> str:
        """
        Obtiene un valor de Redis por su clave.
        
        Args:
            key: Clave del valor a obtener
            
        Returns:
            El valor asociado con la clave
            
        Raises:
            KeyError: Si la clave no existe
            redis.RedisError: Si hay error en la operación Redis
        """
        try:
            value = self.client.get(key)
            if value is None:
                raise KeyError(f"Clave '{key}' no encontrada en Redis")
            logger.debug(f"Obtenido exitosamente: {key}")
            return value
        except KeyError:
            raise  # Re-raise KeyError as is
        except redis.RedisError as e:
            logger.error(f"Error obteniendo clave '{key}': {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado obteniendo clave '{key}': {e}")
            raise redis.RedisError(f"Error inesperado: {e}")
    
    def delete(self, key: str) -> None:
        """
        Elimina una clave y su valor de Redis.
        
        Args:
            key: Clave a eliminar
            
        Raises:
            KeyError: Si la clave no existe
            redis.RedisError: Si hay error en la operación Redis
        """
        try:
            result = self.client.delete(key)
            if result == 0:
                raise KeyError(f"Clave '{key}' no encontrada para eliminar")
            logger.debug(f"Eliminado exitosamente: {key}")
        except KeyError:
            raise  # Re-raise KeyError as is
        except redis.RedisError as e:
            logger.error(f"Error eliminando clave '{key}': {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado eliminando clave '{key}': {e}")
            raise redis.RedisError(f"Error inesperado: {e}")
    
    def exists(self, key: str) -> bool:
        """
        Verifica si una clave existe en Redis.
        
        Args:
            key: Clave a verificar
            
        Returns:
            True si la clave existe, False en caso contrario
        """
        try:
            return bool(self.client.exists(key))
        except redis.RedisError as e:
            logger.error(f"Error verificando existencia de clave '{key}': {e}")
            raise
    
    def close(self) -> None:
        """
        Cierra la conexión a Redis.
        """
        try:
            if hasattr(self.client, 'connection_pool'):
                self.client.connection_pool.disconnect()
            logger.info("Conexión a Redis cerrada exitosamente")
        except Exception as e:
            logger.warning(f"Error cerrando conexión a Redis: {e}")
