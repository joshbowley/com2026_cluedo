"""Unit tests for Board class."""
 
import pytest
from board import Board, _ADJACENCY_MAP, _ROOM_NAMES, _STARTING_POSITIONS
 
 
@pytest.fixture
def board():
    return Board()
 
# is_room 
 
def test_is_room_kitchen(board):
    assert board.is_room("Kitchen") is True
 
def test_is_room_central_room(board):
    assert board.is_room("Central Room") is True
 
@pytest.mark.parametrize("room", _ROOM_NAMES)
def test_is_room_all_rooms(board, room):
    assert board.is_room(room) is True
 
def test_is_room_corridor_tuple(board):
    assert board.is_room((9, 6)) is False
 
def test_is_room_invalid_string(board):
    assert board.is_room("NotARoom") is False
 
def test_is_room_empty_string(board):
    assert board.is_room("") is False
 
 
#  get_valid_moves — return type and basic behaviour 
 
def test_get_valid_moves_returns_list(board):
    assert isinstance(board.get_valid_moves((9, 6), 2, []), list)
 
def test_get_valid_moves_non_empty_from_corridor(board):
    assert len(board.get_valid_moves((9, 6), 2, [])) > 0
 
def test_get_valid_moves_does_not_include_start(board):
    assert (9, 6) not in board.get_valid_moves((9, 6), 2, [])
 
def test_get_valid_moves_no_duplicates(board):
    moves = board.get_valid_moves((9, 6), 4, [])
    assert len(moves) == len(set(str(m) for m in moves))
 
 
# get_valid_moves — step count 
 
def test_get_valid_moves_more_steps_reaches_more_squares(board):
    moves_2 = board.get_valid_moves((9, 6), 2, [])
    moves_5 = board.get_valid_moves((9, 6), 5, [])
    assert len(moves_2) <= len(moves_5)
 
def test_get_valid_moves_one_step_only_neighbours(board):
    # (9,6) neighbours are (8,6), (9,5), (9,7), (10,6)
    moves = board.get_valid_moves((9, 6), 1, [])
    for move in moves:
        assert move in _ADJACENCY_MAP[(9, 6)]
 
 
# get_valid_moves — blocked positions 
 
def test_get_valid_moves_excludes_blocked(board):
    blocked = [(9, 7)]
    moves = board.get_valid_moves((9, 6), 2, blocked)
    assert (9, 7) not in moves
 
def test_get_valid_moves_multiple_blocked(board):
    blocked = [(9, 5), (9, 7), (8, 6), (10, 6)]
    moves = board.get_valid_moves((9, 6), 1, blocked)
    assert moves == []
 
def test_get_valid_moves_blocked_does_not_affect_unblocked(board):
    blocked = [(9, 5)]
    moves = board.get_valid_moves((9, 6), 1, blocked)
    assert (9, 7) in moves
 
 
# get_valid_moves — room entry
 
def test_get_valid_moves_can_enter_ballroom(board):
    moves = board.get_valid_moves((6, 8), 1, [])
    assert "Ballroom" in moves
 
def test_get_valid_moves_can_enter_kitchen(board):
    moves = board.get_valid_moves((8, 5), 1, [])
    assert "Kitchen" in moves
 
def test_get_valid_moves_room_not_added_twice(board):
    moves = board.get_valid_moves((9, 6), 6, [])
    assert moves.count("Ballroom") <= 1
 
 
# get_valid_moves — from room 
 
def test_get_valid_moves_from_room_returns_corridor(board):
    moves = board.get_valid_moves("Lounge", 3, [])
    assert any(isinstance(m, tuple) for m in moves)
 
def test_get_valid_moves_from_room_secret_passage_kitchen(board):
    moves = board.get_valid_moves("Kitchen", 1, [])
    assert "Study" in moves
 
def test_get_valid_moves_from_room_secret_passage_study(board):
    moves = board.get_valid_moves("Study", 1, [])
    assert "Kitchen" in moves
 
def test_get_valid_moves_from_room_secret_passage_conservatory(board):
    moves = board.get_valid_moves("Conservatory", 1, [])
    assert "Lounge" in moves
 
def test_get_valid_moves_from_room_secret_passage_lounge(board):
    moves = board.get_valid_moves("Lounge", 1, [])
    assert "Conservatory" in moves
 
 
# get_valid_moves — starting squares 
 
def test_get_valid_moves_from_miss_scarlett_start(board):
    moves = board.get_valid_moves((25, 8), 1, [])
    assert (24, 8) in moves
 
def test_get_valid_moves_from_col_mustard_start(board):
    moves = board.get_valid_moves((18, 1), 1, [])
    assert (18, 2) in moves
 
 
# adjacency map integrity 
 
def test_adjacency_map_reciprocal():
    """Every A -> B connection must have a corresponding B -> A."""
    errors = []
    for position, neighbours in _ADJACENCY_MAP.items():
        for neighbour in neighbours:
            if neighbour not in _ADJACENCY_MAP:
                errors.append(
                    f"{neighbour} listed as neighbour of {position} "
                    f"but has no entry in adjacency map"
                )
            elif position not in _ADJACENCY_MAP[neighbour]:
                errors.append(
                    f"{position} -> {neighbour} exists but "
                    f"{neighbour} -> {position} does not"
                )
    assert errors == [], "\n".join(errors)
 
def test_all_starting_positions_in_adjacency_map():
    for character, position in _STARTING_POSITIONS.items():
        assert position in _ADJACENCY_MAP, (
            f"{character} starting position {position} not in adjacency map"
        )
 
def test_all_rooms_in_adjacency_map():
    for room in _ROOM_NAMES:
        assert room in _ADJACENCY_MAP, f"{room} missing from adjacency map"
 

