import discord
from discord.ext import commands
import nekos
import requests
import json

class nsfw(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print(f"{self.__class__.__name__}: [Loaded]")

        @commands.command()
        @commands.is_nsfw()
        async def oboobs(self, ctx):
            url = "http://api.oboobs.ru/boobs/0/1/random"
            r = requests.get(url=url)
            res = json.loads(r.text)
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"https://media.oboobs.ru/{res[0]['preview']}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def obutts(self, ctx):
            url = "http://api.obutts.ru/butts/0/1/random"
            r = requests.get(url=url)
            res = json.loads(r.text)
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"http://media.obutts.ru/{res[0]['preview']}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def tits(self, ctx):
            url = "https://nekos.life/api/v2/img/tits"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def hentai(self, ctx):
            url = "https://nekos.life/api/v2/img/hentai"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def yuri(self, ctx):
            url = "https://nekos.life/api/v2/img/yuri"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def erofeet(self, ctx):
            url = "https://nekos.life/api/v2/img/erofeet"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def femdom(self, ctx):
            url = "https://nekos.life/api/v2/img/femdom"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def erok(self, ctx):
            url = "https://nekos.life/api/v2/img/erok"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def les(self, ctx):
            url = "https://nekos.life/api/v2/img/les"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def hololewd(self, ctx):
            url = "https://nekos.life/api/v2/img/hololewd"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def lewdk(self, ctx):
            url = "https://nekos.life/api/v2/img/lewdk"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def keta(self, ctx):
            url = "https://nekos.life/api/v2/img/keta"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def feetg(self, ctx):
            url = "https://nekos.life/api/v2/img/feetg"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def nsfw_neko_gif(self, ctx):
            url = "https://nekos.life/api/v2/img/nsfw_neko_gif"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def pussy_jpg(self, ctx):
            url = "https://nekos.life/api/v2/img/pussy_jpg"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def cum(self, ctx):
            url = "https://nekos.life/api/v2/img/cum_jpg"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def pussy(self, ctx):
            url = "https://nekos.life/api/v2/img/pussy"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def lewdkemo(self, ctx):
            url = "https://nekos.life/api/v2/img/lewdkemo"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def lewd(self, ctx):
            url = "https://nekos.life/api/v2/img/lewd"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def smallboobs(self, ctx):
            url = "https://nekos.life/api/v2/img/smallboobs"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def random_hentai_gif(self, ctx):
            url = "https://nekos.life/api/v2/img/Random_hentai_gif"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def boobs(self, ctx):
            url = "https://nekos.life/api/v2/img/boobs"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def feet(self, ctx):
            url = "https://nekos.life/api/v2/img/feet"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def solog(self, ctx):
            url = "https://nekos.life/api/v2/img/solog"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def ero(self, ctx):
            url = "https://nekos.life/api/v2/img/ero"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def eron(self, ctx):
            url = "https://nekos.life/api/v2/img/eron"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def erokemo(self, ctx):
            url = "https://nekos.life/api/v2/img/erokemo"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def anal(self, ctx):
            url = "https://nekos.life/api/v2/img/anal"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def trap(self, ctx):
            url = "https://nekos.life/api/v2/img/trap"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def bj(self, ctx):
            url = "https://nekos.life/api/v2/img/bj"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def holoero(self, ctx):
            url = "https://nekos.life/api/v2/img/holoero"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def gasm(self, ctx):
            url = "https://nekos.life/api/v2/img/gasm"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def futanari(self, ctx):
            url = "https://nekos.life/api/v2/img/futanari"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def solo(self, ctx):
            url = "https://nekos.life/api/v2/img/solo"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

        @commands.command()
        @commands.is_nsfw()
        async def pwankg(self, ctx):
            url = "https://nekos.life/api/v2/img/pwankg"
            r = requests.get(url=url)
            res = json.loads(r.text)
            picUrl = res['url']
            await ctx.message.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url=f"{picUrl}")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(nsfw(bot))