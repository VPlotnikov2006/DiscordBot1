from dataclasses import dataclass
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

@dataclass
class SelectionConfig:
    limit: int = 10
    pattern: str = r'.*'
    use_reactions: bool = False
    append: bool = False
    delete: bool = False

class SelectionConverter(commands.Converter):
    async def convert(self, ctx, arg: str) -> SelectionConfig:
        config = SelectionConfig()

        for key, value in map(lambda x: x.split('='), arg.split()):
            match key:
                case 'limit':
                    config.limit = int(value)
                case 'pattern':
                    if value[0] == value[-1] and value[0] in ('\'', '\"'):
                        config.pattern = value[1:-1]
                    else:
                        config.pattern = value
                case 'append':
                    config.append = value.lower() == 'true'
                case 'use_reactions':
                    config.use_reactions = value.lower() == 'true'
                case 'delete':
                    config.delete = value.lower() == 'true'
                case _:
                    logger.warning('Wrong key/value pair: (%s, %s)', key, value)
        return config


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
        async def select(ctx: commands.Context, *, config: SelectionConverter = SelectionConfig()):
            logger.debug('Selecting with config: %s', config)
            message = ctx.message
            logger.info('Selecting from: %s/%s', message.channel.guild, message.channel)
            await message.delete()
            messages = ctx.history(limit=None)
            msg_set = set()
            async for msg in messages:
                if fullmatch(config.pattern, msg.content):
                    logger.info('Selected: %s', message_to_string(msg))
                    if config.use_reactions:
                        await msg.add_reaction('✅')
                    if config.delete:
                        logger.info('Deleted: %s', message_to_string(msg))
                        if msg in self.selected_messages:
                            self.selected_messages.remove(msg)
                        await msg.delete()
                    msg_set.add(msg)

                if len(msg_set) == config.limit: 
                    break
            
            if not config.delete:
                if config.append:
                    self.selected_messages.update(msg_set)
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
