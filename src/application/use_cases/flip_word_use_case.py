from src.application.dto.flip_word_dto import FlipWordRequest, FlipWordResponse

class FlipWordUseCase:
    async def execute(self, request: FlipWordRequest) -> FlipWordResponse:
        return FlipWordResponse(word=request.word[::-1])