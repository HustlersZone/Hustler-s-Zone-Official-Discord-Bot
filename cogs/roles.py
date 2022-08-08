# from http import client
# from http import client
import json
import os
from pickle import TRUE
import platform
from datetime import datetime

import discord
from discord.ext import commands
from discord_components import *


with open("data\setting.json", 'r', encoding='utf-8') as _settings_data:
    settings = json.load(_settings_data)


class roles(commands.Cog):
    def __init__(self , client) :
        self.client = client

    # @commands.Cog.listener()
    # async def on_ready():
    #     print(f'Discord.py API version: {discord.__version__}')
    #     print(f'Python version: {platform.python_version()}')
    #     # print(f'Logged in as {bot.user} | {bot.user.id}')
    #     print("Bot is ready to be used!")


    @commands.command(name="selfrole")
    @commands.has_permissions(administrator = True)
    async def self_role(self,ctx):
        await ctx.channel.purge(limit=2)
        emojis = []
        roles = []
        for role in settings['roles']:
            roles.append(role['role'])
            emojis.append(role['emoji'])
        channel = self.client.get_channel(int(settings['channel_id']))

        bot_msg = await channel.send(settings['message'])
        

        with open("data/reactions.json", "r") as f:
            self_roles = json.load(f)

        self_roles[str(bot_msg.id)] = {}
        self_roles[str(bot_msg.id)]["emojis"] = emojis
        self_roles[str(bot_msg.id)]["roles"] = roles

        with open("data/reactions.json", "w") as f:
            json.dump(self_roles, f)

        for emoji in emojis:
            await bot_msg.add_reaction(emoji)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        msg_id = payload.message_id

        with open("data/reactions.json", "r") as f:
            self_roles = json.load(f)

        if payload.member.bot:
            return

        if str(msg_id) in self_roles:
            emojis = []
            roles = []

            for emoji in self_roles[str(msg_id)]['emojis']:
                emojis.append(emoji)

            for role in self_roles[str(msg_id)]['roles']:
                roles.append(role)

            guild = self.client.get_guild(payload.guild_id)
            log_channel = self.client.get_channel(int(settings['log_channel_id']))

            for i in range(len(emojis)):
                choosed_emoji = str(payload.emoji)
                if choosed_emoji == emojis[i]:
                    selected_role = roles[i]

                    role = discord.utils.get(guild.roles, name=selected_role)

                    await payload.member.add_roles(role)
                    await payload.member.send(f"Added **{selected_role}** Role!")
                    await log_channel.send(f'`{datetime.now()}` - Added {selected_role} role to <@{payload.member.id}>')


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        msg_id = payload.message_id

        with open("data/reactions.json", "r") as f:
            self_roles = json.load(f)

        if str(msg_id) in self_roles:
            emojis = []
            roles = []

            for emoji in self_roles[str(msg_id)]['emojis']:
                emojis.append(
                    emoji)

            for role in self_roles[str(msg_id)]['roles']:
                roles.append(role)

            guild = self.client.get_guild(payload.guild_id)
            log_channel = self.client.get_channel(int(settings['log_channel_id']))

            for i in range(len(emojis)):
                choosed_emoji = str(payload.emoji)
                if choosed_emoji == emojis[i]:
                    selected_role = roles[i]
                    role = discord.utils.get(guild.roles, name=selected_role)
                    member = await(guild.fetch_member(payload.user_id))
                    if member is not None:
                        await member.remove_roles(role)
                        await member.send(f"Removed **{selected_role}** Role!")
                        await log_channel.send(f'`{datetime.now()}` - Removed {selected_role} role from <@{member.id}>')


def setup(client):
    client.add_cog(roles(client))
    print('roles Cog Loaded !')