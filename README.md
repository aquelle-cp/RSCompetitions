# RSCompetitions

RSCompetitions is a command line tool I wrote to track clan competitions in Runescape 3 when the tracker my clan used previously was offline intermittently for a couple of weeks. These competitions involve tracking the xp gains of clan members and posting the in-progress standings over the duration of the competition.

There are two main parts to this: starting the competition and getting the in-progress standings. To start the competition, the initial xp values of the clan have to be pulled from the API and recorded in a file for later. To get updates on the standings, the current values have to be pulled from the API again and compared against the starting values that were stored in that first file. Since the project is a command line tool, both starting and updating are done through commands in the command line, though there are two different ways to run the update command.

## Background

First, a little bit of background on how my clan runs clan competitions, and how I use this tool to do that. My clan uses Discord to talk outside the game and to set up events and competitions, since if something is discussed only in the clan chat in the game itself, anyone who is offline at the time won’t see it.

To start a competition, I run the start command right at the start time for the competition, and announce in the Discord channel that it has begun. The command line version of the update command was the original way to do it, and I would run that command every 12 hours or so and post the resulting current standings in the Discord channel (more frequently if it was requested and I was available). The second way to run the command is the Discord bot. When using the bot, right after starting up the competition, I start up the bot on a computer I didn't mind leaving on for the entirety of the competition (I used a Raspberry Pi). The Discord bot version is easier for everyone since they can see the updates whenever they want and I don't have to remember to post them, but it requires more set up and a computer to have it running for the duration of the competition.

## A Note on OldSchool RS

A short summary of this section first: this program can track players in both OSRS and RS3, with some limitations. See the last paragraph of this section for the limitations, and the Usage section for the setting that controls whether a player is tracked in OSRS or RS3.

Though OSRS and RS3 don't share a clan system, if a clan is like mine, a lot of talking and event planning goes on in Discord instead of RS3, so even players who have switched from RS3 to playing more OSRS will still stay in touch with the clan. Recently we had one of our clanmates who has been playing mainly OSRS want to participate in a skilling competition with their OSRS account, despite the disadvantage that would put him at (OSRS xp rates tend to be lower than RS3), just for fun. The part of the RS3 API that I use to pull character xp data is almost identical to the corresponding part of the the OSRS API, so I converted the core function to get player xp and added a variable to hold the names of the players who are playing in OSRS that the function can read data from.

