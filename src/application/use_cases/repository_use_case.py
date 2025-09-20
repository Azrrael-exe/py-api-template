from src.domain.interfaces.storeage_interface import IStorageInterface
from src.application.dto.repository_dto import SaveKeyRequest, ValueResponse, GetKeyRequest, DeleteKeyResponse

class SaveKeyUseCase:
    def __init__(self, storage: IStorageInterface):
        self._storage = storage

    def execute(self, request: SaveKeyRequest) -> ValueResponse:
        self._storage.save(request.key, request.value)
        return ValueResponse(key=request.key, value=request.value)


class GetKeyUseCase:
    def __init__(self, storage: IStorageInterface):
        self._storage = storage

    def execute(self, request: GetKeyRequest) -> ValueResponse:
        key = request.key
        value = self._storage.get(key)
        return ValueResponse(key=request.key, value=value)

class DeleteKeyUseCase:
    def __init__(self, storage: IStorageInterface):
        self._storage = storage

    def execute(self, request: GetKeyRequest) -> DeleteKeyResponse:
        key = request.key
        value = self._storage.get(key)
        self._storage.delete(request.key)
        return DeleteKeyResponse(key=request.key, value=value, is_deleted=True)