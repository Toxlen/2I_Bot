#!/usr/bin/python3

import os
import discord
import typing # C'est pour si on veut faire des argument non obligatoire
import asyncio
from datetime import datetime
import datetime as dt
from random import random, choice

from discord.ext import commands

from functions import *

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']
GUILD = os.environ['DISCORD_GUILD']
CHANNEL = int(os.environ['DISCORD_CHANNEL'])

bot = commands.Bot(command_prefix='!')

tgGifs = ["https://tenor.com/view/lotr-ring-no-isildur-lord-of-the-rings-gif-5743603", "https://tenor.com/view/no-bugs-bunny-nope-gif-14359850", "https://tenor.com/view/cdi-super-mario-no-turn-around-gif-13643447", "https://tenor.com/view/ohhh-whoah-gif-14206432", "https://tenor.com/view/antm-americas-next-top-model-miss-j-j-alexander-omg-gif-3720930", "https://tenor.com/view/anime-punch-fight-slam-wall-gif-5012110", "https://tenor.com/view/cheh-sheh-orge-sumerien-gif-20238938", "https://tenor.com/view/cat-cats-cat-reaction-cat-react-cat-what-gif-17596807", "https://tenor.com/view/umm-confused-blinking-okay-white-guy-blinking-gif-7513882", "https://tenor.com/view/pedro-monkey-puppet-meme-awkward-gif-15268759", "https://tenor.com/view/vieux-old-man-gif-20005208", "https://tenor.com/view/ferme-ta-gueule-ta-gueule-ferme-la-ftg-tg-gif-5034362", "https://tenor.com/view/my-hero-acadamia-deku-excited-head-desk-wiggling-gif-5497470"]

alerteSemainePro = ["4:18:30", "5:12:0", "6:18:30"]
alerteDemain = ["0:18:30", "1:18:30", "2:18:30", "3:18:30"]
alerteAujourdhui = ["0:8:0", "1:8:0", "2:8:0", "3:8:0", "4:8:0", "5:8:0"]


# Gestion des bans de la commande
def bannedList(ctx):
    for role in ctx.author.roles:
        if role.id == 885425513865306112:
            return False
    return True

# Coroutine appelé après chaque commandes (permet ici de supprimer le message de commande sauf pour les commandes add, rm et ping)
@bot.after_invoke
async def after_invoke_cmd(ctx):
    if(ctx.command.name not in ["add", "md", "rm", "ping", "extract"]):
        await ctx.message.delete()


# ========================================================
# Test du ping pong
@bot.command(name='ping', help="Répond pong")
async def ping(ctx):
    response = "pong"
    await ctx.send(response)


# ========================================================
# Camioned
@bot.command(name='camioned', help="Un camion qui se baladait sur une toile toile toile")
async def camioned(ctx):
    response = "https://camioned.fr/"
    await ctx.send(response)


# ========================================================
# Gwened
@bot.command(name='gwened', help="Gweno momento")
async def gwened(ctx):
    response = "https://gwened.fr/"
    await ctx.send(response)


# ========================================================
# Amogus
@bot.command(name='amogus', help="sus")
async def amogus(ctx, nb : typing.Optional[int] = 1):
    if nb < 1:
        response = "https://cdn.discordapp.com/attachments/777292703801147402/961635920078077952/reverseamogus.png"
        nb = -nb
    else:
        response = "https://amogus.org/amogus.png"

    if nb > 20:
        nb = 20

    for i in range(0,nb):
        await ctx.send(response)


# ========================================================
# Sugoma
@bot.command(name='sugoma', help="sus")
async def sugoma(ctx, nb : typing.Optional[int] = 1):
    if nb < 1:
        response = "https://cdn.discordapp.com/attachments/777292703801147402/961638400581054475/flipreverseamogus.png"
        nb = -nb
    else:
        response = "https://cdn.discordapp.com/attachments/777292703801147402/961638400874663966/flipamogus.png"

    if nb > 20:
        nb = 20

    for i in range(0,nb):
        await ctx.send(response)


# ========================================================
# Ajouter les devoirs dans le .json des devoirs
@bot.command(
    name='add',
    help="""
    Ajoute des devoirs dans la liste de devoirs
    Il faut préciser :
        - la date au format JJ/MM ou JJ/MM/AA
        - la matière en un mot
        - puis une description de la longueur souhaité""")
