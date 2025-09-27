from src.presentation.dependencies.container import Container
from src.application.dto.repository_dto import SaveKeyRequest, ValueResponse, GetKeyRequest, DeleteKeyResponse
from typing import Any
import json


def controller_on_message_handler(
    client: Any, 
    topic: str, 
    payload: bytes, 
    container: Container,
    qos: int = 0,
    properties: Any = None, 
):
    try:
        payload_json = json.loads(payload.decode())
        route = topic.split("/")[-1]
        if route == "SAVE":
            save_key_use_case = container.get_save_key_use_case()
            save_key_use_case.execute(SaveKeyRequest(key=payload_json["key"], value=payload_json["value"]))
            print("Key saved: ", payload_json["key"])
        elif route == "DELETE":
            delete_key_use_case = container.get_delete_key_use_case()
            delete_key_use_case.execute(GetKeyRequest(key=payload_json["key"]))
            print("Key deleted: ", payload_json["key"])
    except Exception as e:
        print(e)
    