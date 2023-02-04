from settings import settings
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from controller import controller


app = Client("auth_bot", api_id=settings.api_id, api_hash=settings.api_hash, in_memory=True,
             bot_token=settings.bot_token)


@app.on_message(filters.text)
def echo(client, message):
    message.reply(text='Для регистрации предоставьте данные аккаунта', reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton('Предоставить контакты', request_contact=True)]
                ],
                resize_keyboard=True
            )
    )


@app.on_message(filters.contact)
async def handle_contact(client, message):
    user_phone = message.contact.phone_number
    await controller.reg_user(user_phone)
    await message.reply(text='Введите полученный код')


@app.on_message(filters.text)
async def handle_contact(client, message):
    confirmation_code = message


app.run()
