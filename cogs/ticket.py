# from http import client
import discord
import datetime
from discord.ext import commands
from discord_components import Button, Select, SelectOption, ComponentsBot, interaction
from discord_components.component import ButtonStyle

#Bot prefix
# commands = ComponentsBot(help_command=None)

id_category = 1000072636082167898#put here the id of the category where the bot will create the ticket channels
id_channel_ticket_logs =1005342986651054110 #put here the id of the channel where the bot will create the ticket logs
id_staff_role = 1005390653192146985#put here the id of the staff role
embed_color = discord.Color.from_rgb(255, 255, 255) #put here a hex color that will carry all the embeds sent by the bot

class ticket(commands.Cog):
    def __init__(self , client) :
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready to support ✅')

    #Ticket command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticket(self,ctx):
        await ctx.message.delete()

        #Embed title and descriptiony
        embed = discord.Embed(title ='Create Ticket If ', description ='Welcome to tickets system.', color=embed_color) 

        #Embed image
        embed.set_image(url='https://cdn.discordapp.com/attachments/998878282315485265/1005547863717187644/Hustlers_Zone_2.gif')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/998878282315485265/1001934690619494551/20220726_132253.jpg')

        await ctx.send(
            embed = embed,

            #Embed button
            components = [
                Button(
                    custom_id = 'Ticket',
                    label = "Create a ticket",
                    style = ButtonStyle.green,
                    emoji ='🔧')
            ]
        )

    @commands.Cog.listener()
    async def on_button_click(self,interaction):

        canal = interaction.channel
        canal_logs = interaction.guild.get_channel(id_channel_ticket_logs)

        #Select function
        if interaction.component.custom_id == "Ticket":
            await interaction.send(

                components = [
                    Select(
                        placeholder = "How can we help you?",
                        options = [
                            SelectOption(label="Question", value="question", description='If you have a simple question.', emoji='❔'),
                            SelectOption(label="Help", value="help", description='If you need help from us.', emoji='🔧'),
                            SelectOption(label="Report", value="report", description='To report a misbehaving user.', emoji='🚫'),
                        ],
                        custom_id = "menu")])

        #Call staff function
        elif interaction.component.custom_id == 'call_staff':

            embed_llamar_staff = discord.Embed(description=f"🔔 {interaction.author.mention} has called the staff.", color=embed_color)
            await canal.send(f'<@&{id_staff_role}>', embed=embed_llamar_staff, delete_after= 20)

        #Close ticket function
        elif interaction.component.custom_id == 'close_ticket':

            embed_cerrar_ticket = discord.Embed(description=f"⚠️ Are you sure you want to close the ticket?", color=embed_color)
            await canal.send(interaction.author.mention, embed=embed_cerrar_ticket, 
                            components = [[
                            Button(custom_id = 'close_yes', label = "Yes", style = ButtonStyle.green),
                            Button(custom_id = 'close_no', label = "No", style = ButtonStyle.red)]])

        #Ticket logs function
        elif interaction.component.custom_id == 'close_yes':

            await canal.delete()
            embed_logs = discord.Embed(title="Tickets", description=f"", timestamp = datetime.datetime.utcnow(), color=embed_color)
            embed_logs.add_field(name="Ticket", value=f"{canal.name}", inline=True)
            embed_logs.add_field(name="Closed by", value=f"{interaction.author.mention}", inline=False)
            embed_logs.set_thumbnail(url=interaction.author.avatar)
            await canal_logs.send(embed=embed_logs)


        elif interaction.component.custom_id == 'close_no':
            await interaction.message.delete()

    @commands.Cog.listener()
    async def on_select_option(self,interaction):
        if interaction.component.custom_id == "menu":

            guild = interaction.guild
            category = discord.utils.get(interaction.guild.categories, id = id_category)
            rol_staff = discord.utils.get(interaction.guild.roles, id = id_staff_role)

            #Select option | Question
            if interaction.values[0] == 'question':

                #Creating ticket channel | Question
                channel = await guild.create_text_channel(name=f'❔┃{interaction.author.name}-ticket', category=category)
                
                #Ticket channel permissions | Question
                await channel.set_permissions(interaction.guild.get_role(interaction.guild.id),
                                send_messages=False,
                                read_messages=False)
                await channel.set_permissions(interaction.author, 
                                                    send_messages=True,
                                                    read_messages=True,
                                                    add_reactions=True,
                                                    embed_links=True,
                                                    attach_files=True,
                                                    read_message_history=True,
                                                    external_emojis=True)
                await channel.set_permissions(rol_staff,
                                                    send_messages=True,
                                                    read_messages=True,
                                                    add_reactions=True,
                                                    embed_links=True,
                                                    attach_files=True,
                                                    read_message_history=True,
                                                    external_emojis=True,
                                                    manage_messages=True)
                                                    

                await interaction.send(f'> The {channel.mention} channel was created to solve your questions.', delete_after= 3)

                #Inside the ticket | Question
                #Embed inside the ticket | Question
                embed_question = discord.Embed(title=f'Question - ¡Hi {interaction.author.name}!', description='In this ticket we have an answer to your question.\n\nIf you cant get someone to help you, press the button `🔔 Call staff`..', color=embed_color)
                embed_question.set_thumbnail(url=interaction.author.avatar_url)


                await channel.send(interaction.author.mention, embed=embed_question,
                
                #Embed buttons inside the ticket | Question
                components = [[
                        Button(custom_id = 'close_ticket', label = "Close ticket", style = ButtonStyle.red, emoji ='🔐'),
                        Button(custom_id = 'call_staff', label = "Call staff", style = ButtonStyle.blue, emoji ='🔔')]])


            #Select option | Help
            elif interaction.values[0] == 'help':

                #Creating ticket channel | Help
                channel = await guild.create_text_channel(name=f'🔧┃{interaction.author.name}-ticket', category=category)
                
                #Ticket channel permissions | Help
                await channel.set_permissions(interaction.guild.get_role(interaction.guild.id),
                                send_messages=False,
                                read_messages=False)
                await channel.set_permissions(interaction.author, 
                                                    send_messages=True,
                                                    read_messages=True,
                                                    add_reactions=True,
                                                    embed_links=True,
                                                    attach_files=True,
                                                    read_message_history=True,
                                                    external_emojis=True)
                await channel.set_permissions(rol_staff,
                                                    send_messages=True,
                                                    read_messages=True,
                                                    add_reactions=True,
                                                    embed_links=True,
                                                    attach_files=True,
                                                    read_message_history=True,
                                                    external_emojis=True,
                                                    manage_messages=True)


                await interaction.send(f'> The {channel.mention} channel was created to help you.', delete_after= 3)

                #Inside the ticket | Help
                #Embed inside the ticket | Help
                embed_question = discord.Embed(title=f'Help - ¡Hi {interaction.author.name}!', description='In this ticket we can help you with whatever you need.\n\nIf you cant get someone to help you, press the button `🔔 Call staff`.', color=embed_color)
                embed_question.set_thumbnail(url=interaction.author.avatar_url)


                await channel.send(interaction.author.mention, embed=embed_question, 
                
                #Embed buttons inside the ticket | Help
                components = [[
                        Button(custom_id = 'close_ticket', label = "Close ticket", style = ButtonStyle.red, emoji ='🔐'),
                        Button(custom_id = 'call_staff', label = "Call staff", style = ButtonStyle.blue, emoji ='🔔')]])


            #Select option | Report
            elif interaction.values[0] == 'report':

                #Creating ticket channel | Report
                channel = await guild.create_text_channel(name=f'🚫┃{interaction.author.name}-ticket', category=category)

                #Ticket channel permissions | Report
                await channel.set_permissions(interaction.guild.get_role(interaction.guild.id),
                                send_messages=False,
                                read_messages=False)
                await channel.set_permissions(interaction.author, 
                                                    send_messages=True,
                                                    read_messages=True,
                                                    add_reactions=True,
                                                    embed_links=True,
                                                    attach_files=True,
                                                    read_message_history=True,
                                                    external_emojis=True)
                await channel.set_permissions(rol_staff,
                                                    send_messages=True,
                                                    read_messages=True,
                                                    add_reactions=True,
                                                    embed_links=True,
                                                    attach_files=True,
                                                    read_message_history=True,
                                                    external_emojis=True,
                                                    manage_messages=True)


                await interaction.send(f'> The {channel.mention} channel was created to report to the user.', delete_after= 3)

                #Inside the ticket | Report
                #Embed inside the ticket | Report
                embed_question = discord.Embed(title=f'Report - ¡Hi {interaction.author.name}!', description='In this ticket we can help you with your report.\n\nIf you cant get someone to help you, press the button `🔔 Call staff`.', color=embed_color)
                embed_question.set_thumbnail(url=interaction.author.avatar_url)

                await channel.send(interaction.author.mention, embed=embed_question, 
                
                #Embed buttons inside the ticket | Report
                components = [[
                        Button(custom_id = 'close_ticket', label = "Close ticket", style = ButtonStyle.red, emoji ='🔐'),
                        Button(custom_id = 'call_staff', label = "Call staff", style = ButtonStyle.blue, emoji ='🔔')]])

def setup(client):
    client.add_cog(ticket(client))
    print('Ticket Cog Loaded !')