import requests
import os
import sys
import discord

from key import *

# If xp is -1 will have to skip over, doesn't have reqs or is at 0 xp

# Constants for request parsing
OVERALL = 1
ATTACK = 2
DEFENCE = 3
STRENGTH = 4
CONSTITUTION = 5
RANGED = 6
PRAYER = 7
MAGIC = 8
COOKING = 9
WOODCUTTING = 10
FLETCHING = 11
FISHING = 12
FIREMAKING = 13
CRAFTING = 14
SMITHING = 15
MINING = 16
HERBLORE = 17
AGILITY = 18
THIEVING = 19
SLAYER = 20
FARMING = 21
RUNECRAFTING = 22
HUNTER = 23
CONSTRUCTION = 24
SUMMONING = 25
DUNGEONEERING = 26
DIVINATION = 27
INVENTION = 28
ARCHEOLOGY = 29

NUM_SKILLS = 29

# The template for a player stat request
STAT_REQUEST = 'https://secure.runescape.com/m=hiscore/index_lite.ws?player='

# Return a list of clanmates with their current xp in each skill
def get_current_xp_all(clanmates):
    # Get list of Acorn clanmates
    # clanmate_res = requests.get('http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName=Acorn')
    # clanmate_split = clanmate_res.text.split("\n")
    # c_split_length = len(clanmate_split)

    all_cm_data = []

    # Get the list of clanmates in Acorn
    # for i in range(c_split_length):
    #     if i != 0:
    #         clanmates.append(clanmate_split[i].split(",")[0])

    # Add in any eternal guests
    # clanmates.append('Fairytale')

    # Make sure there are no empty strings
    # while '' in clanmates:
    #     clanmates.remove('')

    # Store the number of people in the clanmate list
    clanmate_length = len(clanmates)

    # Replace any weird space characters with the right one
    for i in range(clanmate_length):
        clanmates[i] = clanmates[i].replace(u'\xa0', u' ')

    # For each clanmate get current xp for every skill [rsn, overall, attack, ...]
    for i in range(clanmate_length):
        cm_data = [clanmates[i]]

        # Get user data from api
        req = requests.get(STAT_REQUEST + clanmates[i])

        # If the user isn't active, api returns 404, skip it
        if req.status_code == 404:
            continue

        # Add each skill xp data point to the clanmate
        cm_stats = req.text.split("\n")
        for i in range(NUM_SKILLS):
            cm_data.append(cm_stats[i].split(",")[2])

        # Add the clanmate with their data to the list of clanmates
        all_cm_data.append(cm_data)

    # Turn any numeric strings into ints
    for i in range(len(all_cm_data)):
        for j in range(len(all_cm_data[i])):
            if (all_cm_data[i][j].isnumeric()):
                all_cm_data[i][j] = int(all_cm_data[i][j])

    return all_cm_data

# Stores formatted clanmate xp data in the specified file
def store_xp_in_file(list, fname):
    # Get current path and open the passed in file
    wd = os.path.dirname(__file__)
    path = os.path.join(wd, fname)
    f = open(path, 'r+')

    # Replace spaces in names with _
    for i in range(len(list)):
        list[i][0] = list[i][0].replace(' ', '_')

    # for i in range(clanmate_length):
    #     clanmates[i] = clanmates[i].replace(u'\xa0', u' ')

    # Check if the file is empty, if it isn't, don't touch it
    if (f.read() != ''):
        print('File already has contents, choose a new file.')
        sys.exit()

    # Print the clan data to the file
    for i in range(len(list)):
        for j in range(len(list[i])):
            print(list[i][j], end=' ', file=f)
        print('', file=f)

    f.close()
    return

