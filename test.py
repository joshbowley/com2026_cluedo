"""
Testing python code. Will eventually be extended to full unit tests. 
"""

from board import _ADJACENCY_MAP as adj_map, Board


def check_reciprocity(adjacency_map):
    error = []
    for position, neighbours in adjacency_map.items():
        for neighbour in neighbours:
            if neighbour not in adjacency_map:
                error.append(f"{neighbour} is listed as neighbour of {position} but has no entry in map")
            elif position not in adjacency_map[neighbour]:
                error.append(f"{position} -> {neighbour} exists but {neighbour} -> {position} does not")
    return error

errors = check_reciprocity(adj_map)
if errors:
    for err in errors:
        print(err)
else:
    print("All connections reciprocal")


# checking get_valid_moves method. 
board = Board()

moves = board.get_valid_moves((9,6), 2, [])
print(moves)

moves = board.get_valid_moves("Lounge", 3, [])
print(moves)

moves = board.get_valid_moves("Hall", 1, [])
print(moves)

# checking is_room method.

print(board.is_room("Kitchen"))

print(board.is_room("(4,5)"))

print(board.is_room("NotARoom"))

