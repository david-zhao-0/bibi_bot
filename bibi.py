import os
import asyncio
import discord
from discord.ext import commands
import json
from loguru import logger
import traceback

TOKEN = os.environ['BIBI_BOT_TOKEN']

def get_server_prefix(client, message):
    with open('serverprefixes.json', 'r') as file:
        prefix = json.load(file)

    return prefix[str(message.guild.id)]

client = commands.Bot(command_prefix=get_server_prefix, intents=discord.Intents.all())

@client.event
async def on_ready():
    logger.info('Bot online!')

@client.event
async def on_guild_join(guild):
    with open('serverprefixes.json', 'r') as file:
        prefix = json.load(file)

    prefix[str(guild.id)] = 'b!'

    with open('serverprefixes.json', 'w') as file:
        json.dump(prefix, file, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('serverprefixes.json', 'r') as file:
        prefix = json.load(file)

    prefix.pop(str(guild.id))

    with open('serverprefixes.json', 'w') as file:
        json.dump(prefix, file, indent=4)

async def load_extensions():
    logger.info('Loading extensions...')
    for fname in os.listdir('./cogs'):
        if fname.endswith(".py"):
            try:
                await client.load_extension(f'cogs.{fname[:-3]}')
                logger.info(f'{fname} loaded!')
            except Exception as error:
                logger.error(f'Error loading [ {fname} ]')
                traceback.print_exception(type(error), error, error.__traceback__)
            
async def main():
    async with client:
        await load_extensions()
        await client.start(TOKEN)

asyncio.run(main())