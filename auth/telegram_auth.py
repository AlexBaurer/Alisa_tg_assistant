import dataclasses
import typing as t
from collections import defaultdict

from settings import settings
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

import client_db
from authenticators.telegram import TelegramAuthenticator
from controller import controller


app = Client("auth_bot", api_id=settings.api_id, api_hash=settings.api_hash,
             bot_token=settings.bot_token)


def state_filter(state):
    async def func(flt, _, message):
        return users_context[message.from_user.id].state == flt.state
    return filters.create(func, state=state)


@dataclasses.dataclass
class UserContext:
    state: str = 'unknown'
    auth: TelegramAuthenticator | None = None
    other: dict = dataclasses.field(default_factory=dict)


# TODO надо обмазать локами
users_context: [int, UserContext] = defaultdict(lambda: UserContext())


def user_context(func):
    def wrapper(client, message):
        context = users_context[message.from_user.id]
        return func(client, message, context)
    return wrapper


def contact_request():
    return {
        'text': 'Для регистрации предоставьте данные аккаунта',
        'reply_markup': ReplyKeyboardMarkup(
                [[KeyboardButton('Предоставить контакты', request_contact=True)]],
                resize_keyboard=True
            )
    }


@app.on_message(filters.text & state_filter('unknown'))
@user_context
async def start(_, message, context):
    user = client_db.get_user(telegram_user_id=message.from_user.id)
    if not user:
        user = client_db.create_user(telegram_user_id=message.from_user.id)
    client = controller.get_client(user.id)
    if not client:
        auther = controller.get_client_authenticator('telegram')
        context.auth = auther(controller)
        await message.reply(**contact_request())
        context.state = 'sent_contact'
    else:
        await message.reply(text='Вы авторизованы.')


@app.on_message(filters.contact & state_filter('sent_contact'))
@user_context
async def handle_contact(_, message, context: UserContext):
    await context.auth.create_client(message.contact.phone_number)
    await message.reply(text='Введите полученный код')

    context.state = 'sent_code'


@app.on_message(state_filter('sent_code'))
@user_context
async def handle_code(_, message: Message, context: UserContext):
    # TODO проверка что это код
    signed_in_client = await context.auth.authorize_client(message.text)
    controller.add_client(signed_in_client)
    context.state = 'unknown'
