import asyncio
from settings import settings
from pyrogram import Client


def create_client(user_phone):
    return Client('client', api_id=settings.api_id, api_hash=settings.api_hash, in_memory=True,
                  phone_number=user_phone)







