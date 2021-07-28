import sys

from functions import *
from settings import *

### Commands
help_text = 'Usage:\n\trun_cmd.py <command>\n' + \
    'Commands:\n' + \
    '\thelp\tDisplays all the commands and their usages\n' + \
    '\tstart\tStarts a competition with the participants set in settings.py\n' + \
    '\tupdate\tDisplays the current standings for the competition, with the \n' + \
    '\t\tparticipants, type, and skill(s) set in settings.py\n' + \
    '\tadd [player_name]\tAdds the current xp of the player specified to \n' + \
    '\t\t\t\tthe start file set in settings.py\n'
help_opt = ['help', '-h']

# If no arguments were specified
if len(sys.argv) < 2:
    print('Invalid argument')
    print(help_text)
# help command
elif sys.argv[1] in help_opt:
    print(help_text)
# start : if the file has content, print file name and are you sure you want to erase this file?
elif sys.argv[1] == 'start':
    # wd = os.path.dirname(__file__)
    # path = os.path.join(wd, fname)
    # f = open(path, 'r+')
    print('start')
# update
elif sys.argv[1] == 'update':
    print('update')
# add [player]
elif sys.argv[1] == 'add':
    if len(sys.argv) == 2:
        print('Please specify the name of the player to add to the comp in the format:\n run_cmd.py add [player_name]')
    else:
        print('adding player(s)')
# If the pattern didn't match any of the above, print a notice then the help text
else:
    print('Invalid arguments')
    print(help_text)

# # Competition start
# current_xp = get_current_xp_all(participants)
# store_xp_in_file(current_xp, start_file)

# Competition standings update
# print(get_current_standings_free_for_all(participants, comp_skills, start_file))

# print(get_current_standings_two_teams(participants, comp_skills, start_file, team1, team2))