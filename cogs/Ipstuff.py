import os
import asyncio
import discord
import json
import requests
from discord.ext import commands

# command_attrs=dict(hidden=True)
class ipstuff(commands.Cog, command_attrs=dict(hidden=True)):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print(f"{self.__class__.__name__}: [Loaded]")


        #ip command Credit to octii he made most of it
        @commands.command(hidden=True)
        async def ip(self, ctx, ipAddress):
            try:
                r = requests.get(url="http://ip-api.com/json/" + ipAddress)
                resp = json.loads(r.text)
                if resp['status'] == 'success':
                    if resp['zip'] == '':
                        resp['zip'] = 'unknown'
                    if resp['org'] == '':
                        resp['org'] = 'unknown'
                    if resp['city'] == '':
                        resp['city'] = 'unknown'

                    ipEmbed = discord.Embed(title = f'IP Address Information: {ipAddress}', colour = 0xff7700, timestamp=ctx.message.created_at)
                    ipEmbed.add_field(name = 'Country', value = resp['country'], inline=False)
                    ipEmbed.add_field(name = 'Region', value = resp['regionName'], inline=False)
                    ipEmbed.add_field(name = 'City', value = resp['city'], inline=False)
                    ipEmbed.add_field(name = 'ZIP Code', value = resp['zip'], inline=False)
                    ipEmbed.add_field(name = 'Latitude', value = resp['lat'], inline=False)
                    ipEmbed.add_field(name = 'Longitude', value = resp['lon'], inline=False)
                    ipEmbed.add_field(name = 'ISP', value = resp['isp'], inline=False)
                    ipEmbed.add_field(name = 'Timezone', value = resp['timezone'], inline=False)
                    ipEmbed.add_field(name = 'Organization', value = resp['org'], inline=False)
                    ipEmbed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed = ipEmbed)
                elif resp['status'] == 'fail':
                    try:
                        ipEmbed = discord.Embed(title = 'IP Address Information Error',
                                                description = resp['query'],
                                                colour = 0xff7700,
                                                timestamp=ctx.message.created_at)
                        ipEmbed.add_field(name = "Error message", value = resp['message'])
                        ipEmbed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                        await ctx.send(embed = ipEmbed)
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)

        #portscan credit to Tux#2339
        @commands.command(hidden=True)
        async def nmap(self, ctx, target):
            await ctx.message.delete()
            r = requests.get(f"https://api.hackertarget.com/nmap/?q={target}")
            embed=discord.Embed(title=f"Scanning ports for {target}", description=f"{r.text}", color = 0xff7700, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ipstuff(bot))
