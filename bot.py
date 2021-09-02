#!/usr/bin/python3

import os
import json
import discord
import typing # C'est pour si on veut faire des argument non obligatoire
import asyncio
from datetime import datetime
import datetime as dt
from random import random, choice

from discord.ext import commands
from discord.ext.commands.errors import ChannelNotFound

from functions import *

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN'] 
GUILD = os.environ['DISCORD_GUILD'] 
CHANNEL = int(os.environ['DISCORD_CHANNEL'])

bot = commands.Bot(command_prefix='!')

# Test du ping pong
@bot.command(name='ping', help="Répond pong")
async def ping(ctx):
    response = "pong"
    await ctx.send(response)

# Ajouter les devoirs dans le .json des devoirs
@bot.command(name='add', help="Ajoute des devoirs dans la liste de devoirs préciser la date, la matière (en un mot) puis une description")
async def add(ctx, date: str, matiere: str, *, description):
    
    date = dateFormating(date)

    if date == None:
        raise commands.CommandError()

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
    if isinstance(error, commands.CommandError) :
        await ctx.send("Fait attention au format de la date !")
    else :
        await ctx.send("Ca n'a pas marché dû à une erreur interne, veuillez contacter le dévellopeur ...")
        print(error)

# Supprimer un devoir du fichier .json par son indice
@bot.command(help="Supprimer un devoir de la liste par son indice (commence à 0, en négatif part de la fin, on est des devs ou pas)")
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
            devoirsPrets["title"] = "Les devoirs en " + description
            
            if devoirsPrets["fields"] == []:
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
    # guild = discord.utils.get(bot.guilds, name=GUILD)
    # for channel in guild.channels:
    #     if channel.name == "devoirs":
    #         channelFinal = channel
    channelFinal = bot.get_channel(CHANNEL)

    while not bot.is_closed():
        aujourdhui = datetime.now()
        if (aujourdhui.hour == 18 and aujourdhui.minute == 30) or (aujourdhui.hour == 12 and aujourdhui.minute == 0 and aujourdhui.weekday() <= 4):
            devoirsPrets = {}

            if aujourdhui.weekday() < 4 or aujourdhui.weekday() == 6:
                aujourdhui = aujourdhui + dt.timedelta(days=1)
                devoirsPrets["title"] = "Voilà les devoirs pour demain"
            elif aujourdhui.weekday() == 4:
                aujourdhui = aujourdhui + dt.timedelta(days=3)
                devoirsPrets["title"] = "Voilà les devoirs pour lundi"
            elif aujourdhui.weekday() == 5:
                aujourdhui = aujourdhui + dt.timedelta(days=2)
                devoirsPrets["title"] = "Voilà les devoirs pour lundi"
            devoirsPrets = devoirsParDate(laDate=aujourdhui)

            if devoirsPrets["fields"] != []:
                miseEnForme = discord.Embed.from_dict(devoirsPrets)
                if random() < 0.001:
                    await channelFinal.send("@everyone", embed= miseEnForme)
                else:
                    await channelFinal.send("@tout_le_monde", embed= miseEnForme)
        
        elif aujourdhui.hour == 8 and aujourdhui.minute == 0 and aujourdhui.weekday() <= 5:
            devoirsPrets = {}
            devoirsPrets["title"] = "Voilà les devoirs pour aujourd'hui"

            devoirsPrets = devoirsParDate(laDate=aujourdhui)
            if devoirsPrets["fields"] != []:
                miseEnForme = discord.Embed.from_dict(devoirsPrets)
                if random() < 0.001:
                    await channelFinal.send("@everyone", embed= miseEnForme)
                else:
                    await channelFinal.send("@tout_le_monde", embed= miseEnForme)

        else:
            if random() < 0.00005:
                randomEmoji = [":kissing_heart:", ":flushed:", ":wink:", ":smirk:", ":rolling_eyes:", ":hot_face:", ":yawning_face:", ":face_vomiting:", ":mechanic_tone4:", ":pinching_hand:", ":person_gesturing_no:", ":kiss_mm:", ":couple_mm:", ":frog:", ":full_moon_with_face:", ":sweat_drops:", ":peach:", ":eggplant:", ":brown_square:", ":flag_af:"]
                channelFinal.send(choice(randomEmoji))

        await asyncio.sleep(60) # task runs every 60 seconds

bot.loop.create_task(my_background_task())
bot.run(TOKEN)
