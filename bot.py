import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

class CustomClient(discord.Client):
    async def on_ready(self):
        guild = discord.utils.get(client.guilds, name=GUILD)
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    async def on_message(message):
        if message.author == client.user:
            return
        
        if message.content == 'ping':
            response = "pong"
            await message.channel.send(response)
        
client = CustomClient()
client.run(TOKEN)