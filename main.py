from dis import disco
from email import message
import discord , configs , os , json
from discord.ext import commands 
from discord_components import *

client = commands.Bot(command_prefix='$', intents=discord.Intents.all())
print('Command Prefix = "$"')
client.remove_command('help')


# channel = client.get_channel('1005342986651054110')

@client.command()
async def load(ctx,extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

for filename in os.listdir('./Economy'):
    if filename.endswith('.py'):
        client.load_extension(f'Economy.{filename[:-3]}')

# for filename in os.listdir('./Ticket'):
#     if filename.endswith('.py'):
#         client.load_extension(f'Ticket.{filename[:-3]}')

#events    
@client.event
async def on_ready():
    print('Hey Sanchit , Your Community Bot Is Online !')  
    await client.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, name='Hustlers Zone'),status=discord.Status.idle)
    print('We have logged in as {0.user}\n🟢Online/Up'.format(client))

client.run(configs.TOKEN)