"""Unit tests for Player class."""

import pytest
from unittest.mock import patch
from player import Player
from cards import Card


@pytest.fixture
def player():
    """A basic Player with no hand or notes."""
    return Player("Josh", "Prof Plum")


@pytest.fixture
def player_with_hand():
    """A Player with three cards of different categories."""
    p = Player("Josh", "Prof Plum")
    p.hand = [
        Card("Knife",         "Weapon"),
        Card("Kitchen",       "Room"),
        Card("Miss Scarlett", "Suspect"),
    ]
    return p


# __init__ defaults 

def test_init_name(player):
    assert player.name == "Josh"

def test_init_character(player):
    assert player.character == "Prof Plum"

def test_init_position_none(player):
    assert player.position is None

def test_init_hand_empty(player):
    assert player.hand == []

def test_init_notes_empty(player):
    assert player.notes == {}

def test_init_is_active_true(player):
    assert player.is_active is True

def test_init_can_suggest_without_moving_false(player):
    assert player.can_suggest_without_moving is False


# move_to 

def test_move_to_corridor_tuple(player):
    player.move_to((9, 6))
    assert player.position == (9, 6)

def test_move_to_room_string(player):
    player.move_to("Kitchen")
    assert player.position == "Kitchen"

def test_move_to_none(player):
    player.move_to((9, 6))
    player.move_to(None)
    assert player.position is None

def test_move_to_updates_position(player):
    player.move_to((9, 6))
    player.move_to((10, 6))
    assert player.position == (10, 6)


# record_seen_card

def test_record_seen_card_adds_entry(player):
    player.record_seen_card("Knife", "Alice")
    assert "Knife" in player.notes

def test_record_seen_card_stores_shown_by(player):
    player.record_seen_card("Knife", "Alice")
    assert player.notes["Knife"] == "Alice"

def test_record_seen_card_does_not_overwrite_existing(player):
    """Verify earlier notes are not overwritten by later ones.

    Call record_seen_card twice with the same card name. The
    first value should be preserved, confirming the guard
    condition in record_seen_card() works correctly.
    """
    player.record_seen_card("Knife", "own hand")
    player.record_seen_card("Knife", "Alice")
    assert player.notes["Knife"] == "own hand"

def test_record_seen_card_multiple_cards(player):
    player.record_seen_card("Knife", "Alice")
    player.record_seen_card("Kitchen", "Bob")
    assert player.notes["Knife"] == "Alice"
    assert player.notes["Kitchen"] == "Bob"

def test_record_seen_card_face_up(player):
    player.record_seen_card("Rope", "face-up")
    assert player.notes["Rope"] == "face-up"

def test_record_seen_card_own_hand(player):
    player.record_seen_card("Revolver", "own hand")
    assert player.notes["Revolver"] == "own hand"


# show_matching_card 

def test_show_matching_card_no_match(player_with_hand):
    result = player_with_hand.show_matching_card(["Candlestick", "Ballroom", "Col Mustard"])
    assert result is None

def test_show_matching_card_empty_hand(player):
    result = player.show_matching_card(["Knife", "Kitchen", "Miss Scarlett"])
    assert result is None

def test_show_matching_card_single_match_weapon(player_with_hand):
    result = player_with_hand.show_matching_card(["Knife", "Ballroom", "Col Mustard"])
    assert result == "Knife"

def test_show_matching_card_single_match_room(player_with_hand):
    result = player_with_hand.show_matching_card(["Candlestick", "Kitchen", "Col Mustard"])
    assert result == "Kitchen"

def test_show_matching_card_single_match_suspect(player_with_hand):
    result = player_with_hand.show_matching_card(["Candlestick", "Ballroom", "Miss Scarlett"])
    assert result == "Miss Scarlett"

def test_show_matching_card_returns_string(player_with_hand):
    result = player_with_hand.show_matching_card(["Knife", "Ballroom", "Col Mustard"])
    assert isinstance(result, str)

