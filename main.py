import discord
import pandas as pd
from discord.ext import commands
from dotenv import dotenv_values
from re import fullmatch


class MyClient(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.change_presence(status=discord.Status.invisible)

    def add_commands(self):
        @self.command(name='fetch')
        async def fetch(ctx, limit=10):
            message = ctx.message
            await message.delete()
            print(f'Last {limit} messages in {message.channel.guild}/{message.channel}')
            async for msg in client.get_partial_messageable(message.channel.id).history(limit=limit):
                print(msg.content)


if __name__ == "__main__":
    config = dotenv_values('.env')
    intents = discord.Intents.default()

    intents.message_content = True
    intents.messages = True

    intents.guild_messages = True
    intents.guilds = True

    client = MyClient(command_prefix='!', intents=intents)
    client.add_commands()
    client.run(config['API_TOKEN'])
