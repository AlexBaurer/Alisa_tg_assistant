import typing as t
from enum import Enum

from clients.client import BaseClient
from controller import Controller


class BaseAuthenticator:
    def __init__(self, controller: Controller):  # TODO нужен тут вообще контроллер?
        self.controller = controller
        self.registered = False
