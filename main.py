from typing import Any
import discord
from dotenv import dotenv_values


class MyClient(discord.Client):
    def __init__(self, **options: Any) -> None:
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(intents=intents, **options)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.change_presence(status=discord.Status.invisible)
    
    async def on_message(self, message: discord.Message):
        if message.author.id != self.user.id:
            await message.channel.send(f"{message.author.global_name} said '{message.content}'")


if __name__ == "__main__":
    config = dotenv_values('.env')
    
    client = MyClient()
    client.run(config['API_TOKEN'])
