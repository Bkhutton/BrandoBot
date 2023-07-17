# Author : Brandon Hutton
# Date : April 17th, 2020
# Description: Random discord bot to play music and have fun commands

# Imports
import os
import discord
import shutil
import asyncio

from os import path
from dotenv import load_dotenv
from discord.ext import commands

# Load the environmental variables
load_dotenv()

# Sets DISCORD TOKEN from .env file
TOKEN = os.getenv('DISCORD_TOKEN')

# Sets command prefix to '!'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Loads commands
async def load_extensions():
    await bot.load_extension("app.admin.commands.admin")
    await bot.load_extension("app.musicbot.commands.music")
    await bot.load_extension("app.admin.commands.emily")

"""
Ready Event:
    Params: None
    Description: Creates a directory for all the songs to be downloaded to
"""
@bot.event
async def on_ready():
    if(not path.exists("music/")):
        os.mkdir("music/")
    print(f'{bot.user.name} has connected to Discord!')

"""
Disconnect Event:
    Params: None
    Description: Deletes all the old music from the music directory
"""
@bot.event
async def on_disconnect():
    shutil.rmtree("music/")
    os.mkdir("music/")
    print(f'{bot.user.name} has disconnected.')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())
