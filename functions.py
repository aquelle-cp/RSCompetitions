import requests
import os
import sys

from key import *

NUM_SKILLS = 29
NUM_SKILLS_OSRS = 24

# The template for a player stat request
STAT_REQUEST = 'https://secure.runescape.com/m=hiscore/index_lite.ws?player='
STAT_REQUEST_OSRS = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player='

# Returns a full list of clanmate names from the API based on the given clan name
def get_clanmate_names(clan_name):
     # Get clanmates from the API and convert result into a list of RSNs
    clanmate_res = requests.get('http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName=' + clan_name)
    clanmate_split = clanmate_res.text.split("\n")
    c_split_length = len(clanmate_split)
    clanmates = []
    for i in range(c_split_length):
        if i != 0:
            clanmates.append(clanmate_split[i].split(",")[0])

    # Make sure there are no empty strings
    while '' in clanmates:
        clanmates.remove('')

    return clanmates

# Return a list of clanmates with their current xp in each skill
def get_current_xp_all(clanmates, osrs_clanmates = []):
    # Store the number of people in the clanmate list
    clanmate_length = len(clanmates)

    # Replace any weird space characters with the right one
    for i in range(clanmate_length):
        clanmates[i] = clanmates[i].replace(u'\xa0', u' ')

    # For each clanmate get current xp for every skill [rsn, overall, attack, ...]
    all_cm_data = []
    for i in range(clanmate_length):
        # First spot is the name of the clanmate
        cm_data = [clanmates[i]]

        # Set the req_url and the num_skills_var to the rs3 version by default, and
        # the osrs version if this player is in the osrs list
        if clanmates[i] in osrs_clanmates:
            req_url = STAT_REQUEST_OSRS
            num_skill_var = NUM_SKILLS_OSRS
        else:
            req_url = STAT_REQUEST
            num_skill_var = NUM_SKILLS


        # Get user data from api
        req = requests.get(req_url + clanmates[i])

        # If the user isn't active, api returns 404, skip it
        if req.status_code == 404:
            continue

        # Add each skill xp data point to the clanmate
        cm_stats = req.text.split("\n")
        for i in range(num_skill_var):
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

    return res

# Removes people from the result list that gained no xp in any of the skills
def filter_no_xp_gained(list):
    ret = []

    for i in range(len(list)):
        for j in range(len(list[i])):
            if ((type(list[i][j]) is int) and (list[i][j] != 0)):
                ret.append(list[i])

    return ret

def divide_xp_into_teams(team1, team2, current_xp_gains):
    team1_xp = [['Total', 0]]
    team2_xp = [['Total', 0]]
    for i in range(len(current_xp_gains)):
        if current_xp_gains[i][0] in team1:
            team1_xp[0][1] += current_xp_gains[i][1]        # Add this person's xp to their team's total xp
            team1_xp.append(current_xp_gains[i])
        elif current_xp_gains[i][0] in team2:
            team2_xp[0][1] += current_xp_gains[i][1]
            team2_xp.append(current_xp_gains[i])

    return [team1_xp, team2_xp]

# Get current standings for a free for all comp
def get_current_standings_free_for_all(participants, skills, file_name):
    # skills = [skill]
    start_xp = pull_xp_from_file(file_name)
    start_xp = calc_comp_gains(start_xp, skills)
    current_xp = get_current_xp_all(participants)
    current_xp = calc_comp_gains(current_xp, skills)
    current_xp_gains = calc_xp_gained(start_xp, current_xp)
    current_xp_gains = filter_no_xp_gained(current_xp_gains)
    current_xp_gains = sorted(current_xp_gains, key=lambda l:l[1], reverse=True)
    ret_str = ''
    for i in range(len(current_xp_gains)):
        ret_str += (str(i + 1) + '. ' + str(current_xp_gains[i][0]) + '\t' + '{:,}'.format(current_xp_gains[i][1])) + '\n'

    return ret_str

# Get current standings for a two team comp
def get_current_standings_two_teams(participants, skills, file_name, team1, team2):
    start_xp = pull_xp_from_file(file_name)
    start_xp = calc_comp_gains(start_xp, skills)
    current_xp = get_current_xp_all(participants)
    current_xp = calc_comp_gains(current_xp, skills)
    current_xp_gains = calc_xp_gained(start_xp, current_xp)
    current_xp_gains = filter_no_xp_gained(current_xp_gains)
    current_xp_gains = sorted(current_xp_gains, key=lambda l:l[1], reverse=True)

    team_xp = divide_xp_into_teams(team1, team2, current_xp_gains)
    team1_xp = team_xp[0]
    team2_xp = team_xp[1]

    ret_str = ''
    ret_str += 'Team 1:\n'
    for i in range(len(team1_xp)):
        ret_str += str(i) + '. ' + str(team1_xp[i][0]) + '\t'  + '{:,}'.format(team1_xp[i][1]) + '\n'
    ret_str += '\nTeam 2:\n'
    for i in range(len(team2_xp)):
        ret_str += str(i) + '. ' + str(team2_xp[i][0]) + '\t'  + '{:,}'.format(team2_xp[i][1]) + '\n'

    # for i in range(len(current_xp_gains)):
    #     ret_str += (str(i + 1) + '. ' + str(current_xp_gains[i][0]) + '\t' + '{:,}'.format(current_xp_gains[i][1])) + '\n'

    return ret_str

# Takes a player and, if that player is active and exists, adds their current xp to the start file for the competition
def add_player_to_comp(player_name, file_name):
    # If the player name has any _ characters, replace with spaces
    player_name_req = player_name.replace(u'_', u' ')

    # Get current xp for this player
    req = requests.get(STAT_REQUEST + player_name_req)

    # If the user is inactive (404) their xp cannot be read and they can't be added to the competition
    if req.status_code == 404:
        print('The player with the RSN ' + player_name + ' is either inactive or does not exist, and cannot\n' + \
            'be added to the competition')
        return

    # Open the start file
    wd = os.path.dirname(__file__)
    path = os.path.join(wd, file_name)
    f = open(path, 'r')

    # Check to see if the player is already in the file (the newline and the space insure that, if you're trying to add
    # a player whose name is a substring of another player in the comp, the added player doesn't get blocked from joining)
    str = '\n' + player_name + ' '
    if str in f.read():
        print(player_name + ' is already in this competition\'s start file')
        f.close()
        return
    f.close()

    # Parse the player's xp into a list so it can be put in the file
    f = open(path, 'a')
    player_data = [player_name]
    player_raw_data = req.text.split('\n')
    for i in range(NUM_SKILLS):
        player_data.append(player_raw_data[i].split(',')[2])

    # Add the xp to the end of the start file
    for i in range(len(player_data)):
        print(player_data[i], end=' ', file=f)
    print('', file=f)

    f.close()
    print(player_name + ' has been added to the competition start file')
    return
