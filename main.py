import json
import logging.config
from typing import Any
import discord
from discord.ext import commands
from dotenv import dotenv_values
from re import fullmatch
import logging

with open ('logging_config.json') as fp:
    config = json.load(fp)

logging.config.dictConfig(config)
logger = logging.getLogger('main')
ds_logger = logging.getLogger('discord')

def message_to_string(msg):
    return f'{msg.created_at:%Y-%m-%d %H:%M:%S}/{msg.author}: {msg.content}'

def messages_to_string(messages, *, sep='\n'):
    return sep.join(map(message_to_string, messages))

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
        logger.debug('Bot created')
        intents = discord.Intents.default()

        intents.message_content = True
        intents.messages = True

        intents.guild_messages = True
        intents.guilds = True

        self.selected_messages = set()

        super().__init__(command_prefix='!', intents=intents, **options)

        @self.command(name='select')
        async def select(ctx: commands.Context, *, config: SelectionConverter = {'limit': 10,'pattern': r'.*','use_reactions': False,'append': False}):
            logger.debug('Selecting with config: %s', config)
            message = ctx.message
            logger.info('Selecting from: %s/%s', message.channel.guild, message.channel)
            await message.delete()
            messages = ctx.history(limit=None)
            msg_set = set()
            async for msg in messages:
                if fullmatch(config['pattern'], msg.content):
                    logger.info('Selected: %s', message_to_string(msg))
                    msg_set.add(msg)
                if len(msg_set) == config['limit']: 
                    break
            

            if config['append']:
                self.selected_messages.union(msg_set)
            else:
                self.selected_messages = msg_set
            
            logger.debug('Storage: %s', messages_to_string(self.selected_messages, sep=' | '))
            
            

    async def on_ready(self):
        logger.info('Logged on as %s!', self.user)
        await self.change_presence(status=discord.Status.invisible)


if __name__ == "__main__":
    config = dotenv_values('.env')

    client = MyClient()
    client.run(config['API_TOKEN'], log_handler=None)
