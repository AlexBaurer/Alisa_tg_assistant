from authenticators.authenticator import BaseAuthenticator
from controller import Controller, controller
from clients.telegram import create_client


class TelegramAuthenticator(BaseAuthenticator):
    def __init__(self, controller: Controller, phone_number: str | None = None):
        self._phone_number = phone_number
        self._phone_code = None
        self._client = None
        self._sent_code = None
        super().__init__(controller)

    async def create_client(self, phone_number: str):
        self._phone_number = phone_number
        self._client = await create_client()
        self._sent_code = await self._client.send_code(phone_number)
        return self._client

    async def authorize_client(self, phone_code):
        await self._client.sign_in(self._phone_number, self._sent_code.phone_code_hash, phone_code)
        await self._client.start()
        return self._client


controller.register_authenticator('telegram', TelegramAuthenticator)
