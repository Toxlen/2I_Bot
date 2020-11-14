import os
import typing
from datetime import datetime

from discord.ext import commands
from dotenv import load_dotenv

from functions import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.command(name='ping', help="Répond pong")
async def ping(ctx):
    response = "pong"
    await ctx.send(response)

@bot.command(name='add', help="Ajoute des devoirs dans la liste de devoirs")
async def add(ctx, date: str, matiere: str, *, description):
    date = dateFormating(date)

    if date == None:
        raise commands.ConversionError

    

    date_str = date.strftime("%d/%m/%Y")
    response = f"J'ajoute le devoir de {matiere} pour le {date_str} vous serez prevenue la veille ! \nVous pouvez également voir la liste des devoirs en tapant !devoirs"
    await ctx.send(response)

@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.ConversionError) :
        await ctx.send("Fait attention au format de la date !")


bot.run(TOKEN)