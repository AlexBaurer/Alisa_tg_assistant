import asyncio
from tg_client import create_client


class Controller:

    def __init__(self):
        pass

    async def reg_user(self, user_phone):
        user_phone = user_phone
        app = create_client(user_phone=user_phone)

        async with app:
            await app.start()
            await app.send_code(user_phone)
            await app.stop()


controller = Controller()
