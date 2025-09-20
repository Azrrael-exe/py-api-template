from fastapi import APIRouter
from src.presentation.dependencies.container import Container
from src.application.dto.flip_word_dto import FlipWordRequest, FlipWordResponse


def get_flip_word_controller(container: Container) -> APIRouter:
    router = APIRouter()

    @router.post("/flip-word")
    async def flip_word(request: FlipWordRequest) -> FlipWordResponse:
        return await container.get_flip_word_use_case().execute(request=request)

    return router