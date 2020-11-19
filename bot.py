#!/usr/bin/python3

import os
import json
import discord
import typing # C'est pour si on veut faire des argument non obligatoire
import asyncio
from datetime import datetime
import datetime as dt

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

    devoirs = getDevoirs()

    toAppend = {"name" : matiere, "value" : description, "date" : date.isoformat()}
    devoirs["fields"].append(toAppend)

    setDevoirs(devoirs)
    
    date_str = date.strftime("%d/%m/%Y")
    response = f"J'ajoute le devoir de {matiere} pour le {date_str} vous serez prevenus la veille ! \nVous pouvez également voir la liste des devoirs en tapant !devoirs"
    await ctx.send(response)
# Gestion des erreur de la commande add
@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.ConversionError) :
        await ctx.send("Fait attention au format de la date !")
    else :
        await ctx.send("Ca n'a pas marché dû à une erreur interne, veuillez contacter le dévellopeur ...")
        print(error)

# Supprimer un devoir du fichier .json par son indice
@bot.command(help="Supprimer un devoir de la liste par son indice")
async def rm(ctx, numero: int):

    devoirs = getDevoirs()
    
    try:
        del(devoirs["fields"][numero])
    except IndexError:
        raise commands.BadArgument

    setDevoirs(devoirs)

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
    devoirsPrets = {}

    if parameter == "-m":
        if description != "":
            devoirsPrets = devoirsParMatiere(matiere=description)
            
            if devoirsPrets["fields"] == []:
                devoirsPrets["title"] = "Les devoirs en " + description
                devoirsPrets["description"] = "Pas de devoirs en cette matière ! YOUPI !!"
        else:
            devoirsPrets = devoirsParMatiere()
            
    elif parameter == "-d":
        devoirsPrets = devoirsParDate()
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
async def my_background_task():
    await bot.wait_until_ready()
    aujourdhui = datetime.now()
    guild = discord.utils.get(bot.guilds, name=GUILD)
    for channel in guild.channels:
        if channel.name == "devoirs":
            channelFinal = channel

    while not bot.is_closed():
        aujourdhui = datetime.now()
        if aujourdhui.hour == 18 and aujourdhui.minute == 30:
            devoirsPrets = {}

            aujourdhui = aujourdhui + dt.timedelta(days=1)
            devoirsPrets = devoirsParDate(laDate=aujourdhui)
            
            miseEnForme = discord.Embed.from_dict(devoirsPrets)
            await channelFinal.send("@everyone", embed= miseEnForme)

        if aujourdhui.hour == 12 and aujourdhui.minute == 0:
            devoirsPrets = {}

            aujourdhui = aujourdhui + dt.timedelta(days=1)
            devoirsPrets = devoirsParDate(laDate=aujourdhui)
            
            miseEnForme = discord.Embed.from_dict(devoirsPrets)
            await channelFinal.send("@everyone", embed= miseEnForme)
        
        if aujourdhui.hour == 8 and aujourdhui.minute == 0:
            devoirsPrets = {}

            devoirsPrets = devoirsParDate(laDate=aujourdhui)
            
            miseEnForme = discord.Embed.from_dict(devoirsPrets)
            await channelFinal.send("@everyone", embed= miseEnForme)

        await asyncio.sleep(60) # task runs every 60 seconds

bot.loop.create_task(my_background_task())
bot.run(TOKEN)
