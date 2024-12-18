import pyrogram
from pyrogram import Client
from pyrogram import raw
from pyrogram.types import User

from clients.client import BaseClient
from settings import settings


async def create_client(user_phone=None):
    client = TelegramClient('client', api_id=settings.api_id, api_hash=settings.api_hash,
                            phone_number=user_phone, test_mode=False)
    await client.connect()
    # await client.authorize()
    return client


class TelegramClient(Client, BaseClient):
    # TODO вынести клиент пирограма в self._client
    def __init__(self, *args, **kwargs):
        self.sent_code = ''
        super().__init__(*args, **kwargs)

    async def start(self):
        try:
            if not await self.storage.is_bot() and self.takeout:
                self.takeout_id = (await self.invoke(raw.functions.account.InitTakeoutSession())).id

            await self.invoke(raw.functions.updates.GetState())
        except (Exception, KeyboardInterrupt):
            await self.disconnect()
            raise
        else:
            self.me = await self.get_me()
            await self.initialize()

            return self

    # async def sign_in_by_code(self, phone_code):
    #     signed_in = await self.sign_in(self.phone_number, self.sent_code.phone_code_hash, phone_code)
    #     await self.start()
    #     await self.send_message('me', 'hui')
    #     async for dialog in self.get_dialogs():
    #         print(dialog.chat.title or dialog.chat.first_name)

