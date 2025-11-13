from typing import Annotated
from fastapi import FastAPI
from pydantic import BaseModel, AfterValidator
from datetime import datetime


def validate_names(name: str) -> str:
    if not name:
        raise ValueError(f"{name} can't be an empty string")

    if name[0].upper() != name[0]:
        raise ValueError(f"{name} does't start with an upper case letter")

    for char in name:
        if not ("А" <= char <= "Я" or "а" <= char <= "я" or char in ("Ё", "ё")):
            raise ValueError(f"{name} must contain only cyrillic characters")

    return name


class Request(BaseModel):
    surname: Annotated[str, AfterValidator(validate_names)]
    name: Annotated[str, AfterValidator(validate_names)]
    birth_date: datetime
    phone_number: str
    email: str


app = FastAPI()


@app.post("/save")
def handle_client_request(request: Request):
    try:
        save_file(request)
    except Exception as e:
        return {"error": e}

    return {"result": "ok"}


def save_file(request: Request) -> None:
    print(request.model_dump_json)
    with open("request.txt", "w") as f:
        f.write(request.model_dump_json())
