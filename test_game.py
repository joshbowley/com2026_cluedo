"""Unit tests for Game class."""
 
import pytest
from unittest.mock import patch
from game import Game, _SUSPECTS, _WEAPONS, _ROOMS
from player import Player
from cards import Card
from endcondition import EndCondition
from board import _STARTING_POSITIONS
 
 
@pytest.fixture
def game():
    """Return a bare Game instance with no players."""
    return Game()
 
 
@pytest.fixture
def game_two_players():
    """Return a Game with two players set up and cards dealt."""
    g = Game()
    p1 = Player("Alice", "Miss Scarlett")
    p2 = Player("Bob", "Prof Plum")
    p1.move_to(_STARTING_POSITIONS["Miss Scarlett"])
    p2.move_to(_STARTING_POSITIONS["Prof Plum"])
    g.current_positions["Miss Scarlett"] = _STARTING_POSITIONS["Miss Scarlett"]
    g.current_positions["Prof Plum"] = _STARTING_POSITIONS["Prof Plum"]
    g.players = [p1, p2]
    g.deal_cards()
    return g
 
 
@pytest.fixture
def game_three_players():
    """Return a Game with three players set up and cards dealt."""
    g = Game()
    for name, char in [("Alice", "Miss Scarlett"), ("Bob", "Prof Plum"), ("Carol", "Rev Green")]:
        p = Player(name, char)
        p.move_to(_STARTING_POSITIONS[char])
        g.current_positions[char] = _STARTING_POSITIONS[char]
        g.players.append(p)
    g.deal_cards()
    return g
 
 
# __init__ 
 
def test_init_players_empty(game):
    assert game.players == []
 
def test_init_solution_empty(game):
    assert game.solution == {}
 
def test_init_face_up_cards_empty(game):
    assert game.face_up_cards == []
 
def test_init_current_positions_empty(game):
    assert game.current_positions == {}
 
def test_init_turn_index_zero(game):
    assert game._turn_index == 0
 
def test_init_current_player_none(game):
    assert game._current_player is None
 
 
# deal_cards 
 
def test_deal_cards_solution_has_three_keys(game_two_players):
    assert set(game_two_players.solution.keys()) == {"Suspect", "Weapon", "Room"}
 
def test_deal_cards_solution_suspect_category(game_two_players):
    assert game_two_players.solution["Suspect"].category == "Suspect"
 
def test_deal_cards_solution_weapon_category(game_two_players):
    assert game_two_players.solution["Weapon"].category == "Weapon"
 
def test_deal_cards_solution_room_category(game_two_players):
    assert game_two_players.solution["Room"].category == "Room"
 
def test_deal_cards_all_cards_accounted_for(game_two_players):
    """Verify solution + all hands + face-up equals total deck."""
    total = len(_SUSPECTS) + len(_WEAPONS) + len(_ROOMS)
    dealt = sum(len(p.hand) for p in game_two_players.players)
    face_up = len(game_two_players.face_up_cards)
    solution = len(game_two_players.solution)
    assert dealt + face_up + solution == total
 
def test_deal_cards_no_duplicates(game_two_players):
    all_names = []
    for p in game_two_players.players:
        all_names.extend([c.name for c in p.hand])
    all_names.extend([c.name for c in game_two_players.face_up_cards])
    all_names.extend([c.name for c in game_two_players.solution.values()])
    assert len(all_names) == len(set(all_names))
 
def test_deal_cards_solution_not_in_any_hand(game_two_players):
    """Verify no solution card appears in any player's hand."""
    solution_names = {c.name for c in game_two_players.solution.values()}
    for p in game_two_players.players:
        hand_names = {c.name for c in p.hand}
        assert solution_names.isdisjoint(hand_names)
 
def test_deal_cards_three_players_all_accounted_for(game_three_players):
    total = len(_SUSPECTS) + len(_WEAPONS) + len(_ROOMS)
    dealt = sum(len(p.hand) for p in game_three_players.players)
    face_up = len(game_three_players.face_up_cards)
    solution = len(game_three_players.solution)
    assert dealt + face_up + solution == total
 
 
# _advance_turn
 
def test_advance_turn_increments_index(game_two_players):
    game_two_players._advance_turn()
    assert game_two_players._turn_index == 1
 
