import asyncio
import json
import os
import re
import time
import random
from datetime import datetime

import discord
import requests
from discord.ext import commands

def our_custom_check():
    async def predicate(ctx):
        return ctx.guild is not None \
            and ctx.author.guild_permissions.manage_channels \
            and ctx.me.guild_permissions.manage_channels
    return commands.check(predicate)


class Moderation(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
               print(f"{self.__class__.__name__}: [Loaded]")

        # kick commnad
        @commands.command(name="kick", description="A command which kicks a given user", usage="<user> [reason]")
        @our_custom_check()
        @commands.has_guild_permissions(kick_members=True)
        async def kick(self, ctx, member: discord.Member, *, reason=None):
            await ctx.guild.kick(user=member, reason=reason)
            embed = discord.Embed(title=f"{ctx.author.name} kicked: {member.name}", description=reason, color=0xff7700, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.message.delete()
            await ctx.send(embed=embed, delete_after=5)

        # ban command
        @commands.command(name="ban", description="A command which bans a given user", usage="<user> [reason]")
        @our_custom_check()
        @commands.has_guild_permissions(ban_members=True)
        async def ban(self, ctx, member: discord.Member, *, reason=None):
            await ctx.guild.ban(user=member, reason=reason)
            embed = discord.Embed(title=f"{ctx.author.name} banned: {member.name}", description=reason, color=0xff7700, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.message.delete()
            await ctx.send(embed=embed, delete_after=5)

        # unbanned command
        @commands.command(name="unban", description="A command which unbans a given user")
        @our_custom_check()
        @commands.has_guild_permissions(ban_members=True)
        async def unban(self, ctx, member, *, reason=None):
            member = await self.bot.fetch_user(int(member))
            await ctx.guild.unban(member, reason=reason)
            embed = discord.Embed(title=f"{ctx.author.name} unbanned: {member.name}", description=reason, color=0xff7700, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        # clear all command
        @commands.command(name="clear", description="A command which clears the messages")
        @our_custom_check()
        @commands.has_guild_permissions(manage_messages=True)
        async def clear(self, ctx, amount=15):
            await ctx.channel.purge(limit=amount+1)
            embed = discord.Embed(title=f"{ctx.author.name} purged: {ctx.channel.name}", description=f"{amount} messages were cleared", color=0xff7700, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed, delete_after = 4)

        # lockdown command
        @commands.command(name="lockdown", description="Lock, or unlock the given channel!",)
        @our_custom_check()
        @commands.has_guild_permissions(manage_channels=True)
        async def lockdown(self, ctx, channel: discord.TextChannel=None):
            channel = channel or ctx.channel
            if ctx.guild.default_role not in channel.overwrites:
                overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
                }
                await channel.edit(overwrites=overwrites)
                embed = discord.Embed(title=f"I have put `{channel.name}` on lockdown.", color=0xff7700, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, delete_after = 15)
            elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
                overwrites = channel.overwrites[ctx.guild.default_role]
                overwrites.send_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
                embed = discord.Embed(title=f"I have put `{channel.name}` on lockdown.", color=0xff7700, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, delete_after = 15)
            else:
                overwrites = channel.overwrites[ctx.guild.default_role]
                overwrites.send_messages = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
                embed = discord.Embed(title=f"I have removed `{channel.name}` from lockdown.", color=0xff7700, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, delete_after = 15)
                await ctx.message.delete()

            # nuke command (like betterantispam)
        @commands.command(hidden=True, aliases=['nc'])
        @commands.has_permissions(manage_messages=True)
        async def nukechat(self, ctx):
            channel_position = ctx.channel.position
            new_channel = await ctx.channel.clone()
            await new_channel.edit(position=channel_position)
            await ctx.channel.delete()
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/425261854558912512/808215783372750898/tenor.gif")
            await new_channel.send(embed=embed, delete_after=40)


        # slowmode command
        @commands.has_permissions(manage_messages=True)
        @commands.command(name="Slowmode", description="Turns on slowmoded", aliases=['sm'])
        @our_custom_check()
        async def slowmode(self, ctx, seconds: int=0):
            if seconds > 120:
                return await ctx.send("Amount can't be over 120 seconds", delete_after = 4)
            if seconds == 0:
                await ctx.channel.edit(slowmode_delay=seconds)
                embed = discord.Embed(title = "**Slowmode is off for this channel**", color = 0xff7700, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, delete_after=5)
            else:
                if seconds == 1:
                    numofsecs = "second"
                else:
                    numofsecs = "seconds"
                await ctx.channel.edit(slowmode_delay=seconds)
                embed = discord.Embed(title = f"**Set the channel slow mode delay to `{seconds}` {numofsecs}**", color = 0xff7700, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, delete_after=5)
                await ctx.message.delete()


        # soft ban command
        @our_custom_check()
        @commands.has_permissions(ban_members=True)
        @commands.command(name="softban", description="placeholdment", usage="placeholdment")
        async def softban(self, ctx, user : discord.Member, *, reason=None):
            if ctx.author.top_role > user.top_role or ctx.author == ctx.guild.owner:
                if user == ctx.author:
                    embed = discord.Embed(title="***You can't softban yourself...***", color=0xff7700, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed)
                await user.ban(reason=reason)
                await user.unban(reason=reason)
                if not reason:
                    embed = discord.Embed(title=f"**{user} was softbanned**", color=0xff7700, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.message.delete()
                    await ctx.send(embed=embed, delete_after=15)
                else:
                    embed = discord.Embed(title=f"**{user} was softbanned Reason:**", color=0xff7700, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.message.delete()
                    await ctx.send(embed=embed, delete_after=15)


        # hackban commnad
        @commands.command(name="hackban", description="placeholdment")
        @commands.has_permissions(ban_members=True)
        @our_custom_check()
        async def hackban(self, ctx, user_id: int):
                author = ctx.message.author
                guild = author.guild

                user = guild.get_member(user_id)
                if user is not None:
                    return await ctx.invoke(self.bot.ban, user=user)

                try:
                    await self.bot.http.ban(user_id, guild.id, 0)
                    embed = discord.Embed(title = f"{user_id} has been banned", color = 0xff7700, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed, delete_after = 15)
                except discord.NotFound:
                    await ctx.send(f'{user_id} has cannot be found', delete_after = 15, timestamp=ctx.message.created_at)
                except discord.errors.Forbidden:
                    await ctx.send(f'User: <@{user_id}> has not been banned due to your permissions', delete_after = 15, timestamp=ctx.message.created_at)

        # createrole command
        @commands.command(name="createrole", description="placeholdment", aliases=['crole'])
        @our_custom_check()
        async def createrole(self, ctx, *, name:str):
            if ctx.message.author.guild_permissions.manage_roles:
                guild = ctx.guild
                await guild.create_role(name=name, permissions=guild.default_role.permissions)
                embed = discord.Embed(title = "created role: " + "**" + f"``{name}``" + "**", color = 0xff7700, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.message.delete()
                await ctx.send(embed=embed, delete_after=5)
            else:
                embed = discord.Embed(title = "no permissions to run createrole", color = 0xff7700, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, delete_after=5)

        # deleterole command
        @commands.command(name="deleterole", description="placeholdment", aliases=['drole'])
        @our_custom_check()
        async def deleterole(self, ctx, *, name:str, embed=None):
            if ctx.message.author.guild_permissions.manage_roles:
                role = discord.utils.get(ctx.guild.roles, name=name)
                await role.delete()
                embed = discord.Embed(title = "deleted role:" + "**" + f"``{name}``" + "**", color = 0xff7700, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.message.delete()
                await ctx.send(embed=embed, delete_after=15)
            else:
                discord.Embed(title = "no permissions to run deleterole", color = 0xff7700, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, delete_after=15)

        #kick all users without a role credit to Tux#2339
        @commands.command(pass_context = True)
        @commands.has_permissions(kick_members=True)
        @our_custom_check()
        async def snap(self, ctx):
            await ctx.message.delete()
            guild=ctx.message.guild
            for member in tuple(guild.members):
                if len(member.roles)==1:
                    await member.kick()
                    embed = discord.Embed(title="I have successfully kicked all the users without a role!", color = 0xff7700, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        
        # snipe command by octtii
        @commands.command()
        async def snipe(self, ctx):
            try:
                with open('settings/snipe.json') as snipeFile:
                    snipes = json.load(snipeFile)
            except Exception as e:
                print(e)

            for x in snipes:
                if x['id'] == ctx.guild.id:
                    authorAvatar = x['author_avatar']
                    content = x['content']

            embed = discord.Embed(color = 0xff7700, timestamp=ctx.message.created_at)
            embed.set_thumbnail(url = authorAvatar)
            embed.add_field(name = "Deleted Message:", value = content, inline = False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.message.delete()
            await ctx.send(embed = embed)

        # change prefix
        @commands.command(
            name="prefix",
            aliases=["cprefix", "sp"],
            description="Change your guilds prefix!",
            usage="[prefix]",
        )
        @commands.has_guild_permissions(manage_guild=True)
        @our_custom_check()
        @commands.cooldown(1, 50, commands.BucketType.guild)
        async def prefix(self, ctx, *, prefix=">"):
            await self.bot.config.upsert({"_id": ctx.guild.id, "prefix": prefix})
            embed = discord.Embed(
                title =f"The guild prefix has been set to `{prefix}`. Use `{prefix}prefix [prefix]` to change it again!",
                color = 0xff7700
            )
            await ctx.send(embed=embed)

        # deleted prefix
        @commands.command(
        name='deleteprefix',
        aliases=['dp'],
        description="Delete your guilds prefix!"
        )
        @commands.guild_only()
        @commands.has_guild_permissions(manage_guild=True)
        @our_custom_check()
        @commands.cooldown(1, 50, commands.BucketType.guild)
        async def deleteprefix(self, ctx):
            await self.bot.config.unset({"_id": ctx.guild.id, "prefix": 1})
            embed = discord.Embed(
                title = "This guilds prefix has been set back to the default",
                color = 0xff7700
            )
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))
