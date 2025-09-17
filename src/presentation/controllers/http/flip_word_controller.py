from fastapi import APIRouter
from src.presentation.dependencies.container import Container


def get_flip_word_controller(container: Container) -> APIRouter:
    router = APIRouter()

    @router.post("/flip-word")
    async def flip_word(request: dict):
        return await container.get_flip_word_use_case().execute(word=request["word"])

    return router