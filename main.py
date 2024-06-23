from typing import Any
import discord
import pandas as pd
from discord.ext import commands
from dotenv import dotenv_values
from re import fullmatch


class MyClient(commands.Bot):
    def __init__(self, **options: Any) -> None:
        intents = discord.Intents.default()

        intents.message_content = True
        intents.messages = True

        intents.guild_messages = True
        intents.guilds = True

        super().__init__(command_prefix='!', intents=intents, **options)

        @self.command(name='fetch')
        async def fetch(ctx, limit=10):
            message = ctx.message
            await message.delete()
            print(f'Last {limit} messages in {message.channel.guild}/{message.channel}')
            async for msg in client.get_partial_messageable(message.channel.id).history(limit=limit):
                print(msg.content)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.change_presence(status=discord.Status.invisible)
        

if __name__ == "__main__":
    config = dotenv_values('.env')

    client = MyClient()
    client.run(config['API_TOKEN'])
