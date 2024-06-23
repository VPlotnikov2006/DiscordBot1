import discord
import pandas as pd
from dotenv import dotenv_values
from re import fullmatch


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        # await self.change_presence(status=discord.Status.invisible)
    
    async def on_message(self, message: discord.Message):
        if (mtch := fullmatch(r'!fetch\s?([\d]*)', message.content)):
            await message.delete()
            limit = int(mtch.groups()[0]) if mtch.groups()[0] else 10
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

    client = MyClient(intents=intents)
    client.run(config['API_TOKEN'])
