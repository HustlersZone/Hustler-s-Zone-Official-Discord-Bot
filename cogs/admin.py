import time
import aiohttp
import discord , asyncio
import importlib
import os
import sys
import json
from datetime import datetime
from discord.ext import commands
# from discord.utils import 


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, user: discord.User, *, message: str):
        """ DM the user of your choice """
        try:
            await user.send(message)
            await ctx.send(f"✉️ Sent a DM to **{user}**")
        except discord.Forbidden:
            await ctx.send("This user might be having DMs blocked or it's a bot account...")



    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def report(self, ctx, *, msg):
        await ctx.message.delete()

        channel = self.client.get_channel(1005342986651054110)
        staff = discord.utils.get(ctx.guild.roles, id=1000076202255585341)

        embed = discord.Embed(colour=discord.Colour.from_rgb(255,255,0))

        embed.add_field(name=f'__**Report:**__', value=f"<@{ctx.author.id}> Reported:", inline=False)
        embed.add_field(name=msg, value="­")
        embed.set_footer(text=f"ID: {ctx.message.author.id}")

        await channel.send(staff.mention, embed=embed)
        await ctx.author.send("Your report has been sent successfully! Action will be taken accordingly.")



    @commands.has_permissions(administrator=True)
    @commands.command(name="setstatus")
    async def set_status(self, ctx, status: str = None):
        '''
        Changes the status message of the bot.
        Usage: !setstatus [status]
        '''
        if status is None:
            await ctx.send("No status was recevied. Status is unchanged.")
            return
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(status)
        )
        await ctx.send("Bot status has been changed!")



# ---------------------------------------------------------------------------------
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self,ctx, member: discord.Member, *, reason=None):

        if str(ctx.author) != member:
            if reason == None:
                reason = 'No Reason Provided'

            mbed = discord.Embed(
                title=f'You Have Been Kicked From {ctx.guild.name}',
                timestamp=datetime.utcnow(),
                color=discord.Color.red())

            mbed.add_field(name="Reason", value=reason, inline=True)

            await ctx.send(f'Kicked {member} for {reason}')

            #this is because some people has message dm disable
            try:
                await member.send(embed=mbed)
            except:
                pass
            await member.kick(reason=reason)
        else:
            await ctx.send(f"{ctx.author.mention} You Can't Kick YourSelf!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self,ctx, member: discord.Member, *, reason=None):

        if str(ctx.author) != member:
            if reason == None:
                reason = 'No Reason Provided'

            mbed = discord.Embed(
                title=f'You Have Been Banned From {ctx.guild.name}',
                timestamp=datetime.utcnow(),
                color=discord.Color.red())

            mbed.add_field(name="Reason", value=reason, inline=True)

            await ctx.send(f'Banned {member} for {reason}')

            try:
                await member.send(embed=mbed)
            except:
                pass
                
            await member.ban(reason=reason)
        else:
            await ctx.channel.send(
                f"{ctx.author.mention} You Can't Ban YourSelf!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self,ctx, member):
        banned_users = ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(
                    f'Unbanned {user.name}#{user.discriminator}')
                return

    @commands.command(name="mute")
    @commands.has_permissions(administrator=True)
    async def mute(self,ctx, member: discord.Member, *, reason=None):
        if str(ctx.author) != member:
            guild = ctx.guild
            mutedRole = discord.utils.get(guild.roles, name="Muted")

            #this is for creating muted role if already not created
            if not mutedRole:
                mutedRole = await guild.create_role(name="Muted")

                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False)

            mbed = discord.Embed(title=f'You Have Been Muted In {ctx.guild.name}',
                                    timestamp=datetime.utcnow(),
                                    color=discord.Color.red())

            mbed.add_field(name="Reason", value=reason, inline=True)

            await member.add_roles(mutedRole, reason=reason)
            await ctx.send(f'Muted {member.mention} for reason {reason}')

            try:
                await member.send(embed=mbed)
            except: 
                pass
            else:
                await ctx.channel.send(f"{member.mention} You Can't Mute Yourself!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self,ctx, member: discord.Member):

        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        mbed = discord.Embed(title=f'You Have Been Unmuted In {ctx.guild.name}',
                                timestamp=datetime.utcnow(),
                                color=discord.Color.red())

        await member.remove_roles(mutedRole)
        await ctx.send(f'Unmuted {member.mention}')

        try:
            await member.send(embed=mbed)
        except:
            pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def temp_mute(self,ctx, member: discord.Member, seconds: int):

        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.add_roles(mutedRole)
        await asyncio.sleep(seconds)
        await member.remove_roles(mutedRole)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn_user(self,ctx, member: discord.Member, *, reason=None):

        try:
            mbed = discord.Embed(title='You Have Been Warned ',
                                    color=discord.Color.red())
            mbed.add_field(name="Reason", value=reason, inline=True)
            await member.send(embed=mbed)
            await ctx.channel.send(member.mention + ' Has Been Warned!')
        except:
            await ctx.channel.send("Couldn't Dm The Given User")

    #if you want to remove slowmode then just use this command with slow mode of 0
    @commands.command(name="slowmode", aliases=["sm"])
    @commands.has_permissions(administrator=True)
    async def slowmode(self,ctx, sm: int, channel=None):
        if channel is None:
            channel = ctx.channel
        if sm < 0:
            await ctx.send("Slow Mode Should be 0 or Positive")
            return
        else:
            await channel.edit(slowmode_delay=sm)

    #this will lock the channel so that no user can send any message
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lock(self,ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f'Locked #{channel}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlock(self,ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f'Unlocked #{channel}')

    @commands.command(aliases = ["purge", "massdelete", "bulkdel"])
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount = 1):
        await ctx.channel.purge(limit = amount)
        
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error):
            embed = discord.Embed(title = "<:fail:761292267360485378> Purge Failed!", color = ctx.author.color)
            embed.add_field(name = "Reason:", value = f"`Manage Messages Permissions Missing!`")
            await ctx.send(embed = embed)



def setup(client):
    client.add_cog(Admin(client))