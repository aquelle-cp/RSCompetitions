# RSCompetitions

RSCompetitions is a command line tool I wrote to track clan competitions in Runescape 3 when the tracker my clan used previously was offline intermittently for a couple of weeks. These competitions involve tracking the xp gains of clan members and posting the in-progress standings over the duration of the competition. 

There are two main parts to this: starting the competition and getting the in-progress standings. To start the competition, the initial xp values of the clan have to be pulled from the API and recorded in a file for later. To get updates on the standings, the current values have to be pulled from the API again and compared against the starting values that were stored in that first file. Since project is a command line tool, both both starting and updating are done through commands in the command line, though there are two ways to update.

First, a little bit of background. My clan uses Discord to talk outside the game and to set up events and competitions, since if something is discussed only in the clan chat in the game itself, anyone who is offline at the time won’t see it. In order to run competitions, I set up a post in Discord with the details and time and instructions to sign up. Sign ups are done through the reactions system in Discord: if someone has added a reaction to the post, they’ve signed up for that competition. In order to update an ongoing competition, I used to run the command line tool locally on my computer periodically throughout the competition (every 12 hours or so, more frequently if someone requested an update), and copy/paste the results from my command line to the Discord channel. Eventually I made a Discord bot that I could run locally (I never did get around to hosting it, so I have it running on a Raspberry Pi usually just so it’s out of the way but still up for the duration of the competition). People could type the trigger command in the chat on Discord and the bot would go run the update command and print the results. This option is much nicer, it means I don’t have to remember to be updating the standings frequently, and people don’t have to rely on my schedule for competition updates. That being said, there is a lot more setup required for the Discord bot version, as well as a computer you don’t mind leaving on for the duration of the competition, or a way to host the bot

## Installation

