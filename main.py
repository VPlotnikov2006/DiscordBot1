from typing import Any
import discord
from discord.ext import commands
from dotenv import dotenv_values
from re import fullmatch


def print_messages(msg_list):
    for msg in msg_list:
        print(f'{msg.created_at:%Y-%m-%d %H:%M:%S}/{msg.author}: {msg.content}')

class SelectionConverter(commands.Converter):
    async def convert(self, ctx, arg: str):
        base_dict = {
            'limit': 10,
            'pattern': r'.*',
            'use_reactions': False,
            'append': False,
        }

        for key, value in map(lambda x: x.split('='), arg.split()):
            base_dict[key] = value
        
        base_dict['limit'] = int(base_dict['limit'])
        base_dict['append'] = base_dict['append'] in (True, 'True')
        base_dict['use_reactions'] = base_dict['use_reactions'] in (True, 'True')
        return base_dict


class MyClient(commands.Bot):
    def __init__(self, **options: Any) -> None:
        intents = discord.Intents.default()

        intents.message_content = True
        intents.messages = True

        intents.guild_messages = True
        intents.guilds = True

        self.selected_messages = []

        super().__init__(command_prefix='!', intents=intents, **options)

        @self.command(name='select')
        async def select(ctx: commands.Context, *, config: SelectionConverter = {'limit': 10,'pattern': r'.*','use_reactions': False,'append': True}):
            print(config)
            print('Storage: ')
            print_messages(self.selected_messages)
            message = ctx.message
            await message.delete()
            messages = ctx.history(limit=None)
            msg_list = []
            async for msg in messages:
                if fullmatch(config['pattern'], msg.content):
                    msg_list.append(msg)
                if len(msg_list) == config['limit']: 
                    break
            
            
            print(f'Last {config['limit']} messages in {message.channel.guild}/{message.channel} requiring {config['pattern']}')
            print_messages(msg_list)
            
            if config['append']:
                self.selected_messages += msg_list
            else:
                self.selected_messages = msg_list
            
            

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.change_presence(status=discord.Status.invisible)
        

if __name__ == "__main__":
    config = dotenv_values('.env')

    client = MyClient()
    client.run(config['API_TOKEN'])