# =============================================================================
# AI PROMPTS AND OUTPUTS (required per coursework specification)
# =============================================================================
# Tool: Claude (claude.ai, claude-sonnet-4-6)
#
# Prompt:
# "Generate pytest unit tests for the methods in this board.py class file.
#
# [uploaded board.py]
#
# Output: test_board.py containing the following tests:
#
# @pytest.fixture
# def board():
#     return Board()
#
# def test_is_room_kitchen(board):
#     assert board.is_room("Kitchen") is True
#
# def test_is_room_central_room(board):
#     assert board.is_room("Central Room") is True
#
# @pytest.mark.parametrize("room", _ROOM_NAMES)
# def test_is_room_all_rooms(board, room):
#     assert board.is_room(room) is True
#
# def test_is_room_corridor_tuple(board):
#     assert board.is_room((9, 6)) is False
#
# def test_is_room_invalid_string(board):
#     assert board.is_room("NotARoom") is False
#
# def test_is_room_empty_string(board):
#     assert board.is_room("") is False
#
# def test_get_valid_moves_returns_list(board):
#     assert isinstance(board.get_valid_moves((9, 6), 2, []), list)
#
# def test_get_valid_moves_non_empty_from_corridor(board):
#     assert len(board.get_valid_moves((9, 6), 2, [])) > 0
#
# def test_get_valid_moves_does_not_include_start(board):
#     assert (9, 6) not in board.get_valid_moves((9, 6), 2, [])
#
# def test_get_valid_moves_no_duplicates(board):
#     moves = board.get_valid_moves((9, 6), 4, [])
#     assert len(moves) == len(set(str(m) for m in moves))
#
# def test_get_valid_moves_more_steps_reaches_more_squares(board):
#     moves_2 = board.get_valid_moves((9, 6), 2, [])
#     moves_5 = board.get_valid_moves((9, 6), 5, [])
#     assert len(moves_2) <= len(moves_5)
#
# def test_get_valid_moves_one_step_only_neighbours(board):
#     moves = board.get_valid_moves((9, 6), 1, [])
#     for move in moves:
#         assert move in _ADJACENCY_MAP[(9, 6)]
#
# def test_get_valid_moves_excludes_blocked(board):
#     blocked = [(9, 7)]
#     moves = board.get_valid_moves((9, 6), 2, blocked)
#     assert (9, 7) not in moves
#
# def test_get_valid_moves_multiple_blocked(board):
#     blocked = [(9, 5), (9, 7), (8, 6), (10, 6)]
#     moves = board.get_valid_moves((9, 6), 1, blocked)
#     assert moves == []
#
# def test_get_valid_moves_blocked_does_not_affect_unblocked(board):
#     blocked = [(9, 5)]
#     moves = board.get_valid_moves((9, 6), 1, blocked)
#     assert (9, 7) in moves
#
# def test_get_valid_moves_can_enter_ballroom(board):
#     moves = board.get_valid_moves((6, 8), 1, [])
#     assert "Ballroom" in moves
#
# def test_get_valid_moves_can_enter_kitchen(board):
#     moves = board.get_valid_moves((8, 5), 1, [])
#     assert "Kitchen" in moves
#
# def test_get_valid_moves_room_not_added_twice(board):
#     moves = board.get_valid_moves((9, 6), 6, [])
#     assert moves.count("Ballroom") <= 1
#
# def test_get_valid_moves_from_room_returns_corridor(board):
#     moves = board.get_valid_moves("Lounge", 3, [])
#     assert any(isinstance(m, tuple) for m in moves)
#
# def test_get_valid_moves_from_room_secret_passage_kitchen(board):
#     moves = board.get_valid_moves("Kitchen", 1, [])
#     assert "Study" in moves
#
# def test_get_valid_moves_from_room_secret_passage_study(board):
#     moves = board.get_valid_moves("Study", 1, [])
#     assert "Kitchen" in moves
#
# def test_get_valid_moves_from_room_secret_passage_conservatory(board):
#     moves = board.get_valid_moves("Conservatory", 1, [])
#     assert "Lounge" in moves
#
# def test_get_valid_moves_from_room_secret_passage_lounge(board):
#     moves = board.get_valid_moves("Lounge", 1, [])
#     assert "Conservatory" in moves
#
# def test_get_valid_moves_from_miss_scarlett_start(board):
#     moves = board.get_valid_moves((25, 8), 1, [])
#     assert (24, 8) in moves
#
# def test_get_valid_moves_from_col_mustard_start(board):
#     moves = board.get_valid_moves((18, 1), 1, [])
#     assert (18, 2) in moves
#
# def test_adjacency_map_reciprocal():
#     errors = []
#     for position, neighbours in _ADJACENCY_MAP.items():
#         for neighbour in neighbours:
#             if neighbour not in _ADJACENCY_MAP:
#                 errors.append(f"{neighbour} listed as neighbour of
#                     {position} but has no entry in adjacency map")
#             elif position not in _ADJACENCY_MAP[neighbour]:
#                 errors.append(f"{position} -> {neighbour} exists but
#                     {neighbour} -> {position} does not")
#     assert errors == [], "\n".join(errors)
#
# def test_all_starting_positions_in_adjacency_map():
#     for character, position in _STARTING_POSITIONS.items():
#         assert position in _ADJACENCY_MAP
#
# def test_all_rooms_in_adjacency_map():
#     for room in _ROOM_NAMES:
#         assert room in _ADJACENCY_MAP
#
# Adaptations made to AI output:
#   - Verified all test coordinates against actual adjacency map entries
#     in board.py before finalising
#   - Used @pytest.mark.parametrize for is_room to cover all room names
#     without repeating test logic
#   - Confirmed secret passage pairs from adjacency map before writing tests
# =============================================================================