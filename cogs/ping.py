import imp
import discord
from discord.ext import commands 
import interactions

Hustler = '<@&1000076202255585341>'

class ping(commands.Cog):
    def __init__(self , client) :
        self.client = client




def setup(client):
    client.add_cog(ping(client))
    print('Ping Cog Loaded !')


#     client = interactions.Client(
#     token="your_secret_bot_token",
#     default_scope=the_id_of_your_guild,
# )