from typing import Any
import discord
from dotenv import dotenv_values
import logging

formatter = logging.Formatter(r'%(asctime)s | %(name)s | %(levelname)s | %(message)s')

ds_file_handler = logging.FileHandler('discord.log', 'w', encoding='utf-8')
ds_file_handler.setFormatter(formatter)
ds_file_handler.setLevel(logging.INFO)

ds_stream_handler = logging.StreamHandler()
ds_stream_handler.setFormatter(formatter)
ds_stream_handler.setLevel(logging.ERROR)

ds_logger = logging.getLogger('discord')
ds_logger.addHandler(ds_file_handler)
ds_logger.addHandler(ds_stream_handler)
ds_logger.setLevel(logging.DEBUG)


stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('main.log', 'w', encoding='utf-8')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


class MyClient(discord.Client):
    def __init__(self, **options: Any) -> None:
        logger.debug('Bot created')
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(intents=intents, **options)

    async def on_ready(self):
        logger.info('Logged on as %s!', self.user)
        await self.change_presence(status=discord.Status.invisible)
    
    async def on_message(self, message: discord.Message):
        logger.info('Message handled: %s', message.content)


if __name__ == "__main__":
    config = dotenv_values('.env')

    client = MyClient()
    client.run(config['API_TOKEN'], log_handler=None)