There are some problems with the way this works right now though. From what I've seen, because the playerbase in OSRS is so much larger than in RS3, even players that have levels and a reasonable amount of xp in a skill might not be ranked, which causes the API call to sometimes return -1 for their xp instead of the actual amount. Because of this, if a player has skills in the competition that are not ranked, their xp either might not track, or, if during the competition they get their xp high enough to be ranked, it might count the entirety of their xp for that skill as their gains for the competition (since the program thinks they started at -1). This is far from ideal, and is something I'll be looking into later, but for now this is how it works. If you have a player or players that want to use OSRS xp, [this](https://secure.runescape.com/m=hiscore_oldschool/overall) is the link to the official OSRS hiscores where you can check if their skills for the compeittion are ranked yet. If the page for that player is missing skills, those skills are not ranked. 

## Installation

1. Make sure you have Python installed (this should return Python 3.x.x; if it doesn't, download from [here](https://www.python.org/downloads/))
    ```bash
    python3 --version
    ```

2. Clone the repository
    ```bash
    git clone git@github.com:aquelle-cp/RSCompetitions.git
    ```

3. Install the dependencies (pip3 should have been included with Python)
    ```bash
    pip3 install -r requirements.txt
    ```

## Usage

### Setting up settings.py

This file contains the variables that hold the data that changes from competition to competition or clan to clan, but is necessary to run any competition. This file needs to be set before a competition starts (that is, before the start command is run) and shouldn't be changed again until after the competition ends, with one exception. (That exception is the third command listed below, the add command, during which you need to modify the settings.py file to add the player(s) to the participants list.)

1. Open the settings.py file in a text editor (Notepad on Windows, TextEdit on Mac, etc.) and modify the variables
    ```python
    s_comp_type          # Either FREE_FOR_ALL or TWO_TEAMS
                         # FREE_FOR_ALL displays each person's xp individually
                         # TWO_TEAMS displays xp split into the teams, and requires the
                         #   s_team1 and s_team2 variables also be set
                         # ex. s_comp_type = FREE_FOR_ALL

    s_participants       # A list of the RSNs of the people participating in the competition
                         # Note: if you want to track the entire clan for the competition, you
                         # can use s_participants = get_clanmate_names('clan name'), but be
                         # warned, unless your clan is very small, this can make it take a long
                         # time to start and update (for reference, with a clan of 40 it would
                         # take several minutes to pull the data from the API and update)
                         # ex. s_participants = ['rsn1', 'rsn2', 'rsn3', 'rsn4']
                         
    s_osrs_participants  # A list of RSNs of the players participating in the competition from
                         # their OSRS account. These players must also be listed in
                         # s_participants
                         # ex. s_osrs_participants = ['rsn3']

    s_team1              # (Only set this if you're running a two team competition)
                         # A list of the RSNs of the people on the first team
                         # ex. s_team1 = ['rsn1', 'rsn3']

    s_team2              # Same as above, but the second team
                         # ex. s_team2 = ['rsn2', 'rsn4']

    s_comp_skills        # A list of skills the competition is for (the way the skills are
                         # written needs to correspond to the constants listed in the
                         # settings.py file, basically just all caps and not in quotes)
                         # Note: if you're running a competition for overall xp (all skills),
                         # use OVERALL instead of listing all the skills out
                         # ex. s_comp_skills = [HUNTER, FISHING]
                         # ex. s_comp_skills = [OVERALL]

    s_start_file         # The path to the file you want to record the starting values for the
                         # competition in. I recommend having a folder for these files, I call
                         # mine start_files, just to keep them separate from the code
                         # Note: if the file doesn't exist, it'll create it for you.  If
                         # the file exists and has contents, it'll ask for confirmation before
                         # deleting any contents and replacing them with the new start file
                         # ex. s_start_file = 'start_files/rc_comp'

    s_standings_header   # (Only set this if you're using a Discord bot)
                         # If you are using a Discord bot, this will print to the channel
                         # when the update is triggered, so it serves both as a header and as
                         # confirmation to the player that requested the update that the
                         # program is working on getting the current standings, since that
                         # can take anywhere from a few seconds to a minute or two depending
                         # on the current state of the API and the number of players in the
                         # competition
                         # ex. s_standings_header = ':fish: Fishing Competition Standings'
                         # (Discord translates :fish: to the fish emoji automatically)
    ```

2. Save the file and don't change it during a competition unless you need to add a player to it

### Staring the competition

1. Make sure the settings.py file is set up with all the necessary variables

2. Open terminal and navigate to the RSCompetitions folder

3. In that folder in terminal, run
    ```bash
    python3 run_cmd.py start
    ```

4. Navigate to the start file (the location you specified in settings.py) and double check that it ran properly. The file should have each participant on a line, followed by a list of numbers. If any of the players are inactive or don't exist, they will not show up in this file. If anything is wrong, double check settings to make sure it was set properly

5. The competition has begun!

### Updating the competition

1. Make sure the settings.py file is the same as when you started the competition (unless you added a player, which I go over in the next section)

2. Open terminal and navigate to the RSCompetitions folder

3. In that folder in terminal, run
    ```bash
    python3 run_cmd.py update
    ```

4. Wait for a bit, this one can take a while to run, especially if you used the function to get the RSNs of everyone in your clan, or if you have a lot of participants

5. When it does finish running and prints out the result, copy/paste it into whatever chat system your clan uses to update everyone on the current standings

### Adding a player to an ongoing competition

Occasionally you'll have a situation where someone missed the signups, or joined the clan during a competition and wants to participate, even if they'll be at a disadvantage xp-wise for joining after it has already started. This is when you'll use these instructions. Please note that this just adds this player's current xp to the start file, so it doesn't track from where they were when the competition started, but from where they were when they joined the competition.

1. Open the terminal and navigate to the RSCompetitions folder

2. In that folder in terminal, run the following, where player_name can either be the name of one player, or a space-separated list of players, but make sure if the player's name has a space in it, you replace that space with an _ so the program doesn't think it's two different names
    ```bash
    python3 run_cmd.py add [player_name]
    ```

3. After that finishes running, make sure the player was added to the start file properly by double checking the start file to see that their name is now at the bottom with their current xp numbers

4. Then add the player(s) to the s_participants variable in the settings.py file. Note: if you don't do this, the update command will not display their xp gains

## Setting up the Discord bot and using it to update the competition

1. Follow the instructions [here](https://discordpy.readthedocs.io/en/stable/discord.html) to set up the account, make a bot, and invite it to a server

2. Create a file called key.py in the RSCompetitions folder and add the token from the 'Build-A-Bot' page (Creating a Bot Account step 6 in the link above)
    ```python
    DISCORD_KEY =   # Your bot's token goes here in quotes
    ```

3. Set up settings.py (follow the instructions in the settings.py section above), and make sure you set the s_standings_header variable

3. Follow the instructions above to start a competition from the command line (currently the Discord bot cannot start a competition, only print the updates, so the competition has to be started normally, from the command line)

4. Start the Discord bot from the command line (same location as where you start the competition in the terminal)
    ```bash
    python3 start_discord_bot.py
    ```

5. Type '!standings' or 'compbot do the thing!' in the channel you invited the bot to. It should print out first the standings header while it's working on calculating, then the standings when it's done pulling and calculating them. Note: if you run this immediately after starting the competition, it'll only print the header, because there aren't any standings yet to display

## Important notes

- The Runescape API updates when players lobby or log out, so if you want your current xp to be reflected in the standings updates, you have to lobby/log first
- In the same way, the start command will pull current xp from when someone last lobbied/logged, so if people are logged in when the competition starts, it might not necessarily be their current xp but whatever they were at when they logged in
     - For my clan, I just tell everyone this and ask people to lobby before the competition starts if they've been training the skill, since cheating isn't usually a problem in a clan as small as mine. But if you have anyone in the clan who might want to mess with the competition and they're told about it, they could potentially gain a bunch of xp in a session before the competition, and not lobby/log until after it starts, which would give them a head start, so fair warning

- The update command will not show players who haven't gained any xp for the competition. I didn't want to call anyone out who hadn't gained any xp yet in a competition, so this was intentional

- Usually if a player's xp is not updating, it's because they haven't lobbied/logged yet. If they have and it still isn't updating, it's possible the API is not updating properly for that player. We've had instances where one or two players' xp wouldn't update for several hours, but everyone else's was updating fine. If you wait it out, it'll update eventually
