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
    
    if message.author.id == 426027258092978176:
        emoji = '\N{WINKING FACE}'
        await message.add_reaction(emoji)
        return


client.run(TOKEN)
