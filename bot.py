import os
import json
# import typing # C'est pour si on veut faire des argument non obligatoire et pour le moment c'est plus le cas
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

    devoirs = ""

    with open("devoirs.json", "r") as myfile:
        devoirs = json.load(myfile)

    with open("devoirs.json", "w") as myfile:
        toAppend = {"name" : matiere, "value" : description, "date" : date.isoformat()}
        devoirs["fields"].append(toAppend)
        print(devoirs)
        myfile.write(json.dumps(devoirs))
    
    date_str = date.strftime("%d/%m/%Y")
    response = f"J'ajoute le devoir de {matiere} pour le {date_str} vous serez prevenue la veille ! \nVous pouvez également voir la liste des devoirs en tapant !devoirs"
    await ctx.send(response)

@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.ConversionError) :
        await ctx.send("Fait attention au format de la date !")


bot.run(TOKEN)