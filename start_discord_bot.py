import discord

from functions import *

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Start comp: valid only if used by Alex, Ned, or Sandor
    # if ((message.author.name == 'Riunn' or message.author.name == 'Mrawr' or message.author.name == 'ColonelSanders')
    #     and message.content.startswith('!start comp')):
    #     await message.channel.send('Valid admin, but competitions are not set up yet')

    if message.content.startswith('!standings') or message.content.startswith('compbot'):
        # await message.channel.send(standings_header)
        # await message.channel.send(get_current_standings(participants, comp_skill, start_file))
        await message.channel.send('loading...')
        await message.channel.send(get_current_standings_one_skill_two_teams(participants, comp_skill, start_file, team1, team2))

    if message.content.startswith('!help'):
        str = 'use "!standings" or "compbot do the thing" to print current standings for the competition'
        await message.channel.send(str)


# client.run(DISCORD_KEY)