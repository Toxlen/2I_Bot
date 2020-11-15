import os
import json
import discord
import typing # C'est pour si on veut faire des argument non obligatoire
import asyncio
from datetime import datetime

from discord.ext import commands

from functions import *

TOKEN = os.environ['DISCORD_TOKEN'] 
GUILD = os.environ['DISCORD_GUILD'] 

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

    toAppend = {"name" : matiere, "value" : description, "date" : date.isoformat()}
    devoirs["fields"].append(toAppend)

    with open("devoirs.json", "w") as myfile:
        myfile.write(json.dumps(devoirs))
    
    date_str = date.strftime("%d/%m/%Y")
    response = f"J'ajoute le devoir de {matiere} pour le {date_str} vous serez prevenue la veille ! \nVous pouvez également voir la liste des devoirs en tapant !devoirs"
    await ctx.send(response)
# Gestion des erreur de la commande add
@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.ConversionError) :
        await ctx.send("Fait attention au format de la date !")
    else :
        await ctx.send("Ca n'a pas marché du à une erreur interne, veuillez contacter le dévellopeur ...")
        print(error)

# Supprimer un devoir du fichier .json par son indice
@bot.command(help="Supprimer un devoir de la liste par son indice")
async def rm(ctx, numero: int):

    devoirs = ""

    with open("devoirs.json", "r") as myfile:
        devoirs = json.load(myfile)
    
    try:
        del(devoirs["fields"][numero])
    except IndexError:
        raise commands.BadArgument

    with open("devoirs.json", "w") as myfile:
        myfile.write(json.dumps(devoirs))

    response = f"Je supprime le devoir n°{numero} de la liste ! \nVous pouvez également voir la liste des devoirs en tapant !devoirs"
    await ctx.send(response)
# Gestion des erreur de la commande rm
@rm.error
async def rm_error(ctx, error):
    if isinstance(error, commands.BadArgument) :
        await ctx.send("Cette indice de devoir n'existe pas (ça commence à 0) !")
    else :
        await ctx.send("Ca n'a pas marché du à une erreur interne, veuillez contacter le dévellopeur ...")
        print(error)
    

# Afficher les devoirs à faire
@bot.command(help="Permet d'afficher les devoirs à faire")
async def devoirs(ctx, parameter: typing.Optional[str] = "-d", *, description: typing.Optional[str] = "" ):
    devoirs = ""
    with open("devoirs.json", "r") as myfile:
        devoirs = json.load(myfile)
    devoirsPrets = {"title": devoirs["title"], "color": 16711680, "fields": []}

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
            
            if devoirsPrets["fields"] == []:
                devoirsPrets["title"] = "Les devoirs en " + description
                devoirsPrets["description"] = "Pas de devoirs en cette matière ! YOUPI !!"
        else:
            i = 0
            for element in devoirs["fields"]:
                date = datetime.fromisoformat(element["date"])
                date_str = date.strftime("%d/%m/%Y")
                toAppend = {"name": devoirs["fields"][i]["name"], "value": devoirs["fields"][i]["value"] + " pour le " + date_str}
                devoirsPrets["fields"].append(toAppend)
                i += 1
            
    elif parameter == "-d":
        i = 0
        for element in devoirs["fields"]:
            date = datetime.fromisoformat(element["date"])
            date_str = date.strftime("%d/%m/%Y")
            toAppend = {"name": date_str + " : " + element["name"], "value": element["value"]}
            devoirsPrets["fields"].append(toAppend)
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
        print(error)

@bot.event
async def my_background_task(self):
    await self.wait_until_ready()
    aujourdhui = datetime.now()
    guild = discord.utils.get(bot.guilds, name=GUILD)
    for channel in guild.channels:
        if channel.name == "devoirs":
            channelFinal = channel

    while not self.is_closed():
        aujourdhui = datetime.now()
        if aujourdhui.hour == 11 and aujourdhui.minute == 0:
            devoirs = ""
            with open("devoirs.json", "r") as myfile:
                devoirs = json.load(myfile)
            devoirsPrets = {"title": "Devoirs pour demain", "color": 16711680, "fields": []}

            i = 0
            for element in devoirs["fields"]:
                date = datetime.fromisoformat(element["date"])
                if date.day - 1 == aujourdhui.day:
                    date_str = date.strftime("%d/%m/%Y")
                    toAppend = {"name": date_str + " : " + element["name"], "value": element["value"]}
                    devoirsPrets["fields"].append(toAppend)
                i += 1
            
            miseEnForme = discord.Embed.from_dict(devoirsPrets)
            await channelFinal.send("@everyone", embed= miseEnForme)
        
        if aujourdhui.hour == 7 and aujourdhui.minute == 0:
            devoirs = ""
            with open("devoirs.json", "r") as myfile:
                devoirs = json.load(myfile)
            devoirsPrets = {"title": "Devoirs pour aujourd'hui", "color": 16711680, "fields": []}

            i = 0
            for element in devoirs["fields"]:
                date = datetime.fromisoformat(element["date"])
                if date.day  == aujourdhui.day:
                    date_str = date.strftime("%d/%m/%Y")
                    toAppend = {"name": date_str + " : " + element["name"], "value": element["value"]}
                    devoirsPrets["fields"].append(toAppend)
                i += 1
            
            miseEnForme = discord.Embed.from_dict(devoirsPrets)
            await channelFinal.send("@everyone", embed= miseEnForme)

        print("je me suis réveillé et je me rendors pour 1min")
        await asyncio.sleep(60) # task runs every 60 seconds

bot.run(TOKEN)
