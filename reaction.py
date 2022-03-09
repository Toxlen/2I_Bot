from ast import Try
from distutils.log import error
import os
from unittest import expectedFailure
import discord
from emoji import EMOJI_DATA

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN'] 

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.author.id == 426027258092978176:
        emoji = '\N{WINKING FACE}'
        await message.add_reaction(emoji)
        return

    for car in message.content:
        if car in EMOJI_DATA:
            try:
                await message.add_reaction(car)
            except Exception as e:
                print(e.text)
                return

client.run(TOKEN)
