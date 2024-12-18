from clients.client import BaseClient
# from clients.telegram import TelegramClient, create_client
# from client_db import create_user


class Controller:
    def __init__(self):
        self.client_name_to_auth: dict = dict()
        self.user_id_to_client: dict[int, BaseClient] = dict()

    def register_authenticator(self, name, auther):
        self.client_name_to_auth[name] = auther

    def get_client_authenticator(self, client_name):
        return self.client_name_to_auth[client_name]

    def get_client(self, user_id):
        return self.user_id_to_client.get(user_id)

    def add_client(self, user_id, client):
        self.user_id_to_client[user_id] = client


controller = Controller()
