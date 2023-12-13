## Script to handle storing url png images of all current nba players ##

from nba_api.stats.static import players    # import players list from nba_api 

list_size = len(players.get_active_players())   # initialize list_size to length of list of active players

player_headshot = []    # initialize list to hold dictionairy keys (key = player's name, value = url png)

# iterate through integers within list_size
for n in range(list_size):
    # append player's name and url png image to list
    player_headshot.append({players.get_active_players()[n]['full_name']: 
                            "https://cdn.nba.com/headshots/nba/latest/260x190/" + 
                            str(players.get_active_players()[n]['id']) + ".png"})