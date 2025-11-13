from typing import Annotated, Literal
from fastapi import FastAPI
from pydantic import BaseModel, AfterValidator, Field
from datetime import date, datetime


def validate_names(name: str) -> str:
    if not name:
        raise ValueError(f"{name} can't be an empty string")

    if name[0].upper() != name[0]:
        raise ValueError(f"{name} does't start with an upper case letter")

    for char in name:
        if not ("А" <= char <= "Я" or "а" <= char <= "я" or char in ("Ё", "ё")):
            raise ValueError(f"{name} must contain only cyrillic characters")

    return name


AllowedRequestReasons = Literal[
    "Нет доступа к сети", "Не работает телефон", "Не приходят письма"
]


class Request(BaseModel):
    surname: Annotated[str, AfterValidator(validate_names)]
    name: Annotated[str, AfterValidator(validate_names)]
    birth_date: date
    phone_number: str
    email: str
    reasons: list[AllowedRequestReasons] = Field(min_length=1)
    occurrence_date_time: datetime


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
