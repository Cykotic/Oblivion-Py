import os
import asyncio
import discord
import json
from discord.ext import commands
from datetime import datetime
# command_attrs=dict(hidden=True)
class guildsinfo(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print(f"{self.__class__.__name__}: [Loaded]")

        #Userinfo command
        @commands.command(name="Userinfo", description="placeholdment", aliases=["ui"])
        async def userinfo(self, ctx, member: discord.Member):
            status = {
                "online": "🟢",
                "idle": "🟡",
                "offline": "⚫",
                "dnd": "🔴"
            }

            embed = discord.Embed(
                color=0xff7700,
                title=f"➜ Userinfo for: {member}",
                description=f"• Information will be displayed about the user below."
            )
            roles = [role for role in member.roles]
            roles = f" ".join([f"@{role}, " for role in roles])

            embed.set_thumbnail(url=member.avatar_url_as(size=4096, format=None, static_format="png"))
            embed.add_field(name="‣ Account Name", value=str(member))
            embed.add_field(name="‣ Discord ID", value=str(member.id))
            embed.add_field(name="‣ Nickname", value=member.nick or "No nickname.")
            embed.add_field(name="‣ Account Created At", value=member.created_at.strftime("%A %d, %B %Y"))
            embed.add_field(name="‣ Account Joined At", value=member.joined_at.strftime("%A %d, %B %Y"))

            if member.activity is None:
                embed.add_field(name="‣ Current Activity", value="No current activity.")
            else:
                embed.add_field(name="‣ Current Activity", value=member.activity.name)
            if member.bot is True:
                embed.add_field(name="‣ Discord Bot? ", value=":robot:")
            else:
                embed.add_field(name="‣ Discord Bot?", value=":no_entry_sign:")
            if member.is_on_mobile() is True:
                embed.add_field(name="‣ On Mobile Device? ", value=":iphone:")
            else:
                embed.add_field(name="‣ On Mobile Device?", value=":no_mobile_phones:")
            embed.add_field(name="‣ Current Status", value=status[member.status.name])
            embed.add_field(name="‣ Highest Role", inline=False, value=f"```@{member.top_role}```")
            embed.add_field(name="‣ All Roles", inline=False, value=f"```{roles}```")

            await ctx.send(embed=embed)

        # emojistats command
        @commands.command(name="emojinfo", description="placeholdment", aliases=["ei"])
        async def emojinfo(self, ctx, emoji: discord.Emoji):
            embed = discord.Embed(colour=0xff7700,title=f"{emoji.name.title()} stats:", timestamp=ctx.message.created_at)
            embed.add_field(name="Emoji Id", value=f"`{emoji.id}`",inline=False)
            embed.add_field(name="Emoji Created at", value=f'`{emoji.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}`', inline=False)
            embed.add_field(name="Animated ?", value=f"`{emoji.animated}`", inline=True)
            embed.add_field(name="Available for use ?", value=f"`{emoji.available}`", inline=False)
            embed.add_field(name="Guild that belongs to this emoj", value=f"{emoji.guild} `({emoji.guild_id})`", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)


        #Channel Stats command
        @commands.command(name="channelinfo", description="placeholdment", aliases=["chinfo"])
        async def channelinfo(self, ctx):
            channel = ctx.channel
            embed = discord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}", color=0xff7700, timestamp=ctx.message.created_at)
            embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
            embed.add_field(name="Channel Id", value=channel.id, inline=False)
            embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic.'}", inline=False)
            embed.add_field(name="Channel Position", value=channel.position, inline=False)
            embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
            embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
            embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
            embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
            embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
            embed.add_field(name="Channel Hash", value=hash(channel), inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        # role info command
        @commands.command(name="roleinfo", description="placeholdment", aliases=['rinfo'])
        async def roleinfo(self, ctx, *, role:discord.Role):
            name = role.name
            id = role.id
            color = role.color
            mention = role.mentionable
            created = role.created_at
            embed = discord.Embed(timestamp=ctx.message.created_at, color=0xff7700)
            embed.add_field(name="Role Name:", value=f'{name}', inline=False)
            embed.add_field(name="Role ID:", value=f'{id}', inline=False)
            embed.add_field(name="Role Color:", value=f"{color}", inline=False)
            embed.add_field(name="Mentionable?", value=f'{mention}', inline=False)
            embed.add_field(name="Role Creation Date:", value=f'{created}', inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(guildsinfo(bot))
