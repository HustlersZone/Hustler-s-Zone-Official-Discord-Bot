import discord
import asyncio
from discord.ext import commands
# from Ticket.reaction import Reaction
import discord
import random
import asyncio
import datetime
from discord.ext import commands
from discord.utils import get
from time import strftime
from datetime import datetime



MESSAGE_ID = 1005389116428533820
ROLE_ID = 1005465085554217011
CATEGORY_ID = 1000072636082167898
BOT_ID = 999573905008246864
LOG_CHANNEL_ID = 1005342986651054110

class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
    channel_ticket = None
    ticket_creator = None

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticket3(self, ctx):
        title = "Would you like to create a ticket?"
        description = "If you have a question or concern, please create a ticket by clicking on the 📩 emoji."
        name = "If you have any general questions about the ticket system please contact a supporter!" 

        embed = discord.Embed(title=title, description=description, color=0x2f2fd0)
        embed.add_field(name="General questions!", value=name, inline=True)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/771635939700768769/773121323341578250/external-content.duckduckgo.com.png")
        embed.set_author(name="Hustler's Zone Bot")

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("📩")
        await ctx.message.delete()



    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild_id = payload.guild_id
        guild = self.client.get_guild(guild_id)
        user_id = payload.user_id
        user = self.client.get_user(user_id)
        message_id = payload.message_id
        channel = self.client.get_channel(payload.channel_id)

        # TICKETS
        emoji = payload.emoji.name
        
        if message_id == MESSAGE_ID and emoji == "📩":

            self.ticket_creator = user_id

            message = await channel.fetch_message(message_id)
            await message.remove_reaction("📩",user)

            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            support_role = guild.get_role(ROLE_ID)
            category = guild.get_channel(CATEGORY_ID)
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                support_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            ticket_nr = random.randint(100,999)
            self.channel_ticket = await category.create_text_channel(f'ticket-{ticket_nr}', overwrites=overwrites)

            embed = discord.Embed(
                title="How can we help you?",
                description="A supporter will take care of you as soon as possible.\n\n:white_check_mark: - Claim the ticket\n:no_entry: - Inform the supporters about your ticket\n:lock: - Close the ticket", 
                color=0x0000ff)
            embed.set_author(name="TiLiKas Ticket Bot")
            embed.set_image(url="https://cdn.discordapp.com/attachments/762902708319420439/769130943762923590/unknown.png")

            msg = await self.channel_ticket.send(embed=embed)

            await msg.add_reaction("✅")
            await msg.add_reaction("⛔")
            await msg.add_reaction("🔒")
        
        if channel == self.channel_ticket and emoji == "⛔" and user_id != BOT_ID:
            
            message = await channel.fetch_message(message_id)
            await message.remove_reaction("⛔",user)

            await channel.send(f"The ticket ``{self.channel_ticket}`` is now unprocessed for more than 10 minutes! <@&ROLE_ID>")

        if channel == self.channel_ticket and emoji == "🔒" and user_id != BOT_ID:
            
            message = await channel.fetch_message(message_id)
            await message.remove_reaction("🔒",user)

            now = datetime.now()   
            time = now.strftime(str("%d.%m.%Y") + " at " + str("%H:%M"))

            channel_log = self.client.get_channel(LOG_CHANNEL_ID)
            text = f"The ticket ``{self.channel_ticket}`` was closed by {user.mention} on {time}"

            embed = discord.Embed(
                title = "Closed Ticket",
                description = text,
                color = 0x0000ff)

            await channel_log.send(embed=embed)

            embed = discord.Embed(
                title = "Ticket closed!",
                description = f":tickets: The ticket was just closed by {user.mention}.",
                color = 0x0000ff)

            await channel.send(embed=embed)

            await asyncio.sleep(10)

            await channel.delete()

        if channel == self.channel_ticket and emoji == "✅" and user_id != BOT_ID:

            message = await channel.fetch_message(message_id)
            await message.remove_reaction("✅",user)

            if self.ticket_creator == user_id:

                embed = discord.Embed(
                    title = "You cant claim the ticket!",
                    color = 0x0000ff)
                embed.set_author(name="TiLiKas Ticket Bot")

                await channel.send(embed=embed)

            else:

                embed = discord.Embed(
                    title = "Ticket claimed!",
                    description = f"The ticket was claimed by {user.mention}.",
                    color = 0x0000ff)
                embed.set_author(name="TiLiKas Ticket Bot")

                await channel.send(embed=embed)



        
def setup(client):
    client.add_cog(AdminCommands(client))