# Returns a formatted list of clanmate xp data
def pull_xp_from_file(fname):
    # Get current path and open the passed in file
    wd = os.path.dirname(__file__)
    path = os.path.join(wd, fname)
    f = open(path, 'r+')

    # Read data from file
    data = f.read()

    # Split data into clanmate sections
    data = data.split('\n')

    # Split clanmate sections into a name and list of xp
    for i in range(len(data)):
        data[i] = data[i].split(' ')

    # Get rid of empty spaces and arrays
    for i in range(len(data)):
        while '' in data[i]:
            data[i].remove('')

    while [] in data:
        data.remove([])

    # Convert all ints in strings to int types
    for i in range(len(data)):
        for j in range(len(data[i])):
            if (data[i][j].isnumeric()):
                data[i][j] = int(data[i][j])

    # Turn all _ in names to spaces
    for i in range(len(data)):
        data[i][0] = data[i][0].replace('_', u' ')

    f.close()
    return data

# TODO -1's should all be changed to 0's
# Returns a list with all xp gained
def calc_xp_gained(old, new):
    results = []
    ares = []

    # For every element in the original list find the matching name in the new list
    for e_o in old:
        for e_n in new:
            if e_o[0] == e_n[0]:
                ares.append(e_o[0])
                for i in range(1, len(e_n)):
                    # If they haven't started the skill set xp to 0
                    if (e_n[i] == '-1'):
                        ares.append(0)
                    # If they started the skill during the comp
                    elif (e_o[i] == '-1'):
                        ares.append(e_n[i])
                    else:
                        ares.append(e_n[i] - e_o[i])
                results.append(ares)
                ares = []

    return results

# Add up the xp gained in each of the listed skills
def calc_comp_gains(gains, skills):
    res = []
    ares = []

    for player in gains:
        ares.append(player[0])
        ares.append(0)
        for s in skills:
            ares[1] += player[s]
        res.append(ares)
        ares = []

# Returns a list of rsn's with xp gained in one skill (list passed in should have gains)
def get_xp_one_skill(list, skill):
    ret = []

    # For each clanmate, pull out name and xp for passed in skill
    for i in range(len(list)):
        ret.append([list[i][0], list[i][skill]])

    return ret

# Removes people from the result list that gained no xp in any of the skills
def filter_no_xp_gained(list):
    ret = []

    for i in range(len(list)):
        for j in range(len(list[i])):
            if ((type(list[i][j]) is int) and (list[i][j] != 0)):
                ret.append(list[i])

    return ret

# Get current standings
def get_current_standings(participants, skill, file_name):
    skills = [skill]
    start_xp = pull_xp_from_file(file_name)
    start_xp = get_xp_one_skill(start_xp, skill)
    current_xp = get_current_xp_all(participants)
    current_xp = get_xp_one_skill(current_xp, skill)
    current_xp_gains = calc_xp_gained(start_xp, current_xp)
    current_xp_gains = filter_no_xp_gained(current_xp_gains)
    current_xp_gains = sorted(current_xp_gains, key=lambda l:l[1], reverse=True)
    ret_str = ''
    for i in range(len(current_xp_gains)):
        ret_str += (str(i + 1) + '. ' + str(current_xp_gains[i][0]) + '\t' + '{:,}'.format(current_xp_gains[i][1])) + '\n'

    return ret_str

always_in = ['Andy Hunts', 'Mrawr', 'Supaskulled']
participants = ['Andy Hunts', 'Mrawr', 'Gadnuka', 'Firekev', 'TheTrueHelix', 'MiracleEdrea', 'Jake4216', 'JK3', 'Supaskulled', 'Matthewalle2', 'die1988', 'Fairytale']
comp_skill = THIEVING
start_file = 'thieving_1_start'
standings_header = ':moneybag: Thieving Competition Standings'

# Competition start
# current_xp = get_current_xp_all(participants)
# store_xp_in_file(current_xp, start_file)

# Competition standings update
# print(get_current_standings(participants, comp_skill, start_file))

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

    if message.content.startswith('!standings'):
        await message.channel.send(standings_header)
        await message.channel.send(get_current_standings(participants, comp_skill, start_file))

    if message.content.startswith('!help'):
        str = 'use !standings to check standings for current competition'
        await message.channel.send(str)


client.run(DISCORD_KEY)
