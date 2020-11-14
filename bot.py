import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.command(name='ping', help="Répond pong")
async def ping(ctx):
    response = "pong"
    await ctx.send(response)

@bot.command(name='add', help="Ajoute des devoirs dans la liste de devoirs")
async def add(ctx,arg):
    response = f"J'ajoute le devoir {arg}"
    await ctx.send(response)

bot.run(TOKEN)