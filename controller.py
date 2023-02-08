import asyncio
from tg_client import create_client


class Controller:

    def __init__(self):
        self.phone_code = None
        self.client = None

    async def phone_handle(self, user_phone):
        self.client = await create_client(user_phone)

    async def code_handle(self, phone_code):
        await self.client.sign_in_by_code(phone_code)


controller = Controller()
