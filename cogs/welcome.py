from datetime import datetime
# from dis import disco
# from unicodedata import name
import discord
from discord.ext import commands


class welcome(commands.Cog):
    def __init__(self , client) :
        self.client = client


    @commands.Cog.listener()
    async def on_member_join(self,member):
        guild = self.client.get_guild(1000069323932577884)
        # await member.add_roles(guild.get_role(998456579630313493))
        channel = self.client.get_channel(1000073612260282378)
        embed = discord.Embed(title='Welcome To The Server👋!',
                              description=f'''**Hello {member.mention} ,**\nWe have multiple roles and different types of\nsub-communities in this server.\n
    like: Gaming,Finance,Trading,Programming,etc.

    More info is inside the server!

    Have a great time here in **Hustler's Zone.**''',
                            color=discord.Color.from_rgb(255, 255, 255))
        embed.set_footer(text='Thanks For Joining🙏!'),
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/attachments/998878282315485265/1001934690619494551/20220726_132253.jpg'
        ),
        embed.set_image(url='https://cdn.discordapp.com/attachments/998878282315485265/1005861636885713036/h1.gif'),
        embed.set_author(
            name="Hustler's Zone",
            icon_url=
    'https://cdn.discordapp.com/attachments/998878282315485265/1001934690619494551/20220726_132253.jpg'
        ),
        embed.add_field(name = "Follow Us😊", value = f":link: [Follow](https://linktr.ee/hustlerszone)")
        await member.send(embed=embed)
        mbed = discord.Embed(
            title=f"Welcome To Hustler's Zone",description='Have A Great Time Here.\nTake Your roles from <#1000459628351602708>',color=discord.Color.from_rgb(255, 255, 255))
        mbed.set_author(
            name="Hustler's Zone",
            icon_url=
    'https://cdn.discordapp.com/attachments/998878282315485265/1001934690619494551/20220726_132253.jpg'
        ),
        mbed.set_image(url='https://cdn.discordapp.com/attachments/998878282315485265/1005861636885713036/h1.gif'),
        mbed.set_footer(text='Thanks For Joining🙏!'),
        mbed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/attachments/998878282315485265/1001934690619494551/20220726_132253.jpg'
        )
        await channel.send(embed = mbed , content = f"Hello👋{member.mention} !")






    @commands.Cog.listener()
    async def on_member_remove(self,member):
        logchannel = self.client.get_channel(1005342986651054110)
        leavembed = discord.Embed(
            title= 'Member Left',description=f"{member.mention} has left the server.",
            color= discord.Color.from_rgb(255, 0, 0))
        # leavembed.set_thumbnail({member.avatar})
        # leavembed.set_footer({datetime})
        await logchannel.send(embed = leavembed)
        dmleave = discord.Embed(
            title='You left our community?',
            description='We are sad because you left our community.\n\nOur Community Is Always Open For You,\nDo Join Again !\nWe are waiting for you.\nHave a nice day !\n\nAnd Do Provide Us reason Why You Left our Community by dming us **$modmail <reason>**\n\n**Note : If you are kicked or have been banned you should have recived one more message if not ignore this paragraph.**\n\nInvite Link Is Given Below If you wanna rejoin.',
            color= discord.Color.from_rgb(255, 0, 0))
        dmleave.add_field(name = "Invite Link", value = f":link: [Follow](https://discord.gg/2NWmKEVYnT)")
        dmleave.set_footer(text='😥!')
        # dmleave.set_thumbnail(url='https://tenor.com/view/sad-sad-eyes-sad-face-%C3%BCzg%C3%BCn-%C3%BCzg%C3%BCn-y%C3%BCz-gif-20234977')
        # dmleave.set_image(url='https://tenor.com/view/sad-gif-23929551')
        await member.send(embed=dmleave)
        
def setup(client):
    client.add_cog(welcome(client))
    print('Welcome Cog Loaded !')
