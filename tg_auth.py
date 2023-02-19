import dataclasses
import typing as t
from collections import defaultdict

from authenticators.authenticator import Request
from settings import settings
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

from authenticators.telegram import TelegramAuthenticator, TelegramRequestType
from controller import controller


app = Client("auth_bot", api_id=settings.api_id, api_hash=settings.api_hash,
             bot_token=settings.bot_token)


def state_filter(state):
    async def func(flt, _, message):
        # print(user_states)
        return users_context.get(message.from_user.id).state == flt.state
    return filters.create(func, state=state)


@dataclasses.dataclass
class UserContext:
    state: str = 'unknown'
    auth: t.AsyncGenerator | None = None
    other: dict = dataclasses.field(default_factory=dict)


# TODO надо обмазать локами
users_context: [int, UserContext] = defaultdict(lambda: UserContext())
# user_auths: dict[int, t.AsyncGenerator] = {}


def contact_request():
    return {
        'text': 'Для регистрации предоставьте данные аккаунта',
        'reply_markup': ReplyKeyboardMarkup(
                [[KeyboardButton('Предоставить контакты', request_contact=True)]],
                resize_keyboard=True
            )
    }


@app.on_message(filters.text & state_filter('unknown'))
async def start(_, message):
    auth = TelegramAuthenticator(controller).authenticate()
    users_context[message.from_user.id].auth = auth
    await message.reply(**contact_request())
    users_context[message.from_user.id].state = 'sent_contact'


@app.on_message(filters.contact)
async def handle_contact(client, message):
    auth = users_context[message.from_user.id].auth
    req: Request = await auth.asend(None)  # Начинаем аутентификацию

    if req.type == TelegramRequestType.PHONE_NUMBER:
        next_req = await auth.asend(message.contact.phone_number)
        users_context[message.from_user.id].other['auth_request'] = next_req

        await message.reply(text='Введите полученный код')
        users_context[message.from_user.id].state = 'sent_code'
    else:
        await message.reply(**contact_request())


@app.on_message(state_filter('sent_code'))
async def handle_code(client, message: Message):
    auth = users_context[message.from_user.id].auth
    req: Request = users_context[message.from_user.id].other['auth_request']
    if req.type == TelegramRequestType.PHONE_CODE:
        await auth.asend(message.text)
