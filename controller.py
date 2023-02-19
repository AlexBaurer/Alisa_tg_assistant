from clients.telegram import TelegramClient, create_client
from client_db import create_user


class Controller:
    def __init__(self):
        self.phone_code = None
        self.client: TelegramClient | None = None

    async def phone_handle(self, user_phone):
        self.client = await create_client(user_phone)
        create_user(self.client, self.client.get_me(), )

    async def code_handle(self, phone_code):
        if self.client:
            await self.client.sign_in_by_code(phone_code)

    async def alisa_request_handler(self, request):
        if request:
            return [message async for message in self.client.get_dalogs('me')]


controller = Controller()
