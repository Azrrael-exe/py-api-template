from src.domain.interfaces.storeage_interface import IStorageInterface

class InMemoryStorage(IStorageInterface):
    def __init__(self):
        self._storage = {}

    def save(self, key: str, value: str) -> None:
        self._storage[key] = str(value)

    def get(self, key: str) -> str:
        return str(self._storage[key])
    
    def delete(self, key: str) -> None:
        del self._storage[key]