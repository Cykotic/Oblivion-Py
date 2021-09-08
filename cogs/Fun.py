import json
import random
import time
import urllib.parse
from datetime import datetime
from io import BytesIO

import aiohttp
import discord
import PIL
import praw
import requests
from aiohttp import ClientSession
from art import text2art
from bs4 import BeautifulSoup
from discord.ext import commands
from PIL import ImageDraw

reddit = praw.Reddit(client_id = "45P_ou9gs-paRQ",
                    client_secret = "_DM1hewFvbgm9WA78DEpa8qNgF8",
                    username = "Returness",
                    password = "Cykotic01",
                    user_agent = "oblivion")

# In cogs we make our own class
# for d.py which subclasses commands.Cog

class Fun(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print(f"{self.__class__.__name__}: [Loaded]")

        # change my mind command it's actuly really funny 
        @commands.command(name="mind", description="placeholdment", usage="placeholdment")
        async def mind(self, ctx, *, text):
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}") as r:
                    res = await r.json()
                    embed = discord.Embed(
                        color=0xff7700
                    )
                    embed.set_image(url=res["message"])

                    await ctx.message.delete()
                    await ctx.send(embed=embed)

        # vs command @ 1 v 1 
        @commands.command(name="Vs", description="placeholdment", usage="placeholdment")
        async def vs(self, ctx, member1: discord.Member, member2: discord.Member):
            member1 = member1.avatar_url_as(size=1024, format=None, static_format='png')
            member2 = member2.avatar_url_as(size=1024, format=None, static_format='png')
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        f"https://nekobot.xyz/api/imagegen?type=whowouldwin&user1={member1}&user2={member2}") as r:
                    res = await r.json()
                    embed = discord.Embed(
                        color=0xff7700,
                        title="Who Would Win"
                    )
                    embed.set_image(url=res["message"])
                    await ctx.send(embed=embed)

        # giphy command
        @commands.command(name="giphy", description="placeholdment", aliases=['gy'])
        async def giphy(self, ctx, *, search):
            embed = discord.Embed(title=f"Giphy Search: '{search}' ",colour=0xff7700, timestamp=ctx.message.created_at)
            session = aiohttp.ClientSession()

            if search == '':
                response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=WPgpNZVZp1bqZcLxTu0wpp83aiXilbuB')
                data = json.loads(await response.text())
                embed.set_image(url=data['data']['images']['original']['url'])
            else:
                search.replace(' ', '+')
                response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=WPgpNZVZp1bqZcLxTu0wpp83aiXilbuB&limit=10')
                data = json.loads(await response.text())
                gif_choice = random.randint(0, 9)
                embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])
                embed.set_footer(text=f"Search by: {ctx.author}", icon_url=ctx.author.avatar_url)
            await session.close()
            await ctx.send(embed=embed)
            await ctx.message.delete()
    
         # embed command 
        @commands.command()
        async def embed(self, ctx, *, message):
            delete_target = ctx.message
            await delete_target.delete()
            embed = discord.Embed(title=message, colour=0xff7700)
            await ctx.send(embed=embed)

        # Gay command
        @commands.command(name="Gay", description="placeholdment", usage="placeholdment")
        async def gay(self, ctx, member: discord.Member):
            await ctx.message.delete()
            embed = discord.Embed(
            color=0xff7700,
            title="Howgay?", timestamp=ctx.message.created_at,
            )
            embed.add_field(name="The account is...", 
            value=f"{random.randint(1, 100)}% gay :gay_pride_flag: → {str(member.mention)}")

            await ctx.send(embed=embed)

        # compliment command
        @commands.command(name="compliment", description="placeholdment", aliases=['comp'])
        async def compliment(self, ctx, member: discord.Member):
            # Getting compliment from api
            response = requests.get('https://complimentr.com/api')
            # Formatting response
            compliment = response.json()['compliment']
            x = discord.Embed(
                title = f'{ member.display_name }, { compliment }',
                color=0xff7700,
            )
            await ctx.message.delete()
            await ctx.send(embed=x)


        # meme command
        @commands.command()
        async def meme(self, ctx, subred = "memes"):
            """it's the meme command"""
            subreddit = reddit.subreddit(subred)
            all_subs = []
            hot = subreddit.hot(limit=250)
            for submission in hot:
                all_subs.append(submission)
            random_sub = random.choice(all_subs)
            submission = reddit.submission("7foq2r")
            # comments = submission.comments.replace_more(limit=None)  # Retrieve every single comment
            # comments = submission.comments.list()
            allcmts = submission.num_comments
            name = random_sub.title
            url = random_sub.url
            em = discord.Embed(title = f"{name}", color = 0xff7700)
            em.set_image(url=f"{url}")
            em.set_footer(text = f"👍 {submission.score} || 💬 {allcmts}")
            await ctx.message.delete()
            await ctx.send(embed=em)

        # roast command
        @commands.command()
        async def roast(self, ctx):
            """gives out a roast to someone"""
            response = requests.get(url="https://evilinsult.com/generate_insult.php?lang=en&type=json")
            roast = json.loads(response.text)
            embed = discord.Embed(title=f"{roast['insult']}", color=0xff7700)
            await ctx.message.delete()
            await ctx.send(embed=embed)
            
        # advice command
        @commands.command()
        async def advice(self, ctx):
            """Oblivion gives you advice from the heart"""
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://api.adviceslip.com/advice') as r:
                    res = await r.json(content_type="text/html")
                    embed = discord.Embed(
                        colour=0xff7700,
                        title=f"{res['slip']['advice']}"
                    )
                    await ctx.message.delete()
                    await ctx.send(embed=embed)

        # topic comand
        @commands.command()
        async def topic(self, ctx):
            """Gives You Something to talk about lol"""
            website = requests.get('https://www.conversationstarters.com/generator.php').content
            soup = BeautifulSoup(website, 'html.parser')
            topic = soup.find(id="random").text
            embed = discord.Embed(
                title = f"{topic}",
                colour=0xff7700,
            )
            await ctx.message.delete()
            await ctx.send(embed=embed)

        @commands.command()
        async def coinflip(self, ctx):
            """Flips a coin Heads or Tails"""
            choices = ["Heads", "Tails", "The coin fell down, Try again."]
            rancoin = random.choice(choices)
            await ctx.send(rancoin)

        @commands.command(aliases=["ascii"])
        async def asciify(self, ctx, *, text: str):
            """ Turns any text given into ascii """
            Art = text2art(text)
            asciiart = f"```\n{Art}\n```"
            if len(asciiart) > 2000:
                return await ctx.send("That art is too big")
            await ctx.send(asciiart)

        @commands.command()
        async def test(self, ctx):
            embed = discord.Embed(
                title = "Cykotic is my Senpai!",
                colour=0xff7700,
            )
            embed.set_image(url="https://tenor.com/view/senpai-notice-gif-5740206")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
