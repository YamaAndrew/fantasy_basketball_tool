# Fantasy Basketball Tool

This is a Python application meant to aid managers of fantasy basketball teams.

The Graphical User Interface (GUI) is created using PyQt, a Python bindings of the Qt platform.

As of now (Last edited: 12/12/23) there is one feature: Tier List.


## Tier List

This feature's design can be segmented into 3 main parts: Web Scraping, Object Oriented Programming (OOP), GUI.

The Web Scraping is handled in web_scraping.py using the Beautiful Soup library. Per game stats (ex. points, rebounds, etc.) are taken from 
https://www.basketball-reference.com/leagues/NBA_2024_per_game.html to be stored and then proccess into new data (a.k.a. Fantasy Points Per Game).

The OOP used is the Python class data structure to make a Player class. This allows for the creation of a Player objects, where each represents an
NBA player that was scraped in web_scraping.py. Each player object holds their respective player's information from the program's web scraping.

The Tier List GUI handles each tier's functionality one at a time. It is here where many of this feature's front end aspects are handled, including: 
exiting the tier list page, organizing/displaying tier sections/subsectins, and selecting/displaying random featured players' images. 
