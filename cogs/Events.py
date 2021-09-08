import asyncio
import json
import random
import time
from datetime import datetime

import discord
from discord.ext import commands
from utils import json_loader

class Events(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print(f"{self.__class__.__name__}: [Loaded]")

        # error event
        @commands.Cog.listener()
        async def on_command_error(self, ctx, error):
            if isinstance(error, commands.CommandNotFound):  # Command not found
                embed = discord.Embed(title = '❌** Command Not Found ** ❌', color = 0xff7700, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, delete_after=5)
                await ctx.message.delete()
            if isinstance(error, commands.NotOwner): # not owner check
                embed = discord.Embed(title = '❌** You are not the owner! ** ❌', color = 0xff7700, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, delete_after=5)
                await ctx.message.delete()
            if isinstance(error, commands.MissingRequiredArgument): # Missing Argument
                embed = discord.Embed(title = f'❌** {error}! ** ❌', color = 0xff7700, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, delete_after=5)
                await ctx.message.delete()
            else:
                embederror1 = discord.Embed(title = f"{error}", color = 0xff7700, timestamp=ctx.message.created_at)
                embederror1.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embederror1, delete_after=10)

        @commands.Cog.listener()
        async def on_message(self, ctx):
            if ctx.author.id == self.bot.user.id:
                return
            else:
                guilds = json_loader.read_json()
                for x in guilds:
                    if x['id'] == ctx.guild.id:
                        for y in x['badwords']:
                            if y in ctx.content.lower():
                                await ctx.delete()
                                await ctx.channel.send('Watch your profanity, <@' + str(ctx.author.id) + '> !!')
                                trigger = y
                                try:
                                    if x['logs'] == 1:
                                        channel = discord.utils.get(ctx.guild.text_channels, name="logs")
                                        embed = discord.Embed(  title = 'Message deleted',
                                                                description = 'Bad word detected! Message was deleted automatically.',
                                                                color = 0xff7700,
                                                                timestamp=datetime.datetime.utcfromtimestamp(datetime.datetime.now().timestamp()))
                                        embed.add_field(name = '__User__', value = '**' + str(ctx.author) + '**\n' + str(ctx.author.id), inline = False)
                                        embed.add_field(name = '__Triggered word__', value = trigger, inline = False)
                                        embed.add_field(name = '__Channel__', value = '**' + ctx.channel.name + '**\n' + str(ctx.channel.id))
                                        embed.add_field(name = '__Server__', value = '**' + ctx.guild.name + '**\n' + str(ctx.guild.id))
                                        embed.add_field(name = '__Message__', value = ctx.content, inline = False)
                                        #embed.set_author(name = str(ctx.author), icon_url = ctx.author.avatar_url)
                                        embed.set_thumbnail(url = ctx.author.avatar_url)
                                        await channel.send(embed = embed)
                                except:
                                    pass


        # snipe command and blacklist words commands credit to octii  
        @commands.Cog.listener()
        async def on_message_delete(self, ctx):
            try:
                with open('settings/snipe.json') as snipeFile:
                    snipes = json.load(snipeFile)
            except Exception as e:
                print(e)

            for x in snipes:
                if x['id'] == ctx.guild.id:
                    x['author_name'] = str(ctx.author)
                    x['author_id'] = ctx.author.id
                    x['author_avatar'] = str(ctx.author.avatar_url)
                    x['content'] = str(ctx.content)
                    x['channel_name'] = ctx.channel.name
                    x['channel_id'] = ctx.channel.id

            try:
                with open('settings/snipe.json', 'w') as outfile:
                    json.dump(snipes, outfile, indent=4)
            except Exception as e:
                print(e)

        @commands.Cog.listener()
        async def on_guild_join(self, guild):
            try:
                with open('settings/snipe.json') as snipesFile:
                    snipes = json.load(snipesFile)
            except Exception as e:
                print(e)

            newGuild = {
                "id": guild.id,
                "author_name": "",
                "author_id": 000,
                "author_avatar": "",
                "content": "",
                "time": "",
                "channel_name": "",
                "channel_id": 000,
            }


            snipes.append(newGuild)

            try:
                with open('settings/snipe.json', 'w') as outfile:
                    json.dump(snipes, outfile, indent=4)
            except Exception as e:
                print(e)

def setup(bot):
    bot.add_cog(Events(bot))