from pydantic import BaseModel

class SaveKeyRequest(BaseModel):
    key: str
    value: str

class ValueResponse(BaseModel):
    key: str
    value: str

class GetKeyRequest(BaseModel):
    key: str

class DeleteKeyResponse(BaseModel):
    key: str
    value: str
    is_deleted: bool