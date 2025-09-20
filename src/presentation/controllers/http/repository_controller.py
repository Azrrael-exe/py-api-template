from fastapi import APIRouter, HTTPException
from src.presentation.dependencies.container import Container
from src.application.dto.repository_dto import SaveKeyRequest, ValueResponse, GetKeyRequest, DeleteKeyResponse


def get_repository_controller(container: Container) -> APIRouter:
    router = APIRouter()

    @router.post("/repository", response_model=ValueResponse)
    async def save_key(request: SaveKeyRequest) -> ValueResponse:
        """Save a key-value pair to the repository."""
        return container.get_save_key_use_case().execute(request=request)

    @router.get("/repository/{key}", response_model=ValueResponse)
    async def get_key(key: str) -> ValueResponse:
        """Get a value by key from the repository."""
        try:
            request = GetKeyRequest(key=key)
            return container.get_get_key_use_case().execute(request=request)
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Key '{key}' not found")

    @router.delete("/repository/{key}", response_model=DeleteKeyResponse)
    async def delete_key(key: str) -> DeleteKeyResponse:
        """Delete a key-value pair from the repository."""
        try:
            request = GetKeyRequest(key=key)
            return container.get_delete_key_use_case().execute(request=request)
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Key '{key}' not found")

    return router
