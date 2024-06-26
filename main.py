import json
import logging.config
from typing import Any
import discord
from dotenv import dotenv_values
import logging

with open ('logging_config.json') as fp:
    config = json.load(fp)

logging.config.dictConfig(config)
logger = logging.getLogger('main')
ds_logger = logging.getLogger('discord')


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