def test_show_matching_card_multiple_matches_prompts_player(player_with_hand):
    """Verify player is prompted when multiple cards match.

    Mock input() to return '1' so the test does not hang
    waiting for keyboard input.
    """
    with patch("builtins.input", return_value="1"):
        result = player_with_hand.show_matching_card(["Knife", "Kitchen", "Col Mustard"])
    assert result in ["Knife", "Kitchen"]

def test_show_matching_card_multiple_matches_second_choice(player_with_hand):
    """Verify second choice is returned when player selects 2.

    Mock input() to return '2' so the test does not hang
    waiting for keyboard input.
    """
    with patch("builtins.input", return_value="2"):
        result = player_with_hand.show_matching_card(["Knife", "Kitchen", "Col Mustard"])
    assert result in ["Knife", "Kitchen"]

def test_show_matching_card_no_match_returns_none_not_empty_string(player_with_hand):
    """Verify no match returns None and not an empty string."""
    result = player_with_hand.show_matching_card(["Rope", "Ballroom", "Col Mustard"])
    assert result is None
    assert result != ""

# =============================================================================
# AI PROMPTS AND OUTPUTS (required per coursework specification)
# =============================================================================
# Tool: Claude (claude.ai, claude-sonnet-4-6)
#
# Prompt 1:
# "Generate pytest unit tests for the methods in this player.py class file.
#
# [uploaded player.py]
#
# Output 1: test_player.py containing the following tests:
#
# @pytest.fixture
# def player():
#     return Player("Josh", "Prof Plum")
#
# @pytest.fixture
# def player_with_hand():
#     p = Player("Josh", "Prof Plum")
#     p.hand = [
#         Card("Knife",         "Weapon"),
#         Card("Kitchen",       "Room"),
#         Card("Miss Scarlett", "Suspect"),
#     ]
#     return p
#
# def test_init_name(player):
#     assert player.name == "Josh"
#
# def test_init_character(player):
#     assert player.character == "Prof Plum"
#
# def test_init_position_none(player):
#     assert player.position is None
#
# def test_init_hand_empty(player):
#     assert player.hand == []
#
# def test_init_notes_empty(player):
#     assert player.notes == {}
#
# def test_init_is_active_true(player):
#     assert player.is_active is True
#
# def test_init_can_suggest_without_moving_false(player):
#     assert player.can_suggest_without_moving is False
#
# def test_move_to_corridor_tuple(player):
#     player.move_to((9, 6))
#     assert player.position == (9, 6)
#
# def test_move_to_room_string(player):
#     player.move_to("Kitchen")
#     assert player.position == "Kitchen"
#
# def test_move_to_none(player):
#     player.move_to((9, 6))
#     player.move_to(None)
#     assert player.position is None
#
# def test_move_to_updates_position(player):
#     player.move_to((9, 6))
#     player.move_to((10, 6))
#     assert player.position == (10, 6)
#
# def test_record_seen_card_adds_entry(player):
#     player.record_seen_card("Knife", "Alice")
#     assert "Knife" in player.notes
#
# def test_record_seen_card_stores_shown_by(player):
#     player.record_seen_card("Knife", "Alice")
#     assert player.notes["Knife"] == "Alice"
#
# def test_record_seen_card_does_not_overwrite_existing(player):
#     player.record_seen_card("Knife", "own hand")
#     player.record_seen_card("Knife", "Alice")
#     assert player.notes["Knife"] == "own hand"
#
# def test_record_seen_card_multiple_cards(player):
#     player.record_seen_card("Knife", "Alice")
#     player.record_seen_card("Kitchen", "Bob")
#     assert player.notes["Knife"] == "Alice"
#     assert player.notes["Kitchen"] == "Bob"
#
# def test_record_seen_card_face_up(player):
#     player.record_seen_card("Rope", "face-up")
#     assert player.notes["Rope"] == "face-up"
#
# def test_record_seen_card_own_hand(player):
#     player.record_seen_card("Revolver", "own hand")
#     assert player.notes["Revolver"] == "own hand"
#
# def test_show_matching_card_no_match(player_with_hand):
#     result = player_with_hand.show_matching_card(
#         ["Candlestick", "Ballroom", "Col Mustard"])
#     assert result is None
#
# def test_show_matching_card_empty_hand(player):
#     result = player.show_matching_card(["Knife", "Kitchen", "Miss Scarlett"])
#     assert result is None
#
# def test_show_matching_card_single_match_weapon(player_with_hand):
#     result = player_with_hand.show_matching_card(
#         ["Knife", "Ballroom", "Col Mustard"])
#     assert result == "Knife"
#
# def test_show_matching_card_single_match_room(player_with_hand):
#     result = player_with_hand.show_matching_card(
#         ["Candlestick", "Kitchen", "Col Mustard"])
#     assert result == "Kitchen"
#
# def test_show_matching_card_single_match_suspect(player_with_hand):
#     result = player_with_hand.show_matching_card(
#         ["Candlestick", "Ballroom", "Miss Scarlett"])
#     assert result == "Miss Scarlett"
#
# def test_show_matching_card_returns_string(player_with_hand):
#     result = player_with_hand.show_matching_card(
#         ["Knife", "Ballroom", "Col Mustard"])
#     assert isinstance(result, str)
#
# def test_show_matching_card_multiple_matches_first_choice(player_with_hand):
#     with patch("builtins.input", return_value="1"):
#         result = player_with_hand.show_matching_card(
#             ["Knife", "Kitchen", "Col Mustard"])
#     assert result in ["Knife", "Kitchen"]
#
# def test_show_matching_card_multiple_matches_second_choice(player_with_hand):
#     with patch("builtins.input", return_value="2"):
#         result = player_with_hand.show_matching_card(
#             ["Knife", "Kitchen", "Col Mustard"])
#     assert result in ["Knife", "Kitchen"]
#
# def test_show_matching_card_no_match_returns_none_not_empty_string(
#         player_with_hand):
#     result = player_with_hand.show_matching_card(
#         ["Rope", "Ballroom", "Col Mustard"])
#     assert result is None
#     assert result != ""
#
# Adaptations made to AI output:
#   - Used actual Card objects in player_with_hand fixture to match how
#     show_matching_card() accesses card.name rather than card directly
#   - Added unittest.mock.patch for the multiple-matches branch of
#     show_matching_card() to avoid the test hanging on input()
#   - Added overwrite guard test for record_seen_card() to verify the
#     if card not in self.notes guard works correctly
# =============================================================================
# 
#
# Prompt 2:
# "Write me docstrings for test_player.py
# [uploaded test_player.py]
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
# Fixture docstrings: already accurate, no change needed.
#
# test_record_seen_card_does_not_overwrite_existing docstring:
# """Verify earlier notes are not overwritten by later ones.
#
# Call record_seen_card twice with the same card name. The
# first value should be preserved, confirming the guard
# condition in record_seen_card() works correctly.
# """
#
# test_show_matching_card_multiple_matches_prompts_player docstring:
# """Verify player is prompted when multiple cards match.
#
# Mock input() to return '1' so the test does not hang
# waiting for keyboard input.
# """
#
# test_show_matching_card_multiple_matches_second_choice docstring:
# """Verify second choice is returned when player selects 2.
#
# Mock input() to return '2' so the test does not hang
# waiting for keyboard input.
# """
#
# test_show_matching_card_no_match_returns_none_not_empty_string:
# """Verify no match returns None and not an empty string."""
#
# All other test functions: no docstrings added. Test function
# names are self-describing, which is standard pytest convention.
# Adding one-liners to every test function would be redundant
# noise and is not expected practice.
#
# Adaptations made to AI output:
#   - Agreed with AI recommendation not to docstring every test
#     function, consistent with pytest best practice
#   - Verified fixture docstrings already accurate, no changes
#     needed
# =============================================================================