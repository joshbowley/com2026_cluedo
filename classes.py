"""
Thoughts about inheritance/OOP considerations:

Player class -> player object defined in setup

Card class -> seperate WHO, WHAT and WHERE classes **(red bonus card class) -> specific cards

Location class -> room class, corridor and center of board instances -> specific rooms

Dice class

"""

class Player(): 
    """
    Player
    """
    def __init__(self):




class Location(): 
    """
    Location
    """
    def __init__(self):

class Room(Location):
    """
    Room
    """
    def __init__(self):
        super().__init__()

class Corridor(Location):
    """
    Room
    """
    def __init__(self):
        super().__init__()

class CenterOfBoard(Location):
    """
    Center of Board
    """
    def __init__(self):
        super().__init__()

class Dice():
    """
    Dice
    """
    def __init__(self):
        pass