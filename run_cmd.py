import sys

from functions import *
from settings import *

### Command functions
# Starts the comp by checking the start file for emptiness (asks user if it can be erased if it's not empty)
# then getting current xp and writing it to the start file
def start_comp():
    wd = os.path.dirname(__file__)
    path = os.path.join(wd, s_start_file)
    # Try to open the file and figure out if it has something in it
    try:
        f = open(path, 'r+')
        # If the file has stuff in it, make sure the user wants to delete the current contents before continuing
        if f.read() != '':
            res = input('This file already has contents, would you like to erase it and use it for this competition? (y/n) ')
            # If the user confirms that they want to erase and use this file, delete the contents by truncating it
            if res.lower() == 'y':
                f.close()
                f = open(path, 'w')
            else:
                print('Ok, leaving file alone. \nTo start a competition please set a differnt start file name in settings.py')
                f.close()
                return
        # If the file is empty, don't do anything with it
    # If the file doesn't exist yet, create it
    except:
        f = open(path, 'x')

    f.close()

    # Get current xp for all participants and store it in the start file
    current_xp = get_current_xp_all(s_participants)
    store_xp_in_file(current_xp, s_start_file)

    print('The start file for this competition has been written')

    return

# Update the comp by printing out the current competition standings
def update_comp():
    if s_comp_type == FREE_FOR_ALL:
        print(get_current_standings_free_for_all(s_participants, s_comp_skills, s_start_file))
    elif s_comp_type == TWO_TEAMS:
        print(get_current_standings_two_teams(s_participants, s_comp_skills, s_start_file, s_team1, s_team2))
    else:
        print('The s_comp_type value in settings.py is invalid')

# Add player(s) to the comp by appending their current xp values to the end of the start file
def add_players(player_names):
    pass

### Command parsing
help_text = 'Usage:\n\trun_cmd.py <command>\n' + \
    'Commands:\n' + \
    '\thelp\tDisplays all the commands and their usages\n' + \
    '\tstart\tStarts a competition with the participants set in settings.py\n' + \
    '\tupdate\tDisplays the current standings for the competition, with the \n' + \
    '\t\tparticipants, type, and skill(s) set in settings.py\n' + \
    '\tadd [player_name]\tAdds the current xp of the player specified to \n' + \
    '\t\t\t\tthe start file set in settings.py\n'
help_opt = ['help', '-h']

# If no arguments were specified, print the help text
if len(sys.argv) < 2:
    print('Invalid argument')
    print(help_text)
# help command
elif sys.argv[1] in help_opt:
    print(help_text)
# start command stores current xp for all participants in the start file from settings
elif sys.argv[1] == 'start':
    start_comp()
# update command prints out the current comp standings based on comp type, skill, and participants from settings
elif sys.argv[1] == 'update':
    update_comp()
# add [player] command adds a player's current xp to an ongoing competition's
elif sys.argv[1] == 'add':
    if len(sys.argv) == 2:
        print('Please specify the name of the player to add to the comp in the format:\n run_cmd.py add [player_name]')
    else:
        add_players(sys.argv[2:])
        print('adding player(s)')
# If the pattern didn't match any of the above, print a notice then the help text
else:
    print('Invalid arguments')
    print(help_text)
