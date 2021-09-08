import json
import os
import asyncio
import discord
from discord import Permissions
from discord.ext import commands
from datetime import datetime
import utils
import io
from utils.Utility import clean_code, Pag
import contextlib
from traceback import format_exception
import ast
import importlib
import textwrap

# part of the pruge members
class MemberIDConverter(commands.MemberConverter):
    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument)
            except ValueError:
                raise commands.BadArgument()            

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class devlopment(commands.Cog, command_attrs=dict(hidden=True)):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print(f"{self.__class__.__name__}: [Loaded]")

        @commands.Cog.listener()
        async def on_command_completion(self, ctx):
            if ctx.command.qualified_name == "logout":
                return

            if await self.bot.command_usage.find(ctx.command.qualified_name) is None:
                await self.bot.command_usage.upsert(
                    {"_id": ctx.command.qualified_name, "usage_count": 1}
                )
            else:
                await self.bot.command_usage.increment(
                    ctx.command.qualified_name, 1, "usage_count"
                )

        @commands.command(aliases=["cs"])
        @commands.is_owner()
        @commands.cooldown(1, 5, commands.BucketType.guild)
        async def command_stats(self, ctx):
            data = await self.bot.command_usage.get_all()
            command_map = {item["_id"]: item["usage_count"] for item in data}

            # get total commands run
            total_commands_run = sum(command_map.values())

            # Sort by value
            sorted_list = sorted(command_map.items(), key=lambda x: x[1], reverse=True)

            pages = []
            cmd_per_page = 10

            for i in range(0, len(sorted_list), cmd_per_page):
                message = "Command Name: `Usage % | Num of command runs`\n\n"
                next_commands = sorted_list[i: i + cmd_per_page]

                for item in next_commands:
                    use_percent = item[1] / total_commands_run
                    message += f"**{item[0]}**: `{use_percent: .2%} | Ran {item[1]} times`\n"

                pages.append(message)

            await Pag(title="Command Usage Statistics!", color=0xff7700, entries=pages, length=1).start(ctx)


        # list servers
        @commands.command(aliases=['list'])
        @commands.is_owner()
        async def servers(self, ctx):
            message = '```'
            message += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID:', 'Member:', 'Name:', 'Owner:')
            for guild in self.bot.guilds:
                message += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
            message += '```'
            embed = discord.Embed(
                color = 0xff7700
            )
            embed.add_field(name="Here are the servers i'm in:", value=f'{message}', inline=False)
            await ctx.send(embed=embed)

        # list bans
        @commands.command(name="listbans", description="shows all the bans in the server")
        @commands.is_owner()
        async def bans(self, ctx):
            users = await ctx.guild.bans()
            if len(users) > 0:
                message = f'``{"ID:":21}{"Name:":25}Reason:\n'
                for entry in users:
                    userID = entry.user.id
                    userName = str(entry.user)
                    if entry.user.bot:
                        userName = '🤖' + userName #:robot: emoji
                    reason = str(entry.reason) #Could be None
                    message += f'{userID:<21}{userName:25} {reason}\n'
                embed = discord.Embed(colour=0xff7700)
                embed.add_field(name='List of bans users:', value=message + '``', inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send('There are no banned users!')

        # log command
        # logging the chat, onl 100 char long.
        @commands.command()
        @commands.is_owner()
        async def log(self, ctx, messages : int = 10000, *, chan : discord.TextChannel = None):

                timeStamp = datetime.today().strftime("%Y-%m-%d %H.%M")
                logFile = 'Logs-{}.txt'.format(timeStamp)

                if not chan:
                    chan = ctx

                # Remove original message
                await ctx.message.delete()
                mess = await ctx.send('Saving logs to *{}*...'.format(logFile))

                # Use logs_from instead of purge
                counter = 0
                msg = ''
                async for message in chan.history(limit=messages):
                    counter += 1
                    msg += message.content + "\n"
                    msg += '----Sent-By: ' + message.author.name + '#' + message.author.discriminator + "\n"
                    msg += '---------At: ' + message.created_at.strftime("%Y-%m-%d %H.%M") + "\n"
                    if message.edited_at:
                        msg += '--Edited-At: ' + message.edited_at.strftime("%Y-%m-%d %H.%M") + "\n"
                    msg += '\n'

                msg = msg[:-2].encode("utf-8")

                with open(logFile, "wb") as myfile:
                    myfile.write(msg)

                await mess.edit(content='Uploading *{}*...'.format(logFile), delete_after = 5)
                await ctx.author.send(file=discord.File(fp=logFile))
                await mess.edit(content='Uploaded *{}!*'.format(logFile), delete_after = 5)
                os.remove(logFile)

        # load . cogs
        @commands.command()
        @commands.is_owner()
        async def load(self, ctx, extension):
            extension = extension.lower()
            self.bot.load_extension(f'cogs.{extension}')
            embed = discord.Embed(title = f"The cog ``{extension}`` has loaded", color = 0xff7700, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.message.delete()
            await ctx.send(embed=embed, delete_after=4)

        # unload . cogs
        @commands.command()
        @commands.is_owner()
        async def unload(self, ctx, extension):
            extension = extension.lower()
            self.bot.unload_extension(f'cogs.{extension}')
            embed = discord.Embed(title = f"The cog ``{extension}`` has unloaded", color = 0xff7700, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.message.delete()
            await ctx.send(embed=embed, delete_after=4)

        # reload . cogs
        @commands.command()
        @commands.is_owner()
        async def reload(self, ctx, extension):
            extension = extension.lower()
            self.bot.unload_extension(f'cogs.{extension}')
            self.bot.load_extension(f'cogs.{extension}')
            embed = discord.Embed(title = f"The cog ``{extension}`` has reloaded", color = 0xff7700, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.message.delete()
            await ctx.send(embed=embed, delete_after=4)

        @commands.command(aliases=['ra'])
        @commands.is_owner()
        async def reloadall(self, ctx):
            firstTime = True
            reloaded = []
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py') and not filename.startswith("_"):
                        self.bot.reload_extension(f'cogs.{filename[:-3]}')
                        reloaded += [filename[:-3], ]
                        if firstTime:
                                embedvar = discord.Embed(title='Reloading Cogs...', description='If you see this message for more than 10 seconds, an error most likely occurred, no cogs were reloaded', color = 0xff7700)
                                message = await ctx.send(embed=embedvar)
                                firstTime = False
                        else:
                                embedvar1 = discord.Embed(title='Reloading Cogs...', description=f"Reloaded cog(s): {', '.join(reloaded)}", color = 0xff7700)
                                await asyncio.sleep(1)
                                await message.edit(embed=embedvar1)
                        #await ctx.send(f'Cog: {filename[:-3]} was reloaded')
            embedvar1 = discord.Embed(title='Reloading Cogs...', description=f"Reloaded cog(s): {', '.join(reloaded)}", color = 0xff7700)
            embedvar1.add_field(name='Success!', value="Successfully reloaded all Cogs")
            await message.edit(embed=embedvar1, delete_after=15)

        # purge the members
        @commands.command(aliases=['dl', 'member'])
        @commands.is_owner()
        async def dmember(self, ctx, member: MemberIDConverter, limit: int=100, channel: discord.TextChannel=None):
            if channel is None:
                channel = ctx.channel

            if isinstance(member, discord.Member):
                def predicate(message):
                    return message.author == member
            else:
                def predicate(message):
                    return message.author.id == member

            # noinspection PyUnresolvedReferences
            messages = await channel.purge(limit=limit, check=predicate)
            messages = len(messages)
            await ctx.message.delete()

        @commands.command(aliases=['bbl'])
        @commands.is_owner()
        async def bblacklist_add(self, ctx, user: discord.Member):
            if ctx.message.author.id == user.id:
                await ctx.send("Hey, you cannot blacklist yourself!")
                return

            self.bot.blacklisted_users.append(user.id)
            data = utils.dbloader.read_json("blacklist")
            data["blacklistedUsers"].append(user.id)
            utils.dbloader.write_json(data, "blacklist")
            embed = discord.Embed(title = f"Hey, I have blacklisted `{user.name}` for you.", color = 0xff7700)
            await ctx.message.delete()
            await ctx.send(embed=embed, delete_after=10)

        @commands.command(aliases=['ubl'])
        @commands.is_owner()
        async def bblacklist_remove(self, ctx, user: discord.Member):
            self.bot.blacklisted_users.remove(user.id)
            data = utils.dbloader.read_json("blacklist")
            data["blacklistedUsers"].remove(user.id)
            utils.dbloader.write_json(data, "blacklist")
            embed = discord.Embed(title = f"Hey, I have unblacklisted `{user.name}` for you.", color = 0xff7700)
            await ctx.message.delete()
            await ctx.send(embed=embed, delete_after=10)

        # restart coommand 
        @commands.command()
        @commands.is_owner()
        async def restart(self, ctx):
            embed = discord.Embed(title="Restarting...", color = 0xff7700)
            try:
                print("---------------------Restarting---------------------")
                await ctx.send(embed=embed)
                await self.bot.cwlose()
            except:
                pass
            finally:
                os.system("python main.py --cmd run")

        #hack ban (massive)
        @commands.command()
        @commands.is_owner()
        async def masshackban(self, ctx, objects: commands.Greedy[discord.Object], *, reason: str=None):
            reason = reason or "Part of a mass ban!"
            for obj in objects:
                await ctx.guild.ban(obj, reason=reason)

            total = len(objects)
            embed = discord.Embed(
                title = f"hackbanned {total} user{'s' if total not in [0,1] else ''} from this guild.",
                color = 0xff7700
            )
            await ctx.send(embed=embed, delete_after=15)

        #hack ban (massive)
        @commands.command()
        @commands.is_owner()
        async def massban(self, ctx, objects: commands.Greedy[discord.Member], *, reason: str=None):
            reason = reason or "Part of a mass ban!"
            for obj in objects:
                await ctx.guild.ban(obj, reason=reason)

            total = len(objects)
            embed = discord.Embed(
                title = f"banned {total} user{'s' if total not in [0,1] else ''} from this guild.",
                color = 0xff7700
            )
            await ctx.send(embed=embed, delete_after=15)

        @commands.command(aliases=["e"])
        @commands.is_owner()
        async def enabled(self, ctx, *, command):
            command = self.bot.get_command(command)
            

            if command is None:
                embed = discord.Embed(
                    title = "I can't find a command with that name!",
                    color = 0xff7700
                )
                await ctx.send(embed=embed)

            elif ctx.command == command:
                    embed = discord.Embed(
                    title = "You cannnot disable this command!",
                    color = 0xff7700
                )
                    await ctx.send(embed=embed)

            else:
                command.enabled = not command.enabled
                ternary = "Enabled" if command.enabled else "Disabled"
                embed = discord.Embed(
                    title = f"I Have **{ternary}** ``{command.qualified_name}`` for you!",
                    color = 0xff7700
                )
                await ctx.send(embed=embed)

        @commands.command(name="eval", aliases=["exec"])
        @commands.is_owner()
        async def _eval(self,ctx, *, code):
            code = clean_code(code)

            local_variables = {
                "discord": discord,
                "commands": commands,
                "bot": self.bot,
                "ctx": ctx,
                "channel": ctx.channel,
                "author": ctx.author,
                "guild": ctx.guild,
                "message": ctx.message
            }

            stdout = io.StringIO()

            try:
                with contextlib.redirect_stdout(stdout):
                    exec(
                        f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                    )

                    obj = await local_variables["func"]()
                    result = f"{stdout.getvalue()}\n-- {obj}\n"
            except Exception as e:
                result = "".join(format_exception(e, e, e.__traceback__))

            pager = Pag(
                timeout=100,
                entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
                length=1,
                prefix="```py\n",
                suffix="```"
            )

            await pager.start(ctx)

        # part of the snipe command
        @commands.command()
        @commands.is_owner()
        async def catch_snipes(self, ctx):
            try:
                with open('settings/snipe.json') as snipeFile:
                    snipes = json.load(snipeFile)
                    guilds = []
                    for x in snipes:
                        guilds.append(x['id'])
            except Exception as e:
                print(e)

            for y in ctx.bot.guilds:
                if y.id not in guilds:
                    try:
                        with open('settings/snipe.json') as snipeFile:
                            snipes = json.load(snipeFile)
                    except Exception as e:
                        print(e)

                    newGuild = {
                        "id": y.id,
                        "author_avatar": "",
                        "content": "",
                    } 
                    snipes.append(newGuild)
                    
                    embed = discord.Embed(
                        title = "Done!",
                        color = 0xff7700
                    )
                    await ctx.send(embed=embed)

                    try:
                        with open('settings/snipe.json', 'w') as outfile:
                            json.dump(snipes, outfile, indent=4)
                    except Exception as e:
                        print(e)

        # get server info command
        @commands.command(aliases=["gsi"])
        @commands.is_owner()
        async def getserverinfo(self, ctx, *, guild_id: int):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send("Hmph.. I got nothing..")
            members = set(guild.members)
            bots = filter(lambda m: m.bot, members)
            bots = set(bots)
            members = len(members) - len(bots)

            if guild == ctx.guild:
                roles = " ".join([x.mention for x in guild.roles != "@everyone"])
            else:
                roles = ", ".join([x.name for x in guild.roles if x.name != "@everyone"])

            embed = discord.Embed(
                title=f"**Guild info:** ``{guild.name}``",
                color = 0xff7700,
                timestamp=ctx.message.created_at
            )
            embed.add_field(name="**Owner:**", value=f"{guild.owner}\n{guild.id}", inline=True)
            embed.add_field(name="**Owner Nick:**", value=f"{guild.owner.nick}", inline=True)
            embed.add_field(name="**Owner Status:**", value=f"{guild.owner.status}", inline=True)
            embed.add_field(name="**Members/Bots:**", value=f"{members}:{len(bots)}", inline=True)
            embed.add_field(name="**Created at:**", value=guild.created_at.__format__('%A, %d. %B %Y'), inline=True)
            embed.add_field(name="**Region:**", value=f"{guild.region}", inline=True)
            embed.add_field(name="**Channels:**", value=len(guild.channels), inline=True)
            embed.add_field(name="**Voice Channels:**", value=len(guild.voice_channels), inline=True)
            embed.add_field(name="**Boosters:**", value=guild.premium_subscription_count, inline=True)
            embed.add_field(name="**Highest role:**", value=guild.roles[-1], inline=True)
            embed.add_field(name="**Verification Level:**", value=str(guild.verification_level), inline=True)
            embed.add_field(name="**Number of emotes:**", value=len(guild.emojis), inline=True)
            embed.add_field(name="**Number of roles:**", value=len(guild.roles), inline=True)
            embed.add_field(name="**Roles:**", value=f"{roles}", inline=True)
            embed.set_footer(text=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=guild.icon_url)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(devlopment(bot))
