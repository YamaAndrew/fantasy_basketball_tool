## Python script to handle main gui for Fantasy Basketball Application ##

import tier_list_gui    # import script for tier list gui
# import PyQt libraries used for main gui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel 
from PyQt5.QtWidgets import QPushButton, QInputDialog, QLineEdit, QMessageBox, QScrollArea

# initialize empty lists to later store every player in a tier
s_tier_players = []
a_tier_players = []
b_tier_players = []
c_tier_players = []
d_tier_players = []
f_tier_players = []

#w = [1, 1, 2, 4, 4, 1, -2, 1, -1, 2, -1]

# main class for handling the general program's gui
class FantasyBasketballApp(QWidget):

    # default constructor 
    def __init__(self):
        super().__init__()  # initialize parent class (QWidget) before anything else

        self.current_feature = None                     # initialize the focused feature to none
        self.w = [1, 1, 2, 4, 4, 1, -2, 1, -1, 2, -1]   # initialize scoring system as empty list

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

        # create tier list button with appropriate styling and connects clicked signal to prompt_for_scoring_system method
        self.tier_list_button = QPushButton("Tier List")
        self.tier_list_button.setStyleSheet("font-size: 18px;")
        self.tier_list_button.clicked.connect(self.prompt_for_scoring_system)

        # create horizontal box layout for displaying feature buttons (inititally only displays tier list button)
        self.feature_layout = QHBoxLayout()
        self.feature_layout.addWidget(self.tier_list_button)  

        # create vertical box layout for displaying content (intially empty)
        self.content_layout = QVBoxLayout()

        # create veritcal box to organize and display main components of program
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)     # add title to be displayed
        layout.addLayout(self.content_layout)  # add content (initially empty)
        layout.addLayout(self.feature_layout)  # add featured button (initially just tier list button)

        # make the base layout above scrollable 
        scroll_area = QScrollArea()                 # initialize scroll_area 
        scroll_area.setWidgetResizable(True)        # allow the scroll_area to change size
        scroll_area.setWidget(QWidget())            # create placeholder for content of scroll_area 
        scroll_area.widget().setLayout(layout) # fill in placeholdrer with layout (a.k.a. the base layout that was just initialized)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)

        # initialize window
        self.setLayout(main_layout)                     # main program's layout is set to layout (^ as seen above)
        self.setGeometry(100, 100, 800, 600)            # set initial dimensions of window
        self.setWindowTitle('Fantasy Basketball Tools') # initialize title of window
        self.show()                                     # display window
    
    # method that prompts user to choose a scoring system (if tier list tool is selected)
    def prompt_for_scoring_system(self):
        # initialize options (standard or custom scoring system), choice (option selected), and ok (user clicks ok button)
        options = ["Standard ESPN Fantay Points League Scoring System", "Custom Scoring System"]
        choice, ok = QInputDialog.getItem(self, "Scoring System", "Select a scoring system:", options, 0, False)

        # if ok button is clicked AND a choice was selected...
        if ok and choice:
            # if user selected the standard espn scoring sytem, initialize scoring system weight
            if choice == "Standard ESPN Fantay Points League Scoring System":
                self.w = [1, 1, 2, 4, 4, 1, -2, 1, -1, 2, -1]
            # if user selected to make a custom scoring sytsem, display a pop up alert to give instructions
            else:
                custom_w, ok = QInputDialog.getText(self, "Custom Scoring System", 
                                                    "The stats used to calculate a player's fantasy value (Fantasy Points Per Game) are:\n"\
                                                    "\n"\
                                                    "Points Per Game,               Rebounds Per Game,              Assists Per Game,\n"\
                                                    "Blocks Per Game,               Steals Per Game,                3 Pointers Per Game,\n"\
                                                    "Turnovers Per Game,            Free Throws Made Per Game,      Free Throws Attempted Per Game,\n"\
                                                    "Field Goals Made Per Game,     Field Goals Attempted Per Game\n"\
                                                    "\n"\
                                                    "\n"\
                                                    "In this order (Points -> Rebounds -> ... -> Field Goals Attempted), enter a custom scoring system with comma-separated values\n"\
                                                    "\n"\
                                                    "Example: 1,1,2,4,4,1,-2,1,-1,2,-1)", QLineEdit.Normal)
                # if they enter a valid scoring system, initialize scoring system weight 
                if ok and custom_w:
                    self.w = [int(val) for val in custom_w.split(',')]
                # if the user canceled or entered invalid input...
                else:
                    self.w = [1, 1, 2, 4, 4, 1, -2, 1, -1, 2, -1]   # initialize weight as standard espn fantasy points league scoring weights
                    alert = QMessageBox()
                    alert.setIcon(QMessageBox.Warning)              # alert user of current situation
                    alert.setText("Uh oh!\n"\
                                  "\n"\
                                  "You either pressed 'Cancel' or input your custom scoring system incorrectly.\n"\
                                  "\n"\
                                  "The program will now use standard ESPN Fantasy Points League scoring.")
                    alert.setWindowTitle("Alert")
                    alert.exec()
        # if user clicks the cancel button...
        else:
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Warning)  # alert user of current situation
            alert.setText("Uh oh!\n"\
                            "\n"\
                            "You pressed 'Cancel'.\n"\
                            "\n"\
                            "The program will now use standard ESPN Fantasy Points League scoring.")
            alert.setWindowTitle("Alert")
            alert.exec()


    # method used to assign a player (with thier respective info) into the corresponding tier list they belong in
    def add_to_tier(self, name, points, rebounds, assists, blocks, steals, threes, turnovers, freeThrowsMade, 
                    freeThrowsAttempted, fieldGoalsMade, fieldGoalsAttempted, minutes, image, tier, fppg):

        player_info = [name, points, rebounds, assists, blocks, steals, threes, turnovers, freeThrowsMade, 
                    freeThrowsAttempted, fieldGoalsMade, fieldGoalsAttempted, minutes, image, fppg]  # initialize player_info as a list of all the player's information

        # append player to correct tier list
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

    # method that displays all tiers 
    def show_tier_list(self):
        self.clear_content_layout()         # clear all currently displayed content
        self.current_feature = "Tier List"  # update the focused feature to tier list
 
        # initialize variables to hold tier list gui
        s_tier = tier_list_gui.PlayerTierWidget("S", s_tier_players)
        a_tier = tier_list_gui.PlayerTierWidget("A", a_tier_players)
        b_tier = tier_list_gui.PlayerTierWidget("B", b_tier_players)
        c_tier = tier_list_gui.PlayerTierWidget("C", c_tier_players)
        d_tier = tier_list_gui.PlayerTierWidget("D", d_tier_players)
        f_tier = tier_list_gui.PlayerTierWidget("F", f_tier_players)

        # add each tier list gui to content 
        self.content_layout.addWidget(s_tier)
        self.content_layout.addWidget(a_tier)
        self.content_layout.addWidget(b_tier)
        self.content_layout.addWidget(c_tier)
        self.content_layout.addWidget(d_tier)
        self.content_layout.addWidget(f_tier)

        self.update_title("Tier List")          # update the title
        self.update_feature_layout(["Home"])    # display the home button to return to main menu

        # alert the user with a welcome message
        message_box = QMessageBox()
        message_box.setText("Welcome to the Tier List!\n"\
                            "\n"\
                            "View players grouped by average Fantasy Points Per Game (FPPG).\n"\
                            "\n"\
                            "Click 'See More' to see an entire tier of players in descending FPPG.")
        message_box.setIcon(QMessageBox.Information)
        message_box.exec_()
    
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

    # method that updates a title given a string
    def update_title(self, title):
        self.title_label.setText(title)

    # method that is called when a user clicks the hoome button
    def show_home_page(self):
        self.clear_content_layout()                     # clear all currently displayed content
        self.current_feature = None                     # set current feature back to none
        self.update_title("Fantasy Basketball Tools")   # update the title
        self.update_feature_layout(["Tier List"])       # display available feature buttons

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