import requests

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
STAT_REQUEST = "https://secure.runescape.com/m=hiscore/index_lite.ws?player="

# Current player xp dict template INCOMPLETE TEMPLATE
CURRENT_XPS = {'name': '-', 'overall': 0, 'attack': 0, 'defence': 0,
               'strength': 0, 'constitution': 0, 'ranged': 0, 'prayer': 0,
               'magic': 0, 'cooking': 0, 'woodcutting': 0, 'fletching': 0,
               'fishing': 0, 'firemaking': 0, 'crafting': 0, 'smithing': 0,
               'mining': 0, 'herblore': 0}

# Return a list of clanmates with their current xp in each skill
def get_current_xp_all():
    # Get list of Acorn clanmates
    clanmate_res = requests.get("http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName=Acorn")
    clanmate_split = clanmate_res.text.split("\n")
    clanmate_length = len(clanmate_split)

    clanmates = []
    all_cm_data = []

    for i in range(clanmate_length):
        if i != 0:
            clanmates.append(clanmate_split[i].split(",")[0])

    print("Acorn member list")

    # Replace any weird space characters with the right one
    for i in range(clanmate_length - 1):
        clanmates[i] = clanmates[i].replace(u'\xa0', u' ')
        print(clanmates[i])

    # For each clanmate get current xp for every skill [rsn, overall, attack, ...]
    for i in range(clanmate_length - 1):
        cm_data = [clanmates[i]]

        # Get user data from api, if the rsn isn't active, skip it
        req = requests.get(STAT_REQUEST + clanmates[i])
        if req.status_code == 404:
            continue
        
        cm_stats = req.text.split("\n")
        for i in range(28):
            cm_data.append(cm_stats[i].split(",")[2])

        all_cm_data.append(cm_data)

    return all_cm_data


def store_xp_in_file(list, fname):
    for i in range(len(list)):
        print(list[i])
    return

# Gets all starting xp and writes the data to a file for later use
def set_start_xp_all():
    return

# One skill level/xp for one player
##skill_res = requests.get("https://secure.runescape.com/m=hiscore/index_lite.ws?player=joe g")
##skill_split = skill_res.text.split("\n")
##
##print("Joe G's xp: Invention")
##print(skill_split[INVENTION].split(",")[2])

store_xp_in_file(get_current_xp_all(), "start")







