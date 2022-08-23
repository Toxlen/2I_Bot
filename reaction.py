import os
import discord
from emoji import EMOJI_DATA
import datetime
from random import random

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN'] 

spamJuliette = False
intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    splited = message.content.split(" ")

    if message.author == client.user:
        return
    
    if message.author.id == 426027258092978176 and spamJuliette:
        emoji = '\N{WINKING FACE}'
        await message.add_reaction(emoji)
        

    if message.author.id == 320666678021193728:
        await message.add_reaction("<:amogus:978570047821860894>")
        await message.add_reaction("<:amogus:978570068050997269>")

        if random() < 0.005:
            await message.channel.send("Deez nuts !")


    # Tentative de back door mais il trouve pas les members ...
    # if message.content == "jav inutile" and message.author.id == 251805972383793153:  
    #     guild = client.get_guild(727624920464359514)
    #     print(guild.name)
    #     print(len(guild.members))
    #     # guild.fetch_members()

    #     for member in client.get_all_members():
    #         print(member)

    #     member = discord.utils.get(guild.members, id= 320666678021193728)
    #     memmber = guild.get_member(320666678021193728)
    #     print(member)
    #     print(memmber)

        # await memmber.add_roles(727625375353405502)
        

    for car in message.content:
        if car in EMOJI_DATA:
            try:
                await message.add_reaction(car)
            except Exception as e:
                print(datetime.datetime.now().time(), e.text)
                return

    for word in splited:
        if word.startswith("<") and word.endswith(">") and word.find(":") != -1:
            await message.add_reaction(word)

@client.event
async def on_reaction_add(reaction, user):
    if client.user == user:
        return

    elif "😉" in reaction.emoji and reaction.message.author.id == 426027258092978176:
        await reaction.message.channel.send(reaction.message.author.mention + " " + user.mention + " viens de réagir à ton message : " + reaction.message.jump_url)
        
    elif reaction.custom_emoji:
        if "amogus" == reaction.emoji.name:
            await reaction.message.add_reaction("<:amogus:978570047821860894>")
            await reaction.message.add_reaction("<:amogus:978570068050997269>")

client.run(TOKEN)
