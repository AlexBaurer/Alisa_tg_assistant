from fastapi import FastAPI
from pydantic import BaseModel

from client_db import get_user
from controller import controller


class User(BaseModel):
    user_id: str
    access_token: str


class Session(BaseModel):
    message_id: str
    session_id: str
    skill_id: str
    user: User


class Request(BaseModel):
    request: dict
    session: Session


class Response(BaseModel):
    response: dict
    version: str = '1.0'


app = FastAPI()


@app.post('/')
async def alisa_post(request: Request):
    print(request)
    # print(response)
    if user := get_user(request.session.user.user_id) is not None:
        dialogs = await controller.alisa_request_handler(user)
        response = Response(response={
            'text': f'Последние диалоги: {", ".join(d for d in dialogs)}', "end_session": False
        })
    else:
        code = 234  # TODO генерировать код
        response = Response(response={'text': f"Шагай авторизовываться. Код: {code}", "end_session": False})
    return response


if __name__ == '__main__':
    print('GOOOOOO!!')
    import uvicorn
    from controller import controller
    from tg_auth import app as telegram_auth

    telegram_auth.start()
    uvicorn.run("alisa:app", host="127.0.0.1", port=8000, log_level="info")
