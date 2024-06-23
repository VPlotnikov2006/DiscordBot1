import discord
from dotenv import dotenv_values


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.change_presence(status=discord.Status.invisible)
    
    async def on_message(self, message: discord.Message):
        if message.author.id != self.user.id:
            await message.reply(message.content)


if __name__ == "__main__":
    config = dotenv_values('.env')
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(config['API_TOKEN'])
