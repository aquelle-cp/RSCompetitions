from functions import get_clanmate_names

### Constants for parsing -- DO NOT CHANGE
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

FREE_FOR_ALL = 0
TWO_TEAMS = 1


### Adjustable variables

# The type of competition, options are FREE_FOR_ALL or TWO_TEAMS. This setting determines how the update function shows the current
# standings. If FREE_FOR_ALL is chosen, everyone's xp will be displayed and ranked individually, if TWO_TEAMS is chosen, the xp will
# be shown divided into those two teams
s_comp_type = FREE_FOR_ALL

# The RSNs of the people participating in the competition, in quotes and comma-separated. If you want to track all players in the
# clan use get_clanmate_names("your clan name goes here") instead of the array. This isn't recommended unless the majority of the
# clan is participating in the competition because the extra API requests make the updates incredibly slow to run
s_participants =  ['Firekev', 'Gadnuka', 'TheTrueHelix', 'MiracleEdrea']

# If the competition is a team comp, use these to list the RSNs of the players on each team. NOTE: the participants variable (above)
# must also include all of the RSNs of the players participating, if it doesn't, even if all of the participants are listed in these
# team variables, they will not be tracked properly
s_team1 = ['Firekev', 'Gadnuka']
s_team2 = ['TheTrueHelix', 'MiracleEdrea']

# The skills for the competition. Use the variable constant names defined above. If the competition is for all skills, use OVERALL
# instead of listing all skills
s_comp_skills = [THIEVING, SLAYER]

# The name of the file you want to store the starting xp in
s_start_file = 'test_file'
