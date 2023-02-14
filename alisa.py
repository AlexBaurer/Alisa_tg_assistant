from fastapi import FastAPI
from pydantic import BaseModel


class Request(BaseModel):
    request: dict


class Response(BaseModel):
    response: dict
    version: str


app = FastAPI()


@app.post('/')
def alisa_post(request: Request):
    response = Response(response={'text': 'hi', "end_session": False}, version='1.0')
    print(request)
    print(response)
    return response
