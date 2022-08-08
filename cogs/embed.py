import asyncio
import discord , time
from discord.ext import commands 
import interactions

Hustler = '<@&1000076202255585341>'

class embed(commands.Cog):
    def __init__(self , client) :
        self.client = client

    @commands.command(name="test")
    async def test(self,ctx):
            message = 'Hi'
            msg = await ctx.send(message)
            await ctx.message.delete() # Deletes the users message
            await asyncio.sleep(5) # you want it to wait.
            # await message.delete() # Deletes the message the bot sends.
    
    
    
    @commands.command()
    async def embed(self,message):
        embed = discord.Embed(title='Welcome To The Server!',
                          description=f'''**Hello ,**
We have multiple roles and different types of sub-communities in this server.
like: Gaming,Finance,Trading,Programming,etc.

More info is inside the server!

Have a great time here in **Hustler's Zone.**''',
                          color=discord.Color.from_rgb(255, 255, 255))
        embed.set_footer(text='Thanks For Joining !'),
        embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/attachments/998878282315485265/1001934690619494551/20220726_132253.jpg'
    ),
        embed.set_author(
        name="Hustler's Zone",
        icon_url=
        'https://cdn.discordapp.com/attachments/998878282315485265/1001934690619494551/20220726_132253.jpg'
    ),
        embed.add_field(name='Follow Us',
                    value='https://linktr.ee/hustlerszone',
                    inline=False)
        await message.channel.send(content = f'Hello {Hustler}',embed=embed)



    

def setup(client):
    client.add_cog(embed(client))
    print('embed Cog Loaded !')







    