import requests
import os
import sys

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

# The template for a player stat request
STAT_REQUEST = 'https://secure.runescape.com/m=hiscore/index_lite.ws?player='

# Current player xp dict template INCOMPLETE TEMPLATE
CURRENT_XPS = {'name': '-', 'overall': 0, 'attack': 0, 'defence': 0,
               'strength': 0, 'constitution': 0, 'ranged': 0, 'prayer': 0,
               'magic': 0, 'cooking': 0, 'woodcutting': 0, 'fletching': 0,
               'fishing': 0, 'firemaking': 0, 'crafting': 0, 'smithing': 0,
               'mining': 0, 'herblore': 0}

# Return a list of clanmates with their current xp in each skill
def get_current_xp_all():
    # Get list of Acorn clanmates
    clanmate_res = requests.get('http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName=Acorn')
    clanmate_split = clanmate_res.text.split("\n")
    c_split_length = len(clanmate_split)

    clanmates = []
    all_cm_data = []

    # Get the list of clanmates in Acorn
    for i in range(c_split_length):
        if i != 0:
            clanmates.append(clanmate_split[i].split(",")[0])

    # Add in any eternal guests
    clanmates.append('Fairytale')

    # Make sure there are no empty strings
    while '' in clanmates:
        clanmates.remove('')

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
        for i in range(28):
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

# Returns a list with all xp gained
def calc_xp_gained(first, second):
    if (len(first) != len(second)):
        print('Lengths of first and second lists are different.')
        sys.exit()

    # print(first)
    # print(second)

    ret = first

    # Calculate differences in xp
    for i in range(len(first)):
        for j in range(len(first[i])):
            # If the skill is not unlocked or hasn't been trained
            if (first[i][j] == -1):
                ret[i][j] = second[i][j]
            # If the data is not numeric (is the name) and the names are the same
            elif ((type(first[i][j]) is str) and (type(second[i][j]) is str) and (first[i][j] == second[i][j])):
                ret[i][j] = first[i][j]
            # If the data is numeric (not a name field)
            elif ((type(first[i][j]) is int) and (type(second[i][j]) is int)):
                ret[i][j] = second[i][j] - first[i][j]
            else:
                ret[i][j] = 0

    return ret

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


# Removes people from the result list that gained no xp in the skill
def filter_no_xp_gained_one_skill(list):
    ret = []

    for i in range(len(list)):
        if (list[i][1] != 0):
            ret.append(list[i])
