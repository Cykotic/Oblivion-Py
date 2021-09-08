import discord
from discord.ext import commands
import utils
from datetime import datetime

class profanity(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print(f"{self.__class__.__name__}: [Loaded]")


        @commands.command()
        async def black_list(self, ctx):
            guilds = utils.json_loader.read_json()
            for x in guilds:
                if x['id'] == ctx.guild.id:
                    sep = "\n"
                    wordList = sep.join(x['badwords'])
                    if len(wordList) < 1:
                        wordList = "*Your blacklist is empty!*"
                    embed = discord.Embed(  title = 'BadWords Blacklist',
                                            description = 'This is a list of all balcklisted words on this server. To add or remove words from the blacklist, please use the "blacklist_add" or "blacklist_remove" command (admins only)',
                                            colour= 0xff7700)
                    embed.add_field(name = "List", value = wordList)
                    await ctx.send(embed = embed)


        @commands.command()
        @commands.has_permissions(manage_messages=True)
        async def blacklist_remove(self, ctx, arg1 = None):
            guilds = utils.json_loader.read_json()
            for x in guilds:
                if x['id'] == ctx.guild.id:
                    if arg1.lower() in x['badwords']:
                        try:
                            x['badwords'].remove(arg1.lower())
                            utils.json_loader.write_json(guilds)
                            await ctx.send('`' + arg1 + '` was removed from your blacklist!')
                        except Exception as e:
                            print(e)
                    else:
                        await ctx.send("`" + arg1 + "` is not on your blacklist!")

        @commands.command()
        @commands.has_permissions(manage_messages=True)
        async def logs_on(self, ctx):
            guilds = utils.json_loader.read_json()
            for x in guilds:
                if x['id'] == ctx.guild.id:
                    if x['logs'] == 1:
                        await ctx.send('Logs already enabled! Create a channel "logs" to see them.')
                    else:
                        x['logs'] = 1
                        utils.json_loader.write_json(guilds)
                        await ctx.send('Logs enabled!')

        @commands.command()
        @commands.has_permissions(manage_messages=True)
        async def logs_off(self, ctx):
            guilds = utils.json_loader.read_json()
            for x in guilds:
                if x['id'] == ctx.guild.id:
                    if x['logs'] == 0:
                        await ctx.send('Logs already disabled!')
                    else:
                        x['logs'] = 0
                        utils.json_loader.write_json(guilds)
                        await ctx.send('Logs disabled!')

        @commands.command()
        @commands.has_permissions(manage_messages=True)
        async def blacklist_add(self, ctx, arg1 = None):
            """
            Adds a word to your blacklist
            To add a phrase out of more than one word, use quotation marks. Example: "more than one word"
            """
            guilds = utils.json_loader.read_json()
            for x in guilds:
                if x['id'] == ctx.guild.id:
                    if arg1 not in x['badwords']:
                        try:
                            x['badwords'].append(arg1.lower())
                            utils.json_loader.write_json(guilds)
                            await ctx.send('`' + arg1 + '` was added to your blacklist!')
                        except Exception as e:
                            print(e)
                    else:
                        await ctx.send("`" + arg1 + "` is already on your blacklist!")

        @commands.command()
        @commands.has_permissions(manage_messages=True)
        async def catch_guilds(self, ctx):
            guilds = ctx.bot.guilds
            guildsFromFile = utils.json_loader.read_json()
            guildList = []
            for guild in guildsFromFile:
                guildList.append(guild['id'])

            for x in guilds:
                if x.id not in guildList:
                    data =  {
                        'id': x.id,
                        'owner': ctx.guild.owner.id,
                        'admins': [],
                        'badwords':[],
                        'enabled': 1,
                        'logs': 1,
                    }
                    guildsFromFile.append(data)
            utils.json_loader.write_json(guildsFromFile)


def setup(bot):
    bot.add_cog(profanity(bot))
