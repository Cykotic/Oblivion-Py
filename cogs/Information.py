import asyncio
import datetime
import json
import logging
import platform
import random
import time
from platform import python_version
from random import choice as rnd

import aiohttp
import discord
import psutil
import requests
from discord.ext import commands
import re
from urllib.parse import urlparse

# In cogs we make our own class
# for d.py which subclasses commands.Cog

session = aiohttp.ClientSession()
start_time = datetime.datetime.now() # uptime command well part of it

# Convert uptime to a string.
def timedelta_str(dt):
    days = dt.days
    hours, r = divmod(dt.seconds, 3600)
    minutes, sec = divmod(r, 60)

    if minutes == 1 and sec == 1:
        return '{0} days, {1} hours, {2} minute and {3} second.'.format(days,hours,minutes,sec)
    elif minutes > 1 and sec == 1:
        return '{0} days, {1} hours, {2} minutes and {3} second.'.format(days,hours,minutes,sec)
    elif minutes == 1 and sec > 1:
        return '{0} days, {1} hours, {2} minute and {3} seconds.'.format(days,hours,minutes,sec)
    else:
        return '{0} days, {1} hours, {2} minutes and {3} seconds.'.format(days,hours,minutes,sec)

class Information(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print(f"{self.__class__.__name__}: [Loaded]")

        # invite command 
        @commands.command(aliases=['inv'])
        async def invite(self, ctx: commands.Context):
            embed = discord.Embed(description = f"<https://discord.com/oauth2/authorize?client_id={ctx.bot.user.id}&permissions=2146958591&scope=bot>", color=0xff7700, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.message.delete()
            await ctx.send(embed=embed)

        # serverinvite command
        @commands.command(name="serverinvite", description="placeholdment", aliases=['sinv'])
        async def serverinvite(self, ctx):
            link = await ctx.channel.create_invite(max_age = 86400, max_uses = 0)
            await ctx.send("Server link:")
            await ctx.send(link)

        # wikipedia command
        @commands.command(name="wikipedia", description="placeholdment", aliases=['w', 'wiki'])
        async def wikipedia(self,ctx, *, query: str):
            sea = requests.get(
                ('https://en.wikipedia.org//w/api.php?action=query'
                '&format=json&list=search&utf8=1&srsearch={}&srlimit=5&srprop='
                ).format(query)).json()['query']

            if sea['searchinfo']['totalhits'] == 0:
                await ctx.send('Sorry, your search could not be found.')
            else:
                for x in range(len(sea['search'])):
                    article = sea['search'][x]['title']
                    req = requests.get('https://en.wikipedia.org//w/api.php?action=query'
                                    '&utf8=1&redirects&format=json&prop=info|images'
                                    '&inprop=url&titles={}'.format(article)).json()['query']['pages']
                    if str(list(req)[0]) != "-1":
                        break
                else:
                    await ctx.send('Sorry, your search could not be found.')
                    return
                article = req[list(req)[0]]['title']
                arturl = req[list(req)[0]]['fullurl']
                artdesc = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/'+article).json()['extract']
                lastedited = datetime.datetime.strptime(req[list(req)[0]]['touched'], "%Y-%m-%dT%H:%M:%SZ")
                embed = discord.Embed(title='**'+article+'**', url=arturl, description=artdesc, color=0xff7700)
                embed.set_footer(text='Wiki entry last modified')
                embed.set_author(name='Wikipedia', url='https://en.wikipedia.org/')
                embed.timestamp = lastedited
                await ctx.send('**Search result for:** ***"{}"***:'.format(query), embed=embed)


        # urban command
        @commands.command(name="urban", description="placeholdment")
        async def urban(self, ctx, *, term: str = 'stupid'):
            URL = f'http://api.urbandictionary.com/v0/define?term={term}'
            DATA = requests.get(URL).json()
            try:
                DEF = DATA['list'][0]['definition']
            except IndexError:
                await ctx.send(f'Could not find a definition for ``{term}``.')
                return
            EKS = DATA['list'][0]['example']
            summary = f'Word: {term}\n\nDefinition:\n\t{DEF}\n\nUsage:\n\t{EKS}'
            dictLen = 1990
            if len(summary) > 1990:
                loop: bool = True
                while loop:
                    if summary[dictLen-1:dictLen] == '.':
                        loop: bool = False
                    else:
                        dictLen -= 1
                await ctx.send('``Summary was longer than expected, output truncated.``')
            await ctx.send(f'```apache\n{summary[:dictLen]}```')
            await ctx.message.delete()

        # random history command
        @commands.command(name="history", description="placeholdment")
        async def history(self, ctx):
            async with aiohttp.ClientSession() as cs:
                async with cs.get('http://numbersapi.com/random/date?json') as r:
                    res = await r.json()
                    embed = discord.Embed(color=0xff7700, title=f"Fact: {res['text']}", description=f"Year it happen in: {res['year']}", timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.message.delete()
                    await ctx.send(embed=embed)

        # server icon command
        @commands.command(name="servericon", description="placeholdment")
        async def servericon(self, ctx):

                embed = discord.Embed(
                    color=0xff7700,
                    title=f"{ctx.guild.name}'s icon",
                    description=f'[PNG]({ctx.guild.icon_url_as(size=1024, format="png")}) | '
                                f'[JPEG]({ctx.guild.icon_url_as(size=1024, format="jpeg")}) | '
                                f'[WEBP]({ctx.guild.icon_url_as(size=1024, format="webp")})',
                                timestamp=ctx.message.created_at
                )

                if ctx.guild.is_icon_animated():
                    embed.description += f' | [GIF]({ctx.guild.icon_url_as(size=1024, format="gif")})'
                    embed.set_image(url=str(ctx.guild.icon_url_as(size=1024, format='gif')))
                else:
                    embed.set_image(url=str(ctx.guild.icon_url_as(size=1024, format='png')))
                    embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)

                await ctx.message.delete()
                return await ctx.send(embed=embed)

        # Avatar command
        @commands.command(name="avatar", description="placeholdment")
        async def avatar(self, ctx, member: discord.Member):
            show_avatar = discord.Embed(
                color=0xff7700,
                timestamp=ctx.message.created_at
            )
            show_avatar.set_image(url='{}'.format(member.avatar_url))
            show_avatar.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=show_avatar)


        @commands.command(aliases=['bi'])
        async def botstatus(self, ctx):
            embed = discord.Embed(title=f"{self.bot.user.name}'s stats",colour=0xff7700, timestamp=ctx.message.created_at)
            mod = ", ".join(list(self.bot.cogs))
            global start_time
            OS = platform.platform()
            OS = str(OS)
            cpu = psutil.cpu_percent()
            cpu = str(cpu)
            ram = dict(psutil.virtual_memory()._asdict())
            ram = str(ram['percent'])
            total_guild_count = len(self.bot.guilds)
            total_user_count = len(list(self.bot.get_all_members()))
            total_unique_user_count = len(list(set(self.bot.get_all_members())))
            fields = [
            # add fields here
            ("Python Version:", python_version(), False),
            ("Discord.py Version:", discord.__version__, False),
            ("Total Commands:", f"{len(self.bot.commands)}", False),
            ("Total Servers:", f"{total_guild_count}", False),
            ("Total Users:", f"{total_user_count}", False),
            ("Total Unique Users:", f"{total_unique_user_count}", False),
            ("Uptime",timedelta_str(datetime.datetime.now() - start_time), False),
            ("API Latency", f"{round(self.bot.latency*1000)}ms", False),
            ("OS:", f"{OS}", False),
            ("CPU:", f"{cpu}", False),
            ("RAM:", f"{ram}", False),
            ("Cogs Loaded:", f"{mod}", False),
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

        #credits command.
        @commands.command()
        async def credits(self, ctx):
            embed = discord.Embed(title="Gotta Give Credit Where it's due:", color=0xff7700, timestamp=ctx.message.created_at)
            fields = [
            # add fields here
            ("Dread:", "** For Helping me and teaching some things in discord.js and also inspiring me to make a bot **", True),
            ("Kernel:", "** For being a amazing ass friend to me all these years and supporting me when i had nobody around / also for being my dad (he's fat) **", True),
            ("Jinx:", "** He's a pain in the ass but he did help me in the devlopment, and help me understand some things **", True),
            ("𝐷𝑎𝑟𝑘𝐵𝑙𝑢𝑒𝐻𝑎𝑧𝑒:", "** He's been a really old friend of mine and he's been really supportive of my bot since day 1 **", True),
            ("👹M҉a҉c҉h҉o҉👹:", "** he's been supporting in my bot development / helping me host my bot and he's just a great friend in general **", True),
            ("ochtii the builder", "** he's been a great help, this bot went through js > python because of this mans and him helping me host and teaching me the coding of python i have to thank him mainly **", True),
            ("Russell:", "** He's been supporting me since the day i've met him **", True),
            ("Celery:", "** he's been supporting and helping me anyway he can **", True),
            ("Tux:", "** credit to tux for giving me 2 of his commands, ""snap"" and ""portscan"" **", True),
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

        # anime command
        @commands.command(aliases=['anilist'])
        async def anime(self, ctx, *, animeName: str):
            api = ''
            query = '''query ($name: String){ Media(search: $name, type: ANIME) { id idMal description title { romaji english } coverImage { large } startDate {year month day} endDate { year month day } synonyms format status episodes duration nextAiringEpisode { episode } averageScore meanScore source genres tags { name } studios(isMain: true) { nodes { name } } siteUrl } }'''
            variables = {
                'name': animeName
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(api, json={'query': query, 'variables': variables}) as r:
                    if r.status == 200:
                        json = await r.json()
                        data = json['data']['Media']

                        embed = discord.Embed(colour= 0xff7700)
                        embed.set_footer(text='API provided by AniList.co | ID: {}'.format(str(data['id'])))
                        embed.set_thumbnail(url=data['coverImage']['large'])
                        if data['title']['english'] == None or data['title']['english'] == data['title']['romaji']:
                            embed.add_field(name='Title:', value=data['title']['romaji'], inline=False)
                        else:
                            embed.add_field(name='Title:', value='{} ({})'.format(data['title']['english'], data['title']['romaji']), inline=False)

                        embed.add_field(name='Description', value=data['description'], inline=False)
                        if data['synonyms'] != []:
                            embed.add_field(name='Synonyms', value=', '.join(data['synonyms']), inline=True)

                        embed.add_field(name='Typ', value=data['format'].replace('_', ' ').title().replace('Tv', 'TV'), inline=True)
                        embed.add_field(name='Duration', value=str(data['duration']) + ' min', inline=True)

                        embed.add_field(name='Started', value='{}.{}.{}'.format(data['startDate']['month'], data['startDate']['day'], data['startDate']['year']), inline=True)
                        if data['endDate']['day'] == None:
                            embed.add_field(name='Released Date', value=data['nextAiringEpisode']['episode'] - 1, inline=True)
                        elif data['episodes'] > 1:
                            embed.add_field(name='Completed', value='{}.{}.{}'.format(data['endDate']['month'], data['endDate']['day'], data['endDate']['year']), inline=True)

                        embed.add_field(name='Status', value=data['status'].replace('_', ' ').title(), inline=True)

                        try:
                            embed.add_field(name='Head-Studio', value=data['studios']['nodes'][0]['name'], inline=True)
                        except IndexError:
                            pass
                        embed.add_field(name='Ø Score', value=data['averageScore'], inline=True)
                        embed.add_field(name='Genres', value=', '.join(data['genres']), inline=False)
                        tags = ''
                        for tag in data['tags']:
                            tags += tag['name'] + ', '
                        embed.add_field(name='Tags', value=tags[:-2], inline=False)
                        try:
                            embed.add_field(name='Adapted from', value=data['source'].replace('_', ' ').title(), inline=True)
                        except AttributeError:
                            pass

                        embed.add_field(name='AniList Link', value=data['siteUrl'], inline=False)
                        embed.add_field(name='MyAnimeList Link', value='https://myanimelist.net/anime/' + str(data['idMal']), inline=False)
                        await ctx.send(embed=embed)

        # manga command
        @commands.command()
        async def manga(self, ctx, *, mangaName: str):
            api = 'https://graphql.agnilist.co'
            query = '''query ($name: String){ Media(search: $name, type: MANGA) {id idMal description title { romaji english } coverImage { large } startDate { year month day } endDate { year month day } status chapters volumes averageScore meanScore genres tags { name } siteUrl } }'''
            variables = {
                'name': mangaName
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(api, json={'query': query, 'variables': variables}) as r:
                    if r.status == 200:
                        json = await r.json()
                        data = json['data']['Media']

                        embed = discord.Embed(colour= 0xff7700)
                        embed.set_footer(text='API provided by AniList.co | ID: {}'.format(str(data['id'])))
                        embed.set_thumbnail(url=data['coverImage']['large'])
                        if data['title']['english'] == None or data['title']['english'] == data['title']['romaji']:
                            embed.add_field(name='Title', value=data['title']['romaji'], inline=False)
                        else:
                            embed.add_field(name='Title', value='{} ({})'.format(data['title']['english'], data['title']['romaji']), inline=False)
                        embed.add_field(name='description', value=data['description'], inline=False)
                        if data['chapters'] != None:
                            # https://github.com/AniList/ApiV2-GraphQL-Docs/issues/47
                            embed.add_field(name='chapter', value=data['chapters'], inline=True)
                            embed.add_field(name='Volumes', value=data['volumes'], inline=True)
                        embed.add_field(name='Started', value='{}.{}.{}'.format(data['startDate']['month'], data['startDate']['day'], data['startDate']['year']), inline=True)
                        if data['endDate']['day'] != None:
                            embed.add_field(name='Completed', value='{}.{}.{}'.format(data['endDate']['month'], data['endDate']['day'], data['endDate']['year']), inline=True)
                        embed.add_field(name='Status', value=data['status'].replace('_', ' ').title(), inline=True)
                        embed.add_field(name='Ø Score', value=data['averageScore'], inline=True)
                        embed.add_field(name='Genres', value=', '.join(data['genres']), inline=False)
                        tags = ''
                        for tag in data['tags']:
                            tags += tag['name'] + ', '
                        embed.add_field(name='Tags', value=tags[:-2], inline=False)
                        embed.add_field(name='AniList Link', value=data['siteUrl'], inline=False)
                        embed.add_field(name='MyAnimeList Link', value='https://myanimelist.net/anime/' + str(data['idMal']), inline=False)
                        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Information(bot))
