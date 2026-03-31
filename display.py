"""Display file. Keeps rendering seperate from game logic."""

from board import _ROOM_CELLS, _STARTING_POSITIONS, _ADJACENCY_MAP
from colorama import Fore, Back, Style, init

init()

_COLOURS = {
    "Room": Back.CYAN + Fore.WHITE,

    "Central Room": Back.BLUE + Fore.WHITE,

    "Corridor": Back.YELLOW + Fore.BLACK,

    "Empty/Wall": Style.RESET_ALL,

    "Miss Scarlett": Back.RED + Fore.WHITE,
    "Prof Plum": Back.MAGENTA + Fore.WHITE,
    "Mrs Peacock": Back.BLUE + Fore.WHITE,
    "Rev Green": Back.GREEN + Fore.WHITE,
    "Mrs White": Back.WHITE + Fore.BLACK,
    "Col Mustard": Back.YELLOW + Fore.WHITE, 

    "Valid Move": Back.GREEN + Fore.BLACK, 
    "Doorway": Back.LIGHTGREEN_EX + Fore.BLACK
}
_RESET = Style.RESET_ALL


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
    "Doorway": "..",
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




def render(current_positions: dict, valid_moves: list = [] ) -> None: 
    """Function to render the board in it's current state."""
    
    grid = [["  " for col in range(_WIDTH)] for row in range(_HEIGHT)]


    for columnNum in range(_WIDTH): 
        grid[0][columnNum] = columnNum

    for rowNum in range(_HEIGHT):
        grid[rowNum][0] = rowNum

    # loop through room interiors

    for room_name, cells in _ROOM_CELLS.items():
        colour = _COLOURS["Central Room"] if room_name == "Central Room" else _COLOURS["Room"]
        for cell in cells:
            grid[cell[0]][cell[1]] = colour + _OBJECT_SYMBOLS[room_name] + _RESET

    # loop through corridor squares
    # corridor squares
    for key in _ADJACENCY_MAP.keys():
        if isinstance(key, tuple):
            grid[key[0]][key[1]] = _COLOURS["Corridor"] + _OBJECT_SYMBOLS["Corridor"] + _RESET

    for room_name, neighbours in _ADJACENCY_MAP.items():
        if isinstance(room_name, str) and room_name != "Central Room":
            for neighbour in neighbours:
                if isinstance(neighbour, tuple):
                    if _OBJECT_SYMBOLS["Corridor"] + _RESET in grid[neighbour[0]][neighbour[1]]:
                        grid[neighbour[0]][neighbour[1]] = _COLOURS["Doorway"] + _OBJECT_SYMBOLS["Doorway"] + _RESET


    for i, move in enumerate(valid_moves, 1):
        label = str(i).ljust(2)
        if isinstance(move, tuple):
            grid[move[0]][move[1]] = _COLOURS["Valid Move"] + label + _RESET
        elif isinstance(move, str):
            for neighbour in _ADJACENCY_MAP.get(move, []):
                if isinstance(neighbour, tuple):
                    grid[neighbour[0]][neighbour[1]] = _COLOURS["Valid Move"] + label + _RESET
    
    # player tokens
    for character, position in current_positions.items():
        if isinstance(position, tuple): # only draws in in corridor
            grid[position[0]][position[1]] = _COLOURS[character] + _OBJECT_SYMBOLS[character] + _RESET

    for row in grid:
        for cell in row:
            print(str(cell).ljust(2), end=" ")
        print()