def test_advance_turn_wraps_around(game_two_players):
    game_two_players._turn_index = 1
    game_two_players._advance_turn()
    assert game_two_players._turn_index == 0
 
def test_advance_turn_three_players(game_three_players):
    game_three_players._advance_turn()
    game_three_players._advance_turn()
    game_three_players._advance_turn()
    assert game_three_players._turn_index == 0
 
 
# _find_player_by_character 
 
def test_find_player_by_character_returns_correct_player(game_two_players):
    result = game_two_players._find_player_by_character("Miss Scarlett")
    assert result is not None
    assert result.name == "Alice"
 
def test_find_player_by_character_second_player(game_two_players):
    result = game_two_players._find_player_by_character("Prof Plum")
    assert result.name == "Bob"
 
def test_find_player_by_character_not_found_returns_none(game_two_players):
    result = game_two_players._find_player_by_character("Rev Green")
    assert result is None
 
 
# handle_accusation 
 
def test_handle_accusation_correct_returns_correct_accusation(game_two_players):
    player = game_two_players.players[0]
    sol = game_two_players.solution
    inputs = [
        sol["Suspect"].name,
        sol["Weapon"].name,
        sol["Room"].name,
    ]
    # _prompt_from_list picks by index — find index of each solution card
    suspect_names = [c.name for c in _SUSPECTS]
    weapon_names  = [c.name for c in _WEAPONS]
    room_names    = [c.name for c in _ROOMS]
    s_idx = str(suspect_names.index(sol["Suspect"].name) + 1)
    w_idx = str(weapon_names.index(sol["Weapon"].name) + 1)
    r_idx = str(room_names.index(sol["Room"].name) + 1)
    with patch("builtins.input", side_effect=[s_idx, w_idx, r_idx]):
        result = game_two_players.handle_accusation(player)
    assert result == EndCondition.CORRECT_ACCUSATION
 
def test_handle_accusation_wrong_eliminates_player(game_two_players):
    player = game_two_players.players[0]
    sol = game_two_players.solution
    suspect_names = [c.name for c in _SUSPECTS]
    weapon_names  = [c.name for c in _WEAPONS]
    room_names    = [c.name for c in _ROOMS]
    # pick deliberately wrong answers
    wrong_suspect = next(
        c for c in _SUSPECTS if c.name != sol["Suspect"].name)
    wrong_weapon  = next(
        c for c in _WEAPONS  if c.name != sol["Weapon"].name)
    wrong_room    = next(
        c for c in _ROOMS    if c.name != sol["Room"].name)
    s_idx = str(suspect_names.index(wrong_suspect.name) + 1)
    w_idx = str(weapon_names.index(wrong_weapon.name) + 1)
    r_idx = str(room_names.index(wrong_room.name) + 1)
    with patch("builtins.input", side_effect=[s_idx, w_idx, r_idx]):
        game_two_players.handle_accusation(player)
    assert player.is_active is False
 
def test_handle_accusation_wrong_returns_wrong_accusation(game_two_players):
    player = game_two_players.players[0]
    sol = game_two_players.solution
    suspect_names = [c.name for c in _SUSPECTS]
    weapon_names  = [c.name for c in _WEAPONS]
    room_names    = [c.name for c in _ROOMS]
    wrong_suspect = next(c for c in _SUSPECTS if c.name != sol["Suspect"].name)
    wrong_weapon  = next(c for c in _WEAPONS  if c.name != sol["Weapon"].name)
    wrong_room    = next(c for c in _ROOMS    if c.name != sol["Room"].name)
    s_idx = str(suspect_names.index(wrong_suspect.name) + 1)
    w_idx = str(weapon_names.index(wrong_weapon.name) + 1)
    r_idx = str(room_names.index(wrong_room.name) + 1)
    with patch("builtins.input", side_effect=[s_idx, w_idx, r_idx]):
        result = game_two_players.handle_accusation(player)
    assert result == EndCondition.WRONG_ACCUSATION
 
