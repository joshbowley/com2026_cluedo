"""Display file. Keeps rendering seperate from game logic."""

from board import _ROOM_CELLS, _ROOM_NAMES, _STARTING_POSITIONS, _ADJACENCY_MAP

_OBJECT_SYMBOLS = {
    "Kitchen": "Ki",
    "Ballroom": "Ba",
    "Conservatory": "Co",
    "Billiard Room": "Bi",
    "Library": "Li",
    "Study": "St",
    "Hall": "Ha",
    "Lounge": "Lo",
    "Dining Room": "Di",

    "Central Room": "Ce",

    "Corridor": "..",
    "Empty/Wall": "  ",

    "Miss Scarlett": "MS",
    "Prof Plum": "PP",
    "Mrs Peacock": "MP",
    "Rev Green": "RG",
    "Mrs White": "MW",
    "Col Mustard": "CM"    
}

# Added 1 to both height and width as dictionary coordinates start on 1
# also can print row and column labels as margins
_WIDTH = 25
_HEIGHT = 26




def Render(current_positions: tuple | str) -> None: 
    """Function to render the board in it's current state."""
    
    grid = [["  " for col in range(_WIDTH)] for row in range(_HEIGHT)]


    for columnNum in range(_WIDTH): 
        grid[0][columnNum] = columnNum

    for rowNum in range(_HEIGHT):
        grid[rowNum][0] = rowNum

    # loop through room interiors
    for key, values in _ROOM_CELLS.items(): 
        for value in values:
            grid[value[0]][value[1]] = _OBJECT_SYMBOLS[key]

    # loop through corridor squares
    for key in _ADJACENCY_MAP.keys():
        if isinstance(key, tuple):
            grid[key[0]][key[1]] = _OBJECT_SYMBOLS["Corridor"]

    # player tokens
    for character, position in _STARTING_POSITIONS.items():
        grid[position[0]][position[1]] = _OBJECT_SYMBOLS[character]

    for row in grid:
        for cell in row:
            print(str(cell).ljust(2), end=" ")
        print()

Render(_STARTING_POSITIONS)
