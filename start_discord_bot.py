import discord

from functions import *
from settings import *
from key import *

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!standings') or message.content.startswith('compbot'):
        if s_comp_type == FREE_FOR_ALL:
            await message.channel.send(s_standings_header)
            await message.channel.send(get_current_standings_free_for_all(s_participants, s_comp_skills, s_start_file))
        elif s_comp_type == TWO_TEAMS:
            await message.channel.send('loading...')
            await message.channel.send(get_current_standings_two_teams(s_participants, s_comp_skills, s_start_file, s_team1, s_team2))
        else:
            await message.channel.send('The s_comp_type in settings.py is invalid')

    if message.content.startswith('!help'):
        str = 'use "!standings" or "compbot do the thing" to print current standings for the competition'
        await message.channel.send(str)


client.run(DISCORD_KEY)
