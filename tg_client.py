import asyncio
import pyrogram
from settings import settings
from pyrogram import Client
from pyrogram.types import User


async def create_client(user_phone):
    client = TgClient('client', api_id=settings.api_id, api_hash=settings.api_hash,
                      phone_number=user_phone)
    await client.connect()
    await client._authorize()
    return client


class TgClient(Client):

    def __init__(self, *args, **kwargs):
        self.sent_code = ''
        super().__init__(*args, **kwargs)

    async def _authorize(self) -> User:
        if self.bot_token:
            return await self.sign_in_bot(self.bot_token)

        sent_code = await self.send_code(self.phone_number)
        self.sent_code = sent_code

    async def sign_in_by_code(self, phone_code):
        signet_in = await self.sign_in(self.phone_number, self.sent_code.phone_code_hash, phone_code)
        await self.start()
        print(signet_in)




