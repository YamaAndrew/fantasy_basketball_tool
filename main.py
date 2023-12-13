## Main python script to run Fantasy Basketball Tool application ##

import sys, web_scraping, main_gui  # imports for: running app, accessing web scraping scripts, acessing app's gui
from PyQt5.QtWidgets import QApplication    # import PyQt library for running app

# Main function that runs application 
def main():
    app = QApplication(sys.argv)                    # initialize app to a QApplication
    fantasy_app = main_gui.FantasyBasketballApp()   # initialize fantasy_app to a FantasyBasketBallApp object from gui.py file

    
    fantasy_app.tier_list_button.clicked.connect(lambda: handle_tier_list_button(fantasy_app))  # connect clicked signal of Tier List button 
    

    sys.exit(app.exec_())   # terminate the program when window is closed

# method to calculate players' fantasy points per game and assign to appropriate tiers in gui
def handle_tier_list_button(fantasy_app):
    # iterate through each player scrapped from web_scraping script
    for p in web_scraping.players:

        # calulate current player's fantasy score and respective tier
        p.calculateFantasyScore(fantasy_app.w)
        p.classifyTier()
        
        # add current player (with info) to respective tier in gui
        fantasy_app.add_to_tier(p.name, p.ppg, p.rpg, p.apg, p.bpg, p.spg, p.fg3, p.tov, p.ftm, p.fta, p.fgm, p.fga, p.mpg, p.img, p.tier, p.fppg[0])

        # print names of player with inconsistent names (wont show headshot in gui)
        #if p.img == "":
            #print(p.name)

    # call the gui method to display the tier lists
    fantasy_app.show_tier_list()

# run main function
if __name__ == '__main__':
    main()