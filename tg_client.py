import asyncio
import pyrogram
from settings import settings
from pyrogram import Client
from pyrogram.types import User
from pyrogram import raw


async def create_client(user_phone):
    client = TgClient('client', api_id=settings.api_id, api_hash=settings.api_hash,
                      phone_number=user_phone, test_mode=True)
    await client.connect()
    await client.authorize()
    return client


class TgClient(Client):

    def __init__(self, *args, **kwargs):
        self.sent_code = ''
        super().__init__(*args, **kwargs)

    async def authorize(self) -> User:
        if self.bot_token:
            return await self.sign_in_bot(self.bot_token)

        sent_code = await self.send_code(self.phone_number)
        self.sent_code = sent_code

    async def start(
        self: "pyrogram.Client"
    ):
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

    async def sign_in_by_code(self, phone_code):
        signed_in = await self.sign_in(self.phone_number, self.sent_code.phone_code_hash, phone_code)
        await self.start()
        await self.send_message('me', 'hui')
        async for dialog in self.get_dialogs():
            print(dialog.chat.title or dialog.chat.first_name)




