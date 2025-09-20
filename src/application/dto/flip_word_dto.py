from pydantic import BaseModel

class FlipWordRequest(BaseModel):
    word: str

class FlipWordResponse(BaseModel):
    word: str