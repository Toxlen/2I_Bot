import os
import typing
from datetime import date

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
async def add(ctx, jour: int, mois: int, annee: typing.Optional[int] = date.today().year):
    date_devoir = date(annee, mois, jour)
    date_devoir_str = date_devoir.strftime("%d/%m/%y")
    response = f"J'ajoute le devoir {date_devoir_str}"
    await ctx.send(response)

bot.run(TOKEN)