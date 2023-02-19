from typing import AsyncGenerator

from authenticators.authenticator import BaseAuthenticator, Request, RequestType
from controller import Controller
from clients.telegram import create_client


class TelegramRequestType(RequestType):
    PHONE_NUMBER = 'request_phone_number'
    PHONE_CODE = 'request_phone_code'


class TelegramAuthenticator(BaseAuthenticator):
    def __init__(self, controller: Controller, phone_number: str | None = None):
        self._phone_number = phone_number
        self._phone_code = None
        self._client = None
        self._sent_code = None
        super().__init__(controller)

    @property
    def phone_number(self):
        if not self._phone_number:
            raise ValueError('Phone NUMBER must be set. Use set_phone(phone_number).')
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number: str):
        # TODO проверять правильность телефона?
        if phone_number is None:
            raise ValueError('phone_number must be str. Use auth.asend(phone_number)')
        self._phone_number = phone_number

    @property
    def phone_code(self):
        if not self._phone_code:
            raise ValueError('Phone CODE must be set. Use set_code(code).')
        return self._phone_code

    @phone_code.setter
    def phone_code(self, phone_code: str):
        if phone_code is None:
            raise ValueError('phone_code must be str. Use auth.asend(phone_code)')
        self._phone_code = phone_code

    async def _authenticate(self) -> AsyncGenerator:
        self.phone_number = yield Request(TelegramRequestType.PHONE_NUMBER, 'Введите номер телефона: ')

        self._client = await create_client()
        self._sent_code = await self._client.send_code(self.phone_number)

        self.phone_code = yield Request(TelegramRequestType.PHONE_CODE, 'Введите КОД полученный от Телеграмм: ')
        await self.sign_in()

    async def sign_in(self):
        await self._client.sign_in(self.phone_number, self._sent_code.phone_code_hash, self.phone_code)
        await self._client.start()
