import os
import discord

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
    emoji = '\N{WINKING FACE}'
    await message.add_reaction(emoji)


client.run(TOKEN)
