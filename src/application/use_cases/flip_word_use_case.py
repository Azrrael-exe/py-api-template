class FlipWordUseCase:
    async def execute(self, word: str) -> str:
        return word[::-1]