async def add(ctx, date: str, matiere: str, *, description):

    date = dateFormating(date)

    if date == None:
        raise commands.BadArgument

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
    if isinstance(error, commands.BadArgument) :
        await ctx.send("Fait attention au format de la date !")
    if isinstance(error, commands.CheckFailure) :
        await ctx.send("Tu crois pouvoir faire quoi toi ?")
    if isinstance(error, commands.CommandError) :
        await ctx.send("Ca n'a pas marché dû à une erreur interne, veuillez contacter le développeur ...")
        print(datetime.now().time(), error)
# Gestion des bans de la commande add
add.add_check(bannedList)


# ========================================================
# Ajouter les devoirs dans le .json des devoirs
@bot.command(
    name='md',
    help="""
    Modifie des devoirs dans la liste de devoirs.
    La commande prend obligatoirement en argument l'indice du devoir à modifier.
    Puis soit on utilise les modificateurs précis soit on entre le devoir commme avec la comande add.
    Les modificateur :
        - -d [DATE] : Pour modifier la date
        - -m [MATIERE] : Pour modifier la matière
        - -e [DESCRIPTION] : Pour modifier la description""")
async def md(ctx, indice: int, arg1: typing.Optional[str] = "", arg2: typing.Optional[str] = "", *, description: typing.Optional[str] = ""):
    devoirs = getDevoirs()
    toModify = {}
    response = ""

    try:
        toModify = devoirs["fields"][indice]
    except IndexError:
        raise commands.BadArgument

    if arg1 == "-d":
        # Modification de la date du devoir
        date = dateFormating(arg2)

        if date == None:
            raise commands.BadArgument

        response = "La date à été modifier de **" + datetime.fromisoformat(toModify["date"]).strftime("%d/%m/%Y")

        toModify["date"] = date.isoformat()

        response += "** à la date suivante **" + datetime.fromisoformat(toModify["date"]).strftime("%d/%m/%Y") + "**\n"

    elif arg1 == "-m":
        # Modification de la matière du devoir
        response = "La matière à été modifié de **" + toModify["name"]

        toModify["name"] = arg2

        response += "** à la matière suivante **" + toModify["name"] + "**\n"

    elif arg1 == "-e":
        # Modification de l'explication/description du devoir
        response = "La description à été modifié de **" + toModify["value"]

        toModify["value"] = arg2 + " " + description

        response += "** à la description suivante **" + toModify["value"] + "**\n"

    else:
        # Modifiction de tout
        date = dateFormating(arg1)

        if date == None:
            raise commands.BadArgument

        response = "Le devoir à été modifié de *" + datetime.fromisoformat(toModify["date"]).strftime("%d/%m/%Y") + " : " + toModify["name"] + " : " + toModify["value"]

        toModify["date"] = date.isoformat()
        toModify["name"] = arg2
        toModify["value"] = description

        response += "* au devoir suivant *" + datetime.fromisoformat(toModify["date"]).strftime("%d/%m/%Y") + " : " + toModify["name"] + " : " + toModify["value"] + "*"

    devoirs["fields"][indice] = toModify

    setDevoirs(devoirs)

    response += "Vous pouvez également voir la liste des devoirs en tapant !devoirs"
    await ctx.send(response)
# Gestion des erreur de la commande md
@md.error
async def md_error(ctx, error):
    if isinstance(error, commands.BadArgument) :
        await ctx.send("Fait attention au format de la date ou a l'index du devoir !")
    if isinstance(error, commands.CheckFailure) :
        await ctx.send("Tu crois pouvoir faire quoi toi ?")
    if isinstance(error, commands.CommandError) :
        await ctx.send("Ca n'a pas marché dû à une erreur interne, veuillez contacter le développeur ...")
        print(datetime.now().time(), error)
# Gestion des bans de la commande md
md.add_check(bannedList)


# ========================================================
# Supprimer un devoir du fichier .json par son indice
@bot.command(
    help="""
    Supprimer un devoir de la liste par son indice
    Attention l'indice commence à 0, en négatif part de la fin, on est des devs ou pas ?""")
async def rm(ctx, indice: int):


    devoirs = getDevoirs()

    try:
        del(devoirs["fields"][indice])
    except IndexError:
        raise commands.BadArgument

    setDevoirs(devoirs)

    response = f"Je supprime le devoir n°{indice} de la liste ! \nVous pouvez également voir la liste des devoirs en tapant !devoirs"
    await ctx.send(response)
