# from http import client
import random
import discord
import secrets
import asyncio
import aiohttp

from io import BytesIO
from discord.ext import commands
# from utils import permissions, http, default


class Fun_Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        # self.config = default.config()


    @commands.command()
    async def thank(self, ctx, member : discord.Member, *, reason = None):
        if reason == None:
            await ctx.send(f"{ctx.author.mention} thanked {member.mention} for no reason at all!")
        else:
            await ctx.send(f"{ctx.author.mention} thanks {member.mention} for {reason} reason.")
        try:
            if reason != None:
                await member.send(f"You were thanked in {ctx.guild.name} by {ctx.author.name}!\nReason: {reason}")
            else:
                await member.send(f"You were thanked in {ctx.guild.name} by {ctx.author.name}")
        except:
            pass

    @commands.command(aliases=["flip", "coin"])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ["Heads", "Tails"]
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    async def payrespect(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")


    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        """ Generates a random password string for you

        This returns a random URL-safe text string, containing nbytes random bytes.
        The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.
        """
        if nbytes not in range(3, 1401):
            return await ctx.send("I only accept any numbers between 3-1400")
        if hasattr(ctx, "guild") and ctx.guild is not None:
            await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
        await ctx.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")

    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        rate_amount = random.uniform(0.0, 100.0)
        await ctx.send(f"I'd rate `{thing}` a **{round(rate_amount, 4)} / 100**")

    @commands.command()
    async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Give someone a beer! 🍻 """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.client.user.id:
            return await ctx.send("*drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")

        beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
        beer_offer = f"{beer_offer}\n\n**Reason:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.client.wait_for("raw_reaction_add", timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            beer_offer = f"{beer_offer}\n\n**Reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command(aliases=["howhot", "hot"])
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 75:
            emoji = "💞"
        elif hot > 50:
            emoji = "💖"
        elif hot > 25:
            emoji = "❤"
        else:
            emoji = "💔"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")


    @commands.command(aliases=["slots", "bet"])
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a, b, c = [random.choice(emojis) for g in range(3)]
        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")


    @commands.command()
    async def poll(self, ctx, *, message):
        embed = discord.Embed(title = f"{ctx.author.name}'s Poll", color = ctx.author.color)
        embed.add_field(name = f"{message}", value = "Share your thoughts about this topic")

        my_msg = await ctx.send(embed = embed)
        await my_msg.add_reaction("✅")
        await my_msg.add_reaction("❌")

    @commands.command(aliases = ['str', 'show_tp', 's_toprole'])
    async def show_toprole(self, ctx, *, member: discord.Member=None):
        if member is None:
            member = ctx.author
            await ctx.send(f'The top role for {member.display_name} is {member.top_role.name}')
        else:
            await ctx.send(f'The top role for {member.display_name} is {member.top_role.name}')

   
    @commands.command(aliases = ["av"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member == None:
            em = discord.Embed(description=f"[**{ctx.author.name}'s Avatar**]({ctx.author.avatar})", colour=ctx.author.color, timestamp =ctx.message.created_at)
            em.set_image(url= ctx.author.avatar)
            em.set_footer(icon_url = ctx.author.avatar, text = f"Requested by {ctx.author}")

            await ctx.send(embed=em)

            return

        else:
            em = discord.Embed(description=f"[**{member.name}'s Avatar**]({member.avatar})", colour = member.color, timestamp =ctx.message.created_at)
            em.set_image(url=member.avatar)
            em.set_footer(icon_url = member.avatar, text = f"Requested by {ctx.author}")
            await ctx.send(embed=em)

            return


def setup(client):
    client.add_cog(Fun_Commands(client))