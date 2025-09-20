from abc import ABC, abstractmethod
from turtle import st

class IStorageInterface(ABC):
    @abstractmethod
    def save(self, key: str, value: str) -> None:
        pass
    
    @abstractmethod
    def get(self, key: str) -> str:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass
