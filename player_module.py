## Player class to create an object for every current NBA player ##

class Player:
    # Default constructor initializes player's name, points, rebounds, assists, blocks, steals, three pointers, 
    # turnovers, free throws made, free throws attempted, field goals made, and field goals attempted per game
    # Constructor also initializes  minutes played per game and a url linked to a png image of the player
    # For stats that are not recorded (ex. Moses Brown never attempting a three pointer) constructor sets value to 0.0
    def __init__ (self, name, ppg, rpg, apg, bpg, spg, fg3, tov, ftm, fta, fgm, fga, mpg, img):  

        self.name = name

        if ppg == None:
            self.ppg = 0.0
        else:
            self.ppg = float(ppg)

        if rpg == None:
            self.rpg == 0.0
        else:
            self.rpg = float(rpg)

        if apg == None:
            self.apg = 0.0
        else:
            self.apg = float(apg) 

        if bpg == None: 
            self.bpg = 0.0
        else:
            self.bpg = float(bpg)
        
        if spg == None:
            self.spg = 0.0
        else:
            self.spg = float(spg)
        
        if fg3 == None:
            self.fg3 = 0.0
        else:
            self.fg3 = float(fg3)
        
        if tov == None:
            self.tov = 0.0
        else: 
            self.tov = float(tov)
        
        if ftm == None:
            self.ftm = 0.0
        else:
            self.ftm = float(ftm)

        if fta == None:
            self.fta = 0.0
        else:
            self.fta = float(fta)
        
        if fgm == None:
            self.fgm = 0.0
        else:
            self.fgm = float(fgm)

        if fga == None:
            self.fga = 0.0
        else:
            self.fga = float(fga)
        
        if mpg == None:
            self.mpg = 0.0
        else:
            self.mpg = float(mpg)

        if img == None:
            self.img = ""
        else:
            self.img = img

    # Function takes in the weight for stats (excluding minutes per game) to calculate 
    # an individual player's fantasy points per game (fppg)
    def calculateFantasyScore (self, weights):

        self.fppg = [round((weights[0] * self.ppg) + (weights[1] * self.rpg) + (weights[2] * self.apg) + 
                       (weights[3] * self.bpg) + (weights[4] * self.spg) + (weights[5] * self.fg3) +
                       (weights[6] * self.tov) + (weights[7] * self.ftm) + (weights[8] * self.fta) +
                       (weights[9] * self.fgm) + (weights[10] * self.fga), 2)]
        
    # Function to classify a player's tier (based on average fppg)
    def classifyTier (self):

        if self.fppg[0] >= 50:
            self.tier = 'S'
        elif self.fppg[0] >= 40:
            self.tier = 'A'
        elif self.fppg[0] >= 30:
            self.tier = 'B'
        elif self.fppg[0] >= 20:
            self.tier = 'C'
        elif self.fppg[0] >= 10:
            self.tier = 'D'
        else:
            self.tier = 'F'