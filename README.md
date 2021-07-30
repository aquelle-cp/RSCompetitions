# RSCompetitions

RSCompetitions is a command line tool I wrote to track clan competitions in Runescape 3 when the tracker my clan used previously was offline intermittently for a couple of weeks. These competitions involve tracking the xp gains of clan members and posting the in-progress standings over the duration of the competition. 

There are two main parts to this: starting the competition and getting the in-progress standings. To start the competition, the initial xp values of the clan have to be pulled from the API and recorded in a file for later. To get updates on the standings, the current values have to be pulled from the API again and compared against the starting values that were stored in that first file. Since project is a command line tool, both both starting and updating are done through commands in the command line, though there are two ways to update.

First, a little bit of background. My clan uses Discord to talk outside the game and to set up events and competitions, since if something is discussed only in the clan chat in the game itself, anyone who is offline at the time won’t see it. In order to run competitions, I set up a post in Discord with the details and time and instructions to sign up. Sign ups are done through the reactions system in Discord: if someone has added a reaction to the post, they’ve signed up for that competition. In order to update an ongoing competition, I used to run the command line tool locally on my computer periodically throughout the competition (every 12 hours or so, more frequently if someone requested an update), and copy/paste the results from my command line to the Discord channel. Eventually I made a Discord bot that I could run locally (I never did get around to hosting it, so I have it running on a Raspberry Pi usually just so it’s out of the way but still up for the duration of the competition). People could type the trigger command in the chat on Discord and the bot would go run the update command and print the results. This option is much nicer, it means I don’t have to remember to be updating the standings frequently, and people don’t have to rely on my schedule for competition updates. That being said, there is a lot more setup required for the Discord bot version, as well as a computer you don’t mind leaving on for the duration of the competition, or a way to host the bot.

## Installation

1. Make sure you have Python installed (should return Python 3.x.x, if it doesn't, download from [here](https://www.python.org/downloads/))
```bash
python3 --version
```

2. Clone the repository (enter this in the command line or terminal ____ figure out what this is on Windows)
```bash
git clone git@github.com:aquelle-cp/RSCompetitions.git
```

3. Install dependencies (pip3 should have been included with Python)
```bash
pip3 install -r requirements.txt
```

## Setting up the Discord bot

1. ____

## Usage

### Staring the competition

1. Open the settings.py file in a text editor (Notepad on Windows, TextEdit on Mac, etc.) and modify the variables
```python
s_comp_type          # Either FREE_FOR_ALL or TWO_TEAMS
                     # FREE_FOR_ALL displays each person's xp individually
                     # TWO_TEAMS displays xp split into the teams, and requires the
                     #   s_team1 and s_team2 variables to also be set
                     # ex. s_comp_type = FREE_FOR_ALL
                     
s_participants       # A list of the RSNs of the people participating in the competition
                     # ex. s_participants = ['rsn1', 'rsn2', 'rsn3', 'rsn4']
                     
s_team1              # Only needs to be set if s_comp_type is TWO_TEAMS, a list of the
                     # RSNs of the people on the first team
                     # ex. s_team1 = ['rsn1', 'rsn3']
                     
s_team2              # Same as above, but the second team
                     # ex. s_team2 = ['rsn2', 'rsn4']
                     
s_comp_skills        # List of skills the competition is for (the way the skills are
                     # written needs to correspond to the constants listed in the 
                     # settings.py file, basically just all caps and not in quotes)
                     # ex. s_comp_skills = [HUNTER, FISHING]
                     # ex. s_comp_skills = [RUNECRAFTING]
                     
s_start_file         # The path to the file you want to record the starting values for the
                     # competition in, I recommend having a folder for these files, I call
                     # mine start_files, just to keep them separate from the code
                     # Note that if the file doesn't exist, it'll create it for you, and if
                     # the file exists and has contents, it'll ask for confirmation before
                     # deleting any contents and replacing with the start files
                     # ex. s_start_file = 'start_files/rc_1_comp'
                     
s_standings_header   # Only set if you're using a discord bot, otherwise this won't do
                     # anything
```

2. Open terminal and navigate to the RSCompetitions folder
 