# Gestion des erreur de la commande rm
@rm.error
async def rm_error(ctx, error):
    if isinstance(error, commands.BadArgument) :
        await ctx.send("Cette indice de devoir n'existe pas (ça commence à 0) !")
    if isinstance(error, commands.CheckFailure) :
        await ctx.send("Tu crois pouvoir faire quoi toi ?")
    if isinstance(error, commands.CommandError) :
        await ctx.send("Ca n'a pas marché du à une erreur interne, veuillez contacter le développeur ...")
        print(datetime.now().time(), error)
# Gestion des bans de la commande rm
rm.add_check(bannedList)

# ========================================================
# Afficher les devoirs à faire
@bot.command(
    help="""
    Permet d'afficher les devoirs à faire.
    Ils sont trié par date par défaut mais il peuvent être trié par matière avec le modificatieur -m.
    Il est également possible d'afficher que les devoirs d'une matière en précisant la matière derrière le modificateur -m.""")
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
    if isinstance(error, commands.CommandError):
        await ctx.send("Ca n'a pas marché du à une erreur interne, veuillez contacter le développeur ...")
        print(datetime.now().time(), error)

# ========================================================
# Tache de vérification régulière
@bot.event
async def my_background_task():
    await bot.wait_until_ready()
    # guild = discord.utils.get(bot.guilds, name=GUILD)
    # for channel in guild.channels:
    #     if channel.name == "devoirs":
    #         channelFinal = channel
    channelFinal = bot.get_channel(CHANNEL)

    while not bot.is_closed():
        aujourdhui = datetime.now()

        # Suppression des devoirs passés
        if (aujourdhui.hour == 0 and aujourdhui.minute == 1):
            devoirs = getDevoirs()
            modif = False
            cpt = 0
            for devoir in devoirs["fields"]:
                if datetime.fromisoformat(devoir["date"]).date() < aujourdhui.date():
                    del(devoirs["fields"][cpt])
                    modif = True
                cpt += 1

            if modif:
                setDevoirs(devoirs)

        aujourdhuiToTest = str(aujourdhui.weekday()) + ":" + str(aujourdhui.hour) + ":" + str(aujourdhui.minute)

        # Alerte pour le jour même :
        if aujourdhuiToTest in alerteAujourdhui:
            devoirsPrets = {}
            devoirsPrets["title"] = "Voilà les devoirs pour aujourd'hui"

            devoirsPrets = devoirsParDate(laDate=aujourdhui)
            if devoirsPrets["fields"] != []:
                miseEnForme = discord.Embed.from_dict(devoirsPrets)
                if random() < 0.001:
                    await channelFinal.send("@everyone", embed= miseEnForme)
                else:
                    await channelFinal.send("@tout_le_monde", embed= miseEnForme)

        # Alerte des devoirs pour le lendemain :
        elif aujourdhuiToTest in alerteDemain:
            devoirsPrets = {}
            aujourdhui = aujourdhui + dt.timedelta(days=1)
            devoirsPrets["title"] = "Voilà les devoirs pour demain"

            devoirsPrets = devoirsParDate(laDate=aujourdhui)
            if devoirsPrets["fields"] != []:
                miseEnForme = discord.Embed.from_dict(devoirsPrets)
                if random() < 0.001:
                    await channelFinal.send("@everyone", embed= miseEnForme)
                else:
                    await channelFinal.send("@tout_le_monde", embed= miseEnForme)

        # Alerte des devoirs pour le lundi :
        elif aujourdhuiToTest in alerteSemainePro:
            devoirsPrets = {}
            aujourdhui = aujourdhui + dt.timedelta(days= 7 - aujourdhui.weekday())
            devoirsPrets["title"] = "Voilà les devoirs pour la semaine prochaine"

            for i in range(0,4):
                aujourdhui = aujourdhui + dt.timedelta(days=1)
                devoirsPrets += devoirsParDate(laDate=aujourdhui)
            if devoirsPrets["fields"] != []:
                miseEnForme = discord.Embed.from_dict(devoirsPrets)
                if random() < 0.001:
                    await channelFinal.send("@everyone", embed= miseEnForme)
                else:
                    await channelFinal.send("@tout_le_monde", embed= miseEnForme)

        else:
            if random() < 0.00005:
                randomEmoji = [":kissing_heart:", ":flushed:", ":wink:", ":smirk:", ":rolling_eyes:", ":hot_face:", ":yawning_face:", ":face_vomiting:", ":mechanic_tone4:", ":pinching_hand:", ":person_gesturing_no:", ":kiss_mm:", ":couple_mm:", ":frog:", ":full_moon_with_face:", ":sweat_drops:", ":peach:", ":eggplant:", ":brown_square:", ":flag_af:"]
                await channelFinal.send(choice(randomEmoji))

        await asyncio.sleep(60) # task runs every 60 seconds

