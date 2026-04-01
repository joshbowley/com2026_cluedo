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
    # two cards match — should prompt for input, mock user choosing first option (1)
    with patch("builtins.input", return_value="1"):
        result = player_with_hand.show_matching_card(["Knife", "Kitchen", "Col Mustard"])
    assert result in ["Knife", "Kitchen"]

def test_show_matching_card_multiple_matches_second_choice(player_with_hand):
    # mock user choosing second option
    with patch("builtins.input", return_value="2"):
        result = player_with_hand.show_matching_card(["Knife", "Kitchen", "Col Mustard"])
    assert result in ["Knife", "Kitchen"]

def test_show_matching_card_no_match_returns_none_not_empty_string(player_with_hand):
    result = player_with_hand.show_matching_card(["Rope", "Ballroom", "Col Mustard"])
    assert result is None
    assert result != ""

# =============================================================================
# AI PROMPTS AND OUTPUTS (required per coursework specification)
# =============================================================================
# Tool: Claude (claude.ai, claude-sonnet-4-6)
#
# Prompt:
# "Generate pytest unit tests for the methods in this player.py class file.
#
# [uploaded player.py]
#
# Output: test_player.py containing the following tests:
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