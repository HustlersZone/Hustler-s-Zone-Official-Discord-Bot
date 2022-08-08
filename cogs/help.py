#help command 
import discord , os
from discord.ext import commands 

#help command 

class help(commands.Cog):
    def __init__(self , client) :
        self.client = client

    @commands.command(aliases = ['commandinfo'])
    async def help(self,ctx):
        if ctx.author.guild_permissions.administrator:
            publicembed = discord.Embed(title="Commands.",description='We Have Categorized Bot Commands.',color=discord.Color.from_rgb(255, 255, 255))
            publicembed.set_footer(text='Made With ❤️ By SANCHITSHARMA#2003')
            publicembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/998878282315485265/1001934690619494551/20220726_132253.jpg')
            publicembed.set_image(url='https://cdn.discordapp.com/attachments/998878282315485265/1005861636885713036/h1.gif')
            publicembed.set_author(name="Hustler's Zone™️" , icon_url='https://cdn.discordapp.com/attachments/998878282315485265/1001934690619494551/20220726_132253.jpg')
            publicembed.add_field(name='Admin Commands 🔴.',value='selfrole , ban , unban , dm , clear , kick , lock , unlock , setstatus , slowmode , mute , unmute , warn_user , load , unload , respond.' , inline=False)
            publicembed.add_field(name='Economy 🪙. ',value='balance , beg , daily , deposit , send , weekly , withdraw , give_coins , remove_coins.')
            publicembed.add_field(name='Fun 🎉.',
                        value='avatar , beer , coinflip , payrespect , hotcalc , password , poll , rate , show_toprole , slot , thank .',
                        inline= False)
            publicembed.add_field(name = 'Ticket📧.', value='helpticket , ticket , new (You can use this command to create channel for some imp thing.)',inline=False)
            publicembed.add_field(name='Info❔.' , value= 'channelinfo , serverinfo , ping , userinfo.',inline= True)
            publicembed.add_field(name='Giveaways🎁.',value='gstart , reroll.',inline= True)
            publicembed.add_field(name='Uncategorized.',value='invite',inline=False)
            publicembed.add_field(name = "Follow Us😊", value = f":link: [Follow](https://linktr.ee/hustlerszone)")
            await ctx.channel.send(embed = publicembed)
            
        else : 
            publicembed = discord.Embed(title="Commands.",description='We Have Categorized Bot Commands.',color=discord.Color.from_rgb(255, 255, 255))
            publicembed.set_footer(text='Made With ❤️ By SANCHITSHARMA#2003')
            publicembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/998878282315485265/1001934690619494551/20220726_132253.jpg')
            publicembed.set_image(url='https://cdn.discordapp.com/attachments/998878282315485265/1005861636885713036/h1.gif')
            publicembed.set_author(name="Hustler's Zone™️" , icon_url='https://cdn.discordapp.com/attachments/998878282315485265/1001934690619494551/20220726_132253.jpg')
            publicembed.add_field(name='Economy 🪙. ',value='balance , beg , daily , deposit , send , weekly , withdraw , give_coins , remove_coins.')
            publicembed.add_field(name='Fun 🎉.',
                        value='avatar , beer , coinflip , payrespect , hotcalc , password , poll , rate , show_toprole , slot , thank .',
                        inline= False)
            publicembed.add_field(name = 'Ticket📧.', value='new (You can use this command to create channel to contact staff.)',inline=False)
            publicembed.add_field(name='Info❔.' , value= 'channelinfo , serverinfo , ping , userinfo.',inline= True)
            # publicembed.add_field(name='Giveaways🎁.',value='gstart , reroll.',inline= True)
            publicembed.add_field(name='Uncategorized.',value='invite',inline=False)
            publicembed.add_field(name = "Follow Us😊", value = f":link: [Follow](https://linktr.ee/hustlerszone)")
            await ctx.channel.send(embed = publicembed)


def setup(client):
    client.add_cog(help(client))
    print('Help Cog Loaded !')


