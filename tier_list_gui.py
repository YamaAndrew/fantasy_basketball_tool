##  Python script to handle gui for each tier in tier list function ##

import random, requests                                                             # imports for randomization and get requests
# imports for needed PyQt libraries
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton 
from PyQt5.QtGui import QMovie, QPixmap, QImage
from PyQt5.QtNetwork import QNetworkAccessManager
from PyQt5.QtCore import Qt, QObject, pyqtSignal

# Add a signal class
class Signal(QObject):
    imageDownloaded = pyqtSignal(QImage)

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

        # Add this line to create an instance of the Signal class
        self.signal = Signal()

        # Create instance variable for image_layout
        self.image_layout = QHBoxLayout()

        # Create a single instance of QNetworkAccessManager
        self.network_manager = QNetworkAccessManager()

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
        
        self.image_layout = QHBoxLayout() # initialize horizontal layout for gifs

        # display gifs for S and A tier players
        if self.tier_name == 'S' or self.tier_name == 'A':
            for player in self.current_players:
                gif_label = QLabel()
                movie = QMovie(f"player_images/{player[0]}.gif")
                #print(player[0])
                gif_label.setMovie(movie)
                movie.start()
                gif_label.setFixedSize(200, 200)
                self.image_layout.addWidget(gif_label)

        # display standard nba headshots for all other players
        else:
            for player in self.current_players:
                if player[13]:
                    image_url = player[13]  # access image url
                    image_label = QLabel()
                    # Download the image from the URL
                    response = requests.get(image_url)
                    image_data = response.content

                    # Create a QPixmap from the image data
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)
                    pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                    # Set the QPixmap to the QLabel
                    image_label.setPixmap(pixmap)
                    self.image_layout.addWidget(image_label)

                # display a "error" picture for players with inconsistent naming (ex. Luka Doncic vs Luka Dončić)
                else:
                    image_path = "player_images/crying jordan.jpg"
                    pixmap = QPixmap(image_path).scaled(100,100)

                    # Create a QLabel and set the pixmap
                    image_label = QLabel(self)
                    image_label.setPixmap(pixmap)

                    # Add the QLabel to the layout
                    self.image_layout.addWidget(image_label)

        self.image_layout_labels = QHBoxLayout()  # initialize horizontal layout for the image_layout's labels
        self.featured_players()                 # call method to add featured players to image_layout_labels layout

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
        layout.addLayout(self.image_layout)           # add current featured players
        layout.addLayout(self.image_layout_labels)    # add current featured players' labels
        layout.addLayout(self.player_layout)        # add list of players for current tier
        layout.addWidget(self.see_more_button)      # add see more button
        layout.addWidget(self.see_less_button)      # add see less button

        self.setLayout(layout)

    # method used to add featured players to correct layout
    def featured_players(self):
        # iterate through all players within current list of players (list is specific to tier)
        for player in self.current_players:
            player_label = QLabel(f"{player[0]}: {player[14]}")    # initialize player_label as cuurent player's name and fppg
            self.image_layout_labels.addWidget(player_label)                  # add current player_label to image_layout_labels

    # method used to return 3 random players from current tier
    def get_random_players(self):
        random.shuffle(self.players)
        return sorted(random.sample(self.players, 3), key=lambda x: x[14], reverse=True)

    # method used to show entire list of players for current tier
    def show_full_tier(self):
        self.current_players = sorted(self.players, key=lambda x: x[14], reverse=True)  # sort current list from most fppg to least

        # iterate through all players within current tier (after being sorted)
        for player in self.current_players:
            player_label = QLabel(f"{player[0]}: {player[14]}")    # initialize player_label as current player's name and fppg
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

    # method used to make sure an image is downloadable
    def handle_download_finished(self, reply, player_image_url):
        # print error message if image isn't loaded
        if reply.error():
            print(f"Error downloading image from {player_image_url}: {reply.errorString()}")
        else:
            data = reply.readAll()          # read in data (image)
            image = QImage.fromData(data)   # create QImage of data received
            # create usable image if an image was actually downloaded
            if not image.isNull():
                self.handleDownloadedImage(image)
            else:
                print(f"Failed to load image from {player_image_url}")
                print(f"Error details: Unable to create QImage from data")

    # method used to display a player's headshot photo
    def handleDownloadedImage(self, image):
        image_label = QLabel()                          # create new QLabel 
        image_label.setPixmap(QPixmap.fromImage(image)) # convert QLabel to QPixmap to display image later
        self.image_layout.addWidget(image_label)        # add QPixmap to layout to be displayed