1. Make sure you have Python installed (should return Python 3.x.x, if it doesn't, download from [here](https://www.python.org/downloads/))
```bash
  python3 --version
```

2. Clone the repository (enter this in the terminal)
```bash
git clone git@github.com:aquelle-cp/RSCompetitions.git
```

3. Install dependencies (pip3 should have been included with Python)
```bash
pip3 install -r requirements.txt
```

## Usage

### Setting up settings.py

This file contains the variables that hold the data that changes from competition to competition or clan to clan, but is necessary to run any competition, like the skills, the participants, and the file the starting data needs to be stored in. This file needs to be set before a competition starts (before the start command is run) and shouldn't be changed again until after the competition ends, with one exception. The exception is the third command listed below (add), during which you need to modify the settings.py file to add the player(s) to the participants list.

1. Open the settings.py file in a text editor (Notepad on Windows, TextEdit on Mac, etc.) and modify the variables
```python
s_comp_type          # Either FREE_FOR_ALL or TWO_TEAMS
                     # FREE_FOR_ALL displays each person's xp individually
                     # TWO_TEAMS displays xp split into the teams, and requires the
                     #   s_team1 and s_team2 variables to also be set
                     # ex. s_comp_type = FREE_FOR_ALL
                     
s_participants       # A list of the RSNs of the people participating in the competition
                     # Note: if you want to track the entire clan for the competition, you
                     # can use s_participants = get_clanmate_names('clan name'), but be
                     # warned, unless your clan is very small, this can make it take a long
                     # time to start and update (for reference, with a clan of 40 it would
                     # take several minutes to pull the data from the API and update)
                     # ex. s_participants = ['rsn1', 'rsn2', 'rsn3', 'rsn4']
                     
s_team1              # Only needs to be set if s_comp_type is TWO_TEAMS, a list of the
                     # RSNs of the people on the first team
                     # ex. s_team1 = ['rsn1', 'rsn3']
                     
s_team2              # Same as above, but the second team
                     # ex. s_team2 = ['rsn2', 'rsn4']
                     
s_comp_skills        # List of skills the competition is for (the way the skills are
                     # written needs to correspond to the constants listed in the 
                     # settings.py file, basically just all caps and not in quotes)
                     # Note: if you're running a competition for overall xp (all skills),
                     # use OVERALL instead of listing all the skills out
                     # ex. s_comp_skills = [HUNTER, FISHING]
                     # ex. s_comp_skills = [OVERALL]
                     
s_start_file         # The path to the file you want to record the starting values for the
                     # competition in, I recommend having a folder for these files, I call
                     # mine start_files, just to keep them separate from the code
                     # Note that if the file doesn't exist, it'll create it for you, and if
                     # the file exists and has contents, it'll ask for confirmation before
                     # deleting any contents and replacing with the start files
                     # ex. s_start_file = 'start_files/rc_1_comp'
                     
s_standings_header   # Only set if you're using a discord bot, otherwise this won't do
                     # anything
                     # If you are using a Discord bot, this will print to the channel 
                     # when the update is triggered, so it serves both as a header and as
                     # confirmation to the player that triggered the update that the
                     # program is working on getting the current standings, since that
                     # can take anywhere from a few seconds to a minute or two depending
                     # on the current state of the API and the number of players in the
                     # competition
                     # ex. s_standings_header = ':fish: Fishing Competition Standings'
                     # (Discord translates :fish: to the fish emoji automatically)
```

2. Don't change it during a competition unless you need to add a player to the competition.

### Staring the competition

1. Make sure the settings.py file is set up with all the necessary variables

2. Open terminal and navigate to the RSCompetitions folder

3. In that folder in terminal, run
```bash
python3 run_cmd.py start
```

4. Navigate to the start file (the location you specified in settings.py) and double check that it ran properly. The file should have each participant on a line, followed by a list of numbers. If any of the players are inactive or don't exist, they will not show up in this file. If anything is wrong, double check settings to make sure it was set properly.

5. The competition has begun!

### Updating the competition

1. Make sure the settings.py file is the same as when you started the competition (unless you added a player, which is talked about next)

2. Open terminal and navigate to the RSCompetitions folder

3. In that folder in terminal, run 
```bash
python3 run_cmd.py update
```

4. Wait for a bit, this one can take a while to run, especially if you used the function to get the RSNs of everyone in your clan, or if you have a lot of participants

5. When it does finish running and prints out the result, copy/paste it into whatever chat system your clan uses to update the others on the current standings

### Adding a player to a competition

Occasionally you'll have a situation where someone missed the signups, or joined the clan during a competition and wants to participate, even if they'll be at a disadvantage xp-wise for joining late. This is when you'll use these instructions. Please note that this just adds this player's current xp to the start file, so it doesn't track from where they were when the competition started, but from where they were when they joined the competition.

1. Open the terminal and navigate to the RSCompetitions folder

2. In that folder in terminal, run (player_name can either be the name of one player, or a space-separated list of players, but make sure if the player's name has a space in it, you replace that space with an _ so the program doesn't think it's two different names)
```bash
python3 run_cmd.py add [player_name]
```

3. After that finishes running, make sure it was added to the start file properly by double checking the start file to see that their name is now at the bottom with their current xp numbers

4. Then add the player(s) to the s_participants variable in the settings.py file. Note: if you don't do this, update will not display their xp gains

## Setting up the Discord bot and using it to update the competition

1. Follow the instructions [here](https://discordpy.readthedocs.io/en/stable/discord.html) to set up the account, make a bot, and invite it to a server

2. Create a file called key.py in the RSCompetitions folder the token from the 'Build-A-Bot' page (Creating a Bot Account step 6 in the link above)
```python
DISCORD_KEY =   # Your bot's token goes here in quotes
```

3. Set up settings.py (follow the instructions in the settings.py section above), and make sure you set the s_standings_header variable

3. Follow the instructions above to start a competition from the command line (currently the Discord bot cannot start a competition, only print the updates, so the competition has to be started normally, from the command line)

4. Start the Discord bot from the command line (same location as where you start the competition in the terminal)
```bash
python3 start_discord_bot.py
```

5. Type '!standings' or 'compbot do the thing!' in the channel you invited the bot to, it should print out the standings header first while it's working on the standings, then it'll print out the standings when it's done pulling and calculating them