# ========================================================
# Commande pour process l'image jointe et en extraire le texte
import pytesseract
import re
import requests

def dowloadImage(src, dest):
    response = requests.get(src)
    if not response.ok:
        raise commands.BadArgument(message="Failed to donwload image")

    img_data = response.content
    with open(dest, 'wb') as handler:
        handler.write(img_data)

@bot.command(
    help="""
    Permet d'extraire le texte d'une image
    La langue d'interprétation est de base en français mais peut être changé en une autre avec l'argument [LANG].
    Liste des langues dispo : """ + str(pytesseract.get_languages(config='')))
async def extract(ctx, parameter: typing.Optional[str] = "fra"):
    if parameter not in pytesseract.get_languages(config=''):
        raise commands.BadArgument

    if ctx.message.reference:
        original = await ctx.fetch_message(id=ctx.message.reference.message_id)

        if len(original.attachments) == 0:
            urlRe = re.search("(?P<url>https?://[^\s]+)", original.content)
            if urlRe is None:
                await ctx.send("Pas d'image dans ce message")
                return

            url = urlRe.group("url")
            if not url.endswith([".png", ".jpg", ".jpeg"]) :
                await ctx.send("Le lien ne fait pas référence à une image supporté")
                return

            async with ctx.typing():
                filename = url.split("/").pop()
                pathToImage = "./images/" + filename
                dowloadImage(url, pathToImage)
                text = pytesseract.image_to_string(pathToImage, lang=parameter)
                os.remove(pathToImage)
                await ctx.send("```" + text.strip() + "```")
            return
        elif len(ctx.message.attachments) > 1:
            await ctx.send("Trop d'images dans ce message !")
            return

        if original.attachments[0].content_type in ["image/jpeg", "image/png"]:
            async with ctx.typing():
                pathToImage = "./images/" + original.attachments[0].filename
                await original.attachments[0].save(pathToImage)
                text = pytesseract.image_to_string(pathToImage, lang=parameter)
                os.remove(pathToImage)
                await ctx.send("```" + text.strip() + "```")
            return

    if len(ctx.message.attachments) == 0:
        urlRe = re.search("(?P<url>https?://[^\s]+)", parameter)
        if urlRe is None :
            await ctx.send("Pas d'image dans ce message")
            return

        url = urlRe.group("url")
        if not url.endswith([".png", ".jpg", ".jpeg"]) :
            await ctx.send("Le lien ne fait pas référence à une image supporté")
            return

        async with ctx.typing():
            filename = url.split("/").pop()
            pathToImage = "./images/" + filename
            dowloadImage(url, pathToImage)
            text = pytesseract.image_to_string(pathToImage, lang=parameter)
            os.remove(pathToImage)
            await ctx.send("```" + text.strip() + "```")
        return

    elif len(ctx.message.attachments) > 1:
        # plusieurs liens
        # re.findall(r'(https?://[^\s]+)', myString)

        ctx.send("Bro attend le fait d'envoyer plusieurs photos n'est pas encore implémenté !")
        return

    if ctx.message.attachments[0].content_type in ["image/jpeg", "image/png"]:
        async with ctx.typing():
            pathToImage = "./images/" + ctx.message.attachments[0].filename
            await ctx.message.attachments[0].save(pathToImage)
            text = pytesseract.image_to_string(pathToImage, lang=parameter)
            os.remove(pathToImage)
            await ctx.send("```" + text.strip() + "```")
        return

# Gestion des erreur de la commande devoirs
@extract.error
async def devoirs_error(ctx, error):
    if isinstance(error, commands.BadArgument) :
        await ctx.send("Tu as mal écris la commande !\n", error.message)
    if isinstance(error, commands.CommandError) :
        await ctx.send("Ca n'a pas marché du à une erreur interne, veuillez contacter le développeur ...")
        print(datetime.now().time(), error)

if __name__ == "__main__":
    bot.loop.create_task(my_background_task())
    print(datetime.now().time(), "Let's get started !")
    bot.run(TOKEN)
