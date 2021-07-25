import sys

from functions import *

participants =  ['Andy Hunts', 'Firekev', 'Mrawr', 'Gadnuka']
comp_skills = [THIEVING, SLAYER]
start_file = 'start_files/thieving_1_start'

team1 = ['Andy Hunts', 'Firekev']
team2 = ['Mrawr', 'Gadnuka']

# # Competition start
# current_xp = get_current_xp_all(participants)
# store_xp_in_file(current_xp, start_file)

# Competition standings update
# print(get_current_standings_free_for_all(participants, comp_skills, start_file))

print(get_current_standings_two_teams(participants, comp_skills, start_file, team1, team2))