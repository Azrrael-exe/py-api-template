from fastapi import APIRouter

from src.presentation.dependencies.container import Container


def get_health_check_controller(container: Container) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    async def health_check():
        return await container.get_health_check_use_case().execute()

    return router
