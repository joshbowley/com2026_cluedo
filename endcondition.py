"""Class for end conditions of Cluedo game."""

from enum import Enum, auto

class EndCondition(Enum):
    CORRECT_ACCUSATION = auto()
    WRONG_ACCUSATION = auto() # player eliminated from game
    ALL_ELIMINATED = auto() # everyone made false accusations
