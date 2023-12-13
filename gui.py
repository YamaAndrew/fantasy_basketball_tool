import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt5.QtGui import QMovie

# initialize lists as empty for each player tier list
s_tier_players = []
a_tier_players = []
b_tier_players = []
c_tier_players = []
d_tier_players = []
f_tier_players = []

# class to handle the functionality of a current tier list
class PlayerTierWidget(QWidget):

    # default constructor that initializes crucial variables
    def __init__(self, tier_name, players):
        super().__init__() # initializes parent class constructor (a.k.a. QWidget)

        # assign passed in arguments to instance variables (helps PlayerTierWidget remember which tier it represents)
        self.tier_name = tier_name  # current tier
        self.players = players      # current tier's list of players

        #self.initial_state = True

        self.current_players = self.get_random_players()    # initialize current_players to 3 random players from current tier (for featured players w/ gifs)
        self.current_tier_list = []                         # initialize list for all players within current tier

        self.init_ui()  # call main gui constructor

    # gui method for current tier 
    def init_ui(self):
        self.tier_label = QLabel(self.tier_name) # set tier_label to current tier's name

        # apply background color to tier_label depending on its tier
        if self.tier_name == 'S':
            self.tier_label.setStyleSheet("background-color: red; font-size: 20px;")
        elif self.tier_name =='A':
            self.tier_label.setStyleSheet("background-color: gold; font-size: 20px;")
        elif self.tier_name =='B':
            self.tier_label.setStyleSheet("background-color: chartreuse; font-size: 20px;")
        elif self.tier_name =='C':
            self.tier_label.setStyleSheet("background-color: lightskyblue; font-size: 20px;")
        elif self.tier_name =='D':
            self.tier_label.setStyleSheet("background-color: magenta; font-size: 20px;")
        elif self.tier_name =='F':
            self.tier_label.setStyleSheet("background-color: dimgray; font-size: 20px;")
        
        self.gif_layout = QHBoxLayout() # initialize horizontal layout for gifs
        #self.gif_label_list = []        # initialize list to store gif labels

        # iterate through list of current_players (the 3 randomly featured players)
        for player in self.current_players:
            gif_label = QLabel()                                    # initialize gif label 
            movie = QMovie(f"player_images/{player['name']}.gif")   # initialize movie as current player's respective gif
            gif_label.setMovie(movie)                               # assign movie (actual gif) to gif label
            movie.start()                                           # allow gif to animate
            gif_label.setFixedSize(200, 200)                        # set gif to a fixed size of 200x200 pixels
            self.gif_layout.addWidget(gif_label)                    # add current gif label to gif layout
            #self.gif_label_list.append(gif_label)                  # add current gif label to 

        self.gif_layout_labels = QHBoxLayout()  # initialize horizontal layout for the gif_layout's labels
        self.featured_players()                 # call method to add featured players to gif_layout_labels layout

        self.see_more_button = QPushButton("See More")              # initialize see more button 
        self.see_more_button.clicked.connect(self.show_full_tier)   # connect clicked signal of see more button to show_full_tier method (calls the method when clicked)

        self.player_layout = QVBoxLayout()  # initialize vertical layout for players within current tier

        self.see_less_button = QPushButton("See Less")              # initialize see less button 
        self.see_less_button.clicked.connect(self.hide_full_tier)   # connect clicked signal of see less button to hide_full_tier method (calls the method when clicked)
        self.see_less_button.hide()                                 # initially hid the see less button

        self.player_layout.addSpacing(30)   # Add some vertical spacing between the gifs and list of players

        # initialize a base layout 
        layout = QVBoxLayout()                      # initialize layout as a vertical layout
        layout.addWidget(self.tier_label)           # add current tier name
        layout.addLayout(self.gif_layout)           # add current featured players
        layout.addLayout(self.gif_layout_labels)    # add current featured players' labels
        layout.addLayout(self.player_layout)        # add list of players for current tier
        layout.addWidget(self.see_more_button)      # add see more button
        layout.addWidget(self.see_less_button)      # add see less button

        # make the base layout above scrollable 
        scroll_area = QScrollArea()                 # initialize scroll_area 
        scroll_area.setWidgetResizable(True)        # allow the scroll_area to change size
        scroll_area.setWidget(QWidget())            # create placeholder for content of scroll_area 
        scroll_area.widget().setLayout(layout)      # fill in placeholdrer with layout (a.k.a. the base layout that was just initialized)

        # create a main layout for current tier list
        main_layout = QVBoxLayout(self)             # initialize main layout as a vertical layout
        main_layout.addWidget(scroll_area)          # add scrollable base layout to main layout

    # method used to add featured players to correct layout
    def featured_players(self):
        # iterate through all players within current list of players (list is specific to tier)
        for player in self.current_players:
            player_label = QLabel(f"{player['name']}: {player['fppg']}")    # initialize player_label as cuurent player's name and fppg
            self.gif_layout_labels.addWidget(player_label)                  # add current player_label to gif_layout_labels

    # method used to return 3 random players from current tier
    def get_random_players(self):
        random.shuffle(self.players)
        return sorted(random.sample(self.players, 3), key=lambda x: x['fppg'], reverse=True)

    # method used to show entire list of players for current tier
    def show_full_tier(self):
        self.current_players = sorted(self.players, key=lambda x: x['fppg'], reverse=True)  # sort current list from most fppg to least

        # iterate through all players within current tier (after being sorted)
        for player in self.current_players:
            player_label = QLabel(f"{player['name']}: {player['fppg']}")    # initialize player_label as current player's name and fppg
            self.current_tier_list.append(player_label)                     # add current player to the tier list 
            self.player_layout.addWidget(player_label)                      # add current player to the player_layout

        self.see_more_button.hide() # hide the see more button
        self.see_less_button.show() # display the see less button 

    # method used to hide the entire list of players for current tier
    def hide_full_tier(self):
        #self.current_players = self.get_random_players()    # sort current list from most 

        # iterate through players in current tier list
        for label in self.current_tier_list:
            label.setParent(None)   # remove player from player_layout
            label.deleteLater()     # safely deletes label that held deleted player 

        self.current_tier_list = [] # assign tier list to be empty

        self.see_less_button.hide() # hide the see less button
        self.see_more_button.show() # show the see more button


