import os
import typing
from datetime import datetime

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
async def add(ctx, date: str):
    if isFormat(date,"%d/%m/%y"):
        date_devoir = datetime.strptime(date,"%d/%m/%y")
    elif isFormat(date,"%d-%m-%y"):
        date_devoir = datetime.strptime(date,"%d-%m-%y")
    elif isFormat(date,"%d/%m"):
        date_devoir = datetime.strptime(date,"%d/%m")
        date_devoir.replace(year=datetime.now().year)
    elif isFormat(date,"%d-%m"):
        date_devoir = datetime.strptime(date,"%d-%m")
        date_devoir.replace(year=datetime.now().year)
    else :
        raise commands.BadArgument

    date_devoir_str = date_devoir.strftime("%d/%m/%Y")
    response = f"J'ajoute le devoir {date_devoir_str}"
    await ctx.send(response)

@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.BadArgument) :
        await ctx.send("Fait attention au format de la date !")

def isFormat(date, format):
    try:
        if date != datetime.strptime(date, format).strftime(format):
            raise ValueError
        return True
    except ValueError:
        return False


bot.run(TOKEN)