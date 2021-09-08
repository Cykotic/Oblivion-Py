# NAME: Oblivion
# DATE: Thursday 14, March 2019
# Started: 8/12/20 (REWRITTEN PY VERSION)
# OWNER: CYKOTIC
# PROJECT STATUS: ( WORKING )

# Public or Private: (PUBLIC)


# sub classes are mad fucking retarted. 
# group classes are fucking retarted too 

import asyncio
import json
import os
from pathlib import Path  # For paths

import discord
from discord.ext import commands
from discoutils import MinimalEmbedHelp

# Local code
import utils.dbloader
from utils.mongo import Document
import motor.motor_asyncio

# credit to octii
try:
    with open('settings/settings.json') as configFile:
        config = json.load(configFile)
        token = config['token']
except Exception as e:
    print(e)

async def get_prefix(bot, message):
    # If dm's
    if not message.guild:
        return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)

intents = discord.Intents.default()
intents.members = True
DEFAULTPREFIX = ">"
# prefix command basically were the command prefix shit coming from.
bot = commands.Bot(
    command_prefix=get_prefix,
    case_insensitive=True,
    intents=intents,
    help_command=MinimalEmbedHelp()
    )

# Defining a few things
cwd = Path(__file__).parents[0]
cwd = str(cwd)
secret_file = utils.dbloader.read_json('settings')
bot.connection_url = secret_file["mongo"]
bot.DEFAULTPREFIX = DEFAULTPREFIX
bot.blacklisted_users = []

# ready event and reading the stats for the bot pretty self explaintory
@bot.event
async def on_ready():
    print(f"Loaded: [{bot.user.name}]")
    print(f"Servers: [{str(len(bot.guilds))}]")
    print(f"Command Loaded: [{len(bot.commands)}]")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(len(bot.guilds))} servers | >help"))
    # bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    # bot.db = bot.mongo["cykotic"]
    # bot.config = Document(bot.db, "config")
    # bot.command_usage = Document(bot.db, "command_usage")
    # bot.reaction_roles = Document(bot.db, "reaction_roles")
    # print("Initialized Database\n-----")


@bot.event
async def on_message(message):

    # Ignore messages sent by yourself
    if message.author.bot:
        return

    # A way to blacklist users from the bot by not processing commands
    # if the author is in the blacklisted_users list
    if message.author.id in bot.blacklisted_users:
        return

    # Whenever the bot is tagged, respond with its prefix
    if message.content.startswith(f"<@!{bot.user.id}>") and len(message.content) == len(
        f"<@!{bot.user.id}>"
    ):
        data = await bot.config.get_by_id(message.guild.id)
        if not data or "prefix" not in data:
            prefix = bot.DEFAULTPREFIX
        else:
            prefix = data["prefix"]
            embed = discord.Embed(
                title = f"My prefix here is `{prefix}`",
                color = 0xff7700
            )
            await message.channel.send(embed=embed, delete_after=15)

    await bot.process_commands(message)

    if message.content.startswith('F.'):
        await message.channel.send("has paid respects!")
    if message.content.startswith('gn'):
        await message.channel.send("Goodnight ❤️🌙")
    if message.content.startswith('gm'):
        await message.channel.send("Goodmorning 🌞")
    if message.content.startswith('maul.'):
        await message.channel.send("Maullll")
    if message.content.startswith('jo.'):
        await message.channel.send("Maullll")



if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")



# token reading in the config file
bot.run(token, bot=True, reconnect=True)
