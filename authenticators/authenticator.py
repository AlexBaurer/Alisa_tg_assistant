import typing as t
from enum import Enum

from clients.client import BaseClient
from controller import Controller


class BaseAuthenticator:
    def __init__(self, controller: Controller):
        self.controller = controller
        self.registered = False

    async def _authenticate(self) -> t.AsyncGenerator:
        raise NotImplementedError

    async def authenticate(self) -> t.AsyncGenerator:
        auth_gen = self._authenticate()
        async for step in auth_gen:
            value = yield step
            await auth_gen.asend(value)

        if not self.registered:
            raise RuntimeError('Client is not registered!')

    async def register(self, client: BaseClient):
        # TODO придумать интерфейс контроллера
        # self.controller.register(client)
        pass


class RequestType(Enum):
    ...


class Request:
    def __init__(self, request_type: RequestType, message: str):
        self.type = request_type
        self.message = message