# main class for handling the general program's gui
class FantasyBasketballApp(QWidget):

    # default constructor 
    def __init__(self):
        super().__init__()  # initialize parent class (QWidget) before anything else

        self.current_feature = None # initiliaze the focused feature to none

        self.init_ui()  # call init_ui function

    # gui method for program's main interface
    def init_ui(self):
        # create program's title with appropriate styling
        self.title_label = QLabel("Fantasy Basketball Tools")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # create home button with appropriate styling and connects clicked signal to show_home_page method
        self.home_button = QPushButton("Home")
        self.home_button.setStyleSheet("font-size: 18px;")
        self.home_button.clicked.connect(self.show_home_page)

        # create tier list button with appropriate styling and connects clicked signal to show_tier_list method
        self.tier_list_button = QPushButton("Tier List")
        self.tier_list_button.setStyleSheet("font-size: 18px;")
        self.tier_list_button.clicked.connect(self.show_tier_list)

        # create horizontal box layout for displaying feature buttons (inititally only displays tier list button)
        self.feature_layout = QHBoxLayout()
        self.feature_layout.addWidget(self.tier_list_button)  

        # create vertical box layout for displaying content (intially empty)
        self.content_layout = QVBoxLayout()

        # create veritcal box to organize and display main components of program
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)     # add title to be displayed
        main_layout.addLayout(self.content_layout)  # add content (initially empty)
        main_layout.addLayout(self.feature_layout)  # add featured button (initially just tier list button)

        # initialize window
        self.setLayout(main_layout)                     # main program's layout is set to main_layout (^ as seen above)
        self.setGeometry(100, 100, 800, 600)            # set initial dimensions of window
        self.setWindowTitle('Fantasy Basketball Tools') # initialize title of window
        self.show()                                     # display window

    # method used to assign a player's info to the corresponding tier list they belong in
    def add_to_tier(self, name, tier, fppg):

        player_info = {'name': name, 'fppg': fppg}  # initialize player_info as a dictionary mapping player's name to fppg

        if tier == 'S':
            s_tier_players.append(player_info)
        elif tier == 'A':
            a_tier_players.append(player_info)
        elif tier == 'B':
            b_tier_players.append(player_info)
        elif tier == 'C':
            c_tier_players.append(player_info)
        elif tier == 'D':
            d_tier_players.append(player_info)
        elif tier == 'F':
            f_tier_players.append(player_info)

    # method that is called when a user clicks the tier list button
    def show_tier_list(self):
        self.clear_content_layout()         # clear all currently displayed content
        self.current_feature = "Tier List"  # update the focused feature to tier list

        s_tier = PlayerTierWidget("S", s_tier_players)
        #a_tier = PlayerTierWidget("A", ["Player 4", "Player 5", "Player 6"])
        # Add more tiers as needed

        self.content_layout.addWidget(s_tier)
        #self.content_layout.addWidget(a_tier)
        # Add more tiers as needed

        self.update_title("Tier List")          # update the title
        self.update_feature_layout(["Home"])    # display the home button to return to main menu

    # method that is called when a user clicks the hoome button
    def show_home_page(self):
        self.clear_content_layout()                     # clear all currently displayed content
        self.current_feature = None                     # set current feature back to none
        self.update_title("Fantasy Basketball Tools")   # update the title
        self.update_feature_layout(["Tier List"])       # display available feature buttons

    # method that updates a title given a string
    def update_title(self, title):
        self.title_label.setText(title)

    # method that updates the feature button
    def update_feature_layout(self, feature_buttons):
        # iterate through each button currently in feature_layout
        while self.feature_layout.count():
            item = self.feature_layout.takeAt(0)    # remove current button
            if item.widget():
                item.widget().deleteLater()         # safely delete widget associated to button 

        # iterate through each string in list
        for button_text in feature_buttons:
            button = QPushButton(button_text)                   # initialize button as current string
            button.setStyleSheet("font-size: 18px;")            # style the button
            self.feature_layout.addWidget(button)               # add button to feature_layout
            button.clicked.connect(self.handle_feature_button)  # connect clicked signal of button to handle_feature_button method

    # method that connect signals to correct functions/methods
    def handle_feature_button(self):
        sender_button = self.sender()   # initialize sender_button as button from clicked signal

        # check the sender_button's text to call the correct function/method
        if sender_button.text() == "Tier List":
            self.show_tier_list()
        elif sender_button.text() == "Home":
            self.show_home_page()
        # Add more feature handlers as needed

    # method used to clear all displayed content
    def clear_content_layout(self):
        # iterate through each item in content_layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)    # delete current item
            if item.widget():
                item.widget().deleteLater()         # delete widget associated to item
