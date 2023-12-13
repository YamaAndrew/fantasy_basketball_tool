## Main script to handle web scraping ##

from bs4 import BeautifulSoup       # import BeautifuSoup for web scraping
import requests                     # import requests to access internet requests   
import player_module                # import class_module.py to access Player class
import player_photos                # import player_photos to update player objects' img value

stats_url = "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"   # stats website to scrape from
result = requests.get(stats_url).text                                               # hold the html page in results
doc = BeautifulSoup(result, "html.parser")                                          # hold the parsed html page in doc

tbody = doc.tbody       # access main table from stats website 
trs = tbody.contents    # save contents of main table in trs (table rows)

count = 0       # counter to avoid errors (the html page stores a blank table row after every real table row for some reason)
players = []    # list to store Player objects
name = ""       # initialize name outside of loop to later check for duplicates (this happens due to players changing teams; we only want the first table row, which has cummulative stats)

# iterate through each table row within main table
for tr in trs:

    count += 1  # increment counter

    if count % 2 == 0 or tr.find(text="Player"):    # if the current table row is a blank or a header, ignore it and continue loop
        #print(tr)
        continue

    if name == tr.a.string:     # if the previous name is the same as the current table row's name, ignore it and continue loop
        #print("Duplicate name detected")
        continue

    name = tr.a.string                                  # store name from table row
    points = tr.find_all("td")[28].string               # store points per game from table row
    rebounds = tr.find_all("td")[22].string             # store rebounds per game from table row
    assists = tr.find_all("td")[23].string              # store assists per game from table row
    blocks = tr.find_all("td")[25].string               # store blocks per game from table row
    steals = tr.find_all("td")[24].string               # store steals per game from table row
    threes = tr.find_all("td")[10].string               # store three pointers per game from table row
    turnovers = tr.find_all("td")[26].string            # store turnovers per game from table row
    freeThrowsMade = tr.find_all("td")[17].string       # store free throws made per game from table row
    freeThrowsAttempted = tr.find_all("td")[18].string  # store free throws attempted per game from table row
    fieldGoalsMade = tr.find_all("td")[7].string        # store field goal made per game from table row
    fieldGoalsAttempted = tr.find_all("td")[8].string   # store field goals attempted per game from able row
    minutes = tr.find_all("td")[6].string               # store minutes per game from table row

    player = player_module.Player(name, points, rebounds, assists, blocks, steals, threes, turnovers, freeThrowsMade, 
                    freeThrowsAttempted, fieldGoalsMade, fieldGoalsAttempted, minutes, "")   # initialize new Player object
    players.append(player)  # add current Player object to list of players

# iterate through each player object in players list
for player in players:
    # iterate through every existing key value (player name) in player_headshot list
    for i, existing_dict in enumerate(player_photos.player_headshot):
        if player.name in existing_dict:                                    # if the key exists...
            player.img = player_photos.player_headshot[i][f'{player.name}'] # set the player object's img value to the key's value (url png)