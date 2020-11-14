import os
import json
import discord
import typing # C'est pour si on veut faire des argument non obligatoire
from datetime import datetime

from discord.ext import commands
from dotenv import load_dotenv

from functions import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

# Test du ping pong
@bot.command(name='ping', help="Répond pong")
async def ping(ctx):
    response = "pong"
    await ctx.send(response)

# Ajouter les devoirs dans le .json des devoirs
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
        myfile.write(json.dumps(devoirs))
    
    date_str = date.strftime("%d/%m/%Y")
    response = f"J'ajoute le devoir de {matiere} pour le {date_str} vous serez prevenue la veille ! \nVous pouvez également voir la liste des devoirs en tapant !devoirs"
    await ctx.send(response)
# Gestion des erreur de la commande add
@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.ConversionError) :
        await ctx.send("Fait attention au format de la date !")

# Afficher les devoirs à faire
@bot.command(help="Permet d'afficher les devoirs à faire")
async def devoirs(ctx, parameter: typing.Optional[str] = "-m", *, description: typing.Optional[str] = "" ):
    devoirs = ""
    devoirsPrets = {"title": "", "color": 16711680, "fields": []}
    with open("devoirs.json", "r") as myfile:
        devoirs = json.load(myfile)

    if parameter == "-m":
        if description != "":
            i = 0
            for element in devoirs["fields"]:
                if element["name"].lower() == description.lower():
                    date = datetime.fromisoformat(element["date"])
                    date_str = date.strftime("%d/%m/%Y")
                    toAppend = {"name": devoirs["fields"][i]["name"], "value": devoirs["fields"][i]["value"] + " pour le " + date_str}
                    devoirsPrets["fields"].append(toAppend)
                    devoirsPrets["title"] = "Les devoirs en " + devoirs["fields"][i]["name"]
                i += 1

        else:
            i = 0
            for element in devoirs["fields"]:
                date = datetime.fromisoformat(element["date"])
                date_str = date.strftime("%d/%m/%Y")
                devoirsPrets["fields"][i]["value"] = devoirs["fields"][i]["value"] + " pour le " + date_str
                i += 1
            
    elif parameter == "-d":
        i = 0
        for element in devoirs["fields"]:
            date = datetime.fromisoformat(element["date"])
            date_str = date.strftime("%d/%m/%Y")
            devoirsPrets["fields"][i]["name"] = date_str + " : " + devoirs["fields"][i]["name"]
            i += 1
    else:
        raise commands.BadArgument
        
    miseEnForme = discord.Embed.from_dict(devoirsPrets)
    await ctx.send(embed= miseEnForme)
# Gestion des erreur de la commande devoirs
@devoirs.error
async def devoirs_error(ctx, error):
    if isinstance(error, commands.BadArgument) :
        await ctx.send("Tu as mal écris la commande !")
    else :
        await ctx.send("Ca n'a pas marché du à une erreur interne, veuillez contacter le dévellopeur ...")


bot.run(TOKEN)