def test_handle_accusation_all_eliminated(game_two_players):
    """Verify ALL_ELIMINATED returned when last active player
    accuses wrongly.

    Manually set the second player inactive before calling
    handle_accusation to simulate the last remaining active
    player making a wrong accusation.
    """    
    game_two_players.players[1].is_active = False
    player = game_two_players.players[0]
    sol = game_two_players.solution
    suspect_names = [c.name for c in _SUSPECTS]
    weapon_names  = [c.name for c in _WEAPONS]
    room_names    = [c.name for c in _ROOMS]
    wrong_suspect = next(c for c in _SUSPECTS if c.name != sol["Suspect"].name)
    wrong_weapon  = next(c for c in _WEAPONS  if c.name != sol["Weapon"].name)
    wrong_room    = next(c for c in _ROOMS    if c.name != sol["Room"].name)
    s_idx = str(suspect_names.index(wrong_suspect.name) + 1)
    w_idx = str(weapon_names.index(wrong_weapon.name) + 1)
    r_idx = str(room_names.index(wrong_room.name) + 1)
    with patch("builtins.input", side_effect=[s_idx, w_idx, r_idx]):
        result = game_two_players.handle_accusation(player)
    assert result == EndCondition.ALL_ELIMINATED


# =============================================================================
# AI PROMPTS AND OUTPUTS (required per coursework specification)
# =============================================================================
# Tool: Claude (claude.ai, claude-sonnet-4-6)
#
# Prompt 1:
# "Generate pytest unit tests for the methods in this game.py class file.
#
# [uploaded game.py]
#
# Output 1: test_game.py containing the following tests:
#
# @pytest.fixture
# def game():
#     return Game()
#
# @pytest.fixture
# def game_two_players():
#     g = Game()
#     p1 = Player("Alice", "Miss Scarlett")
#     p2 = Player("Bob", "Prof Plum")
#     p1.move_to(_STARTING_POSITIONS["Miss Scarlett"])
#     p2.move_to(_STARTING_POSITIONS["Prof Plum"])
#     g.current_positions["Miss Scarlett"] = _STARTING_POSITIONS["Miss Scarlett"]
#     g.current_positions["Prof Plum"] = _STARTING_POSITIONS["Prof Plum"]
#     g.players = [p1, p2]
#     g.deal_cards()
#     return g
#
# @pytest.fixture
# def game_three_players():
#     g = Game()
#     for name, char in [("Alice", "Miss Scarlett"),
#                         ("Bob", "Prof Plum"),
#                         ("Carol", "Rev Green")]:
#         p = Player(name, char)
#         p.move_to(_STARTING_POSITIONS[char])
#         g.current_positions[char] = _STARTING_POSITIONS[char]
#         g.players.append(p)
#     g.deal_cards()
#     return g
#
# def test_init_players_empty(game):
#     assert game.players == []
#
# def test_init_solution_empty(game):
#     assert game.solution == {}
#
# def test_init_face_up_cards_empty(game):
#     assert game.face_up_cards == []
#
# def test_init_current_positions_empty(game):
#     assert game.current_positions == {}
#
# def test_init_turn_index_zero(game):
#     assert game._turn_index == 0
#
# def test_init_current_player_none(game):
#     assert game._current_player is None
#
# def test_deal_cards_solution_has_three_keys(game_two_players):
#     assert set(game_two_players.solution.keys()) == {"Suspect","Weapon","Room"}
#
# def test_deal_cards_solution_suspect_category(game_two_players):
#     assert game_two_players.solution["Suspect"].category == "Suspect"
#
# def test_deal_cards_solution_weapon_category(game_two_players):
#     assert game_two_players.solution["Weapon"].category == "Weapon"
#
# def test_deal_cards_solution_room_category(game_two_players):
#     assert game_two_players.solution["Room"].category == "Room"
#
# def test_deal_cards_all_cards_accounted_for(game_two_players):
#     total = len(_SUSPECTS) + len(_WEAPONS) + len(_ROOMS)
#     dealt = sum(len(p.hand) for p in game_two_players.players)
#     face_up = len(game_two_players.face_up_cards)
#     solution = len(game_two_players.solution)
#     assert dealt + face_up + solution == total
#
# def test_deal_cards_no_duplicates(game_two_players):
#     all_names = []
#     for p in game_two_players.players:
#         all_names.extend([c.name for c in p.hand])
#     all_names.extend([c.name for c in game_two_players.face_up_cards])
#     all_names.extend([c.name for c in game_two_players.solution.values()])
#     assert len(all_names) == len(set(all_names))
#
# def test_deal_cards_solution_not_in_any_hand(game_two_players):
#     solution_names = {c.name for c in game_two_players.solution.values()}
#     for p in game_two_players.players:
#         hand_names = {c.name for c in p.hand}
#         assert solution_names.isdisjoint(hand_names)
#
# def test_deal_cards_three_players_all_accounted_for(game_three_players):
#     total = len(_SUSPECTS) + len(_WEAPONS) + len(_ROOMS)
#     dealt = sum(len(p.hand) for p in game_three_players.players)
#     face_up = len(game_three_players.face_up_cards)
#     solution = len(game_three_players.solution)
#     assert dealt + face_up + solution == total
#
# def test_advance_turn_increments_index(game_two_players):
#     game_two_players._advance_turn()
#     assert game_two_players._turn_index == 1
#
# def test_advance_turn_wraps_around(game_two_players):
#     game_two_players._turn_index = 1
#     game_two_players._advance_turn()
#     assert game_two_players._turn_index == 0
#
# def test_advance_turn_three_players(game_three_players):
#     game_three_players._advance_turn()
#     game_three_players._advance_turn()
#     game_three_players._advance_turn()
#     assert game_three_players._turn_index == 0
#
# def test_find_player_by_character_returns_correct_player(game_two_players):
#     result = game_two_players._find_player_by_character("Miss Scarlett")
#     assert result is not None
#     assert result.name == "Alice"
#
# def test_find_player_by_character_second_player(game_two_players):
#     result = game_two_players._find_player_by_character("Prof Plum")
#     assert result.name == "Bob"
#
# def test_find_player_by_character_not_found_returns_none(game_two_players):
#     result = game_two_players._find_player_by_character("Rev Green")
#     assert result is None
#
# def test_handle_accusation_correct_returns_correct_accusation(game_two_players):
#     player = game_two_players.players[0]
#     sol = game_two_players.solution
#     suspect_names = [c.name for c in _SUSPECTS]
#     weapon_names  = [c.name for c in _WEAPONS]
#     room_names    = [c.name for c in _ROOMS]
#     s_idx = str(suspect_names.index(sol["Suspect"].name) + 1)
#     w_idx = str(weapon_names.index(sol["Weapon"].name) + 1)
#     r_idx = str(room_names.index(sol["Room"].name) + 1)
#     with patch("builtins.input", side_effect=[s_idx, w_idx, r_idx]):
#         result = game_two_players.handle_accusation(player)
#     assert result == EndCondition.CORRECT_ACCUSATION
#
# def test_handle_accusation_wrong_eliminates_player(game_two_players):
#     player = game_two_players.players[0]
#     sol = game_two_players.solution
#     suspect_names = [c.name for c in _SUSPECTS]
#     weapon_names  = [c.name for c in _WEAPONS]
#     room_names    = [c.name for c in _ROOMS]
#     wrong_suspect = next(c for c in _SUSPECTS if c.name != sol["Suspect"].name)
#     wrong_weapon  = next(c for c in _WEAPONS  if c.name != sol["Weapon"].name)
#     wrong_room    = next(c for c in _ROOMS    if c.name != sol["Room"].name)
#     s_idx = str(suspect_names.index(wrong_suspect.name) + 1)
#     w_idx = str(weapon_names.index(wrong_weapon.name) + 1)
#     r_idx = str(room_names.index(wrong_room.name) + 1)
#     with patch("builtins.input", side_effect=[s_idx, w_idx, r_idx]):
#         game_two_players.handle_accusation(player)
#     assert player.is_active is False
#
# def test_handle_accusation_wrong_returns_wrong_accusation(game_two_players):
#     player = game_two_players.players[0]
#     sol = game_two_players.solution
#     suspect_names = [c.name for c in _SUSPECTS]
#     weapon_names  = [c.name for c in _WEAPONS]
#     room_names    = [c.name for c in _ROOMS]
#     wrong_suspect = next(c for c in _SUSPECTS if c.name != sol["Suspect"].name)
#     wrong_weapon  = next(c for c in _WEAPONS  if c.name != sol["Weapon"].name)
#     wrong_room    = next(c for c in _ROOMS    if c.name != sol["Room"].name)
#     s_idx = str(suspect_names.index(wrong_suspect.name) + 1)
#     w_idx = str(weapon_names.index(wrong_weapon.name) + 1)
#     r_idx = str(room_names.index(wrong_room.name) + 1)
#     with patch("builtins.input", side_effect=[s_idx, w_idx, r_idx]):
#         result = game_two_players.handle_accusation(player)
#     assert result == EndCondition.WRONG_ACCUSATION
#
# def test_handle_accusation_all_eliminated(game_two_players):
#     game_two_players.players[1].is_active = False
#     player = game_two_players.players[0]
#     sol = game_two_players.solution
#     suspect_names = [c.name for c in _SUSPECTS]
#     weapon_names  = [c.name for c in _WEAPONS]
#     room_names    = [c.name for c in _ROOMS]
#     wrong_suspect = next(c for c in _SUSPECTS if c.name != sol["Suspect"].name)
#     wrong_weapon  = next(c for c in _WEAPONS  if c.name != sol["Weapon"].name)
#     wrong_room    = next(c for c in _ROOMS    if c.name != sol["Room"].name)
#     s_idx = str(suspect_names.index(wrong_suspect.name) + 1)
#     w_idx = str(weapon_names.index(wrong_weapon.name) + 1)
#     r_idx = str(room_names.index(wrong_room.name) + 1)
#     with patch("builtins.input", side_effect=[s_idx, w_idx, r_idx]):
#         result = game_two_players.handle_accusation(player)
#     assert result == EndCondition.ALL_ELIMINATED
#
# Adaptations made to AI output:
#   - Methods relying on input() (setup, play_turn, handle_suggestion) not
#     directly tested as they require extensive mocking of full game flow;
#     testable helper methods targeted instead.
#   - handle_accusation tests find correct index for each solution card
#     dynamically using .index() so tests pass regardless of which cards
#     are randomly selected as the solution each run.
#   - Used side_effect=[...] not return_value for input mocking in
#     handle_accusation since three separate input() calls are made.
#   - ALL_ELIMINATED test manually sets second player inactive before
#     calling handle_accusation to simulate last active player accusing.
# =============================================================================
# 
# Prompt 2:
# "Write me docstrings for test_game.py
# [uploaded test_game.py]
# Return just the docstrings not full code.
# Write the docstrings in accordance with these instructions:
# * Write docstrings for all public modules, functions, classes,
#   and methods. Public methods including __init__ should also
#   have docstrings.
# * Always use triple double quotes around docstrings.
# * One-line docstrings should fit on a single line, with closing
#   quotes on the same line as the opening quotes, and no blank
#   line before or after.
# * Write docstrings as a command, not a description.
# * Multi-line docstrings consist of a summary line, followed by
#   a blank line, followed by a more elaborate description.
# * For functions and methods, document arguments, return values,
#   side effects, exceptions raised, and restrictions.
# * For classes, summarise behaviour and list public methods and
#   instance variables.
# * Unless the entire docstring fits on one line, place the
#   closing quotes on a line by themselves.
# * Insert a blank line after all docstrings that document a class.
# * Docstrings and comments should be wrapped at 72 characters."
#
# Output 2:
#
# Module docstring: already accurate, no change needed.
#
# game fixture docstring:
# """Return a bare Game instance with no players."""
#
# game_two_players fixture docstring:
# """Return a Game with two players set up and cards dealt."""
#
# game_three_players fixture docstring:
# """Return a Game with three players set up and cards dealt."""
#
# test_deal_cards_all_cards_accounted_for docstring:
# """Verify solution + all hands + face-up equals total deck."""
#
# test_deal_cards_solution_not_in_any_hand docstring:
# """Verify no solution card appears in any player's hand."""
#
# test_handle_accusation_all_eliminated docstring:
# """Verify ALL_ELIMINATED returned when last active player
# accuses wrongly.
#
# Manually set the second player inactive before calling
# handle_accusation to simulate the last remaining active
# player making a wrong accusation.
# """
#
# All other test functions: no docstrings added. Test function
# names are self-describing, which is standard pytest convention.
# Adding one-liners to every test function would be redundant
# noise and is not expected practice.
#
# Adaptations made to AI output:
#   - Agreed with AI recommendation not to docstring every test
#     function, consistent with pytest best practice
#   - Verified fixture descriptions match actual setup logic
#     in each fixture before applying
# =============================================================================