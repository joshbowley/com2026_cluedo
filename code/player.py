"""Player class definition for Cluedo game."""

class Player:
    """Represent a Cluedo player with state and game actions.

    Track a player's name, character token, board position, card
    hand, notesheet, active status, and whether they may suggest
    without moving.

    Attributes:
        name: The player's entered name.
        character: The Cluedo suspect token they are playing as.
        position: Current board position, either a corridor
            coordinate tuple, a room name string, or None before
            setup.
        hand: List of Card objects dealt to the player.
        notes: Dict mapping card name to who showed it, used as
            the player's CLUE sheet.
        is_active: False after the player makes a wrong accusation.
        can_suggest_without_moving: True if this player's token
            was moved into a room by another player's suggestion,
            allowing them to suggest without rolling first.

    Public methods:
        record_seen_card: Record a card and who showed it.
        show_matching_card: Return a matching card from hand.
        move_to: Move the player token to a new position.
    """

    def __init__(self, name: str, character: str):
        """Initialise a Player with a name and character.

        Args:
            name: The player's entered name.
            character: The Cluedo suspect token they will play as.
        """

        self.name: str = name

        self.character: str = character

        self.position: tuple | str | None = None

        self.hand: list = []

        self.notes: dict = {}

        self.is_active: bool = True

        self.can_suggest_without_moving: bool = False


    def record_seen_card(self, card: str, shown_by: str) -> None:
        """Record a card that has been seen and who showed it.

        Do nothing if the card is already recorded, so that earlier
        entries such as own hand are not overwritten by later ones.

        Args:
            card: The name of the card that was shown.
            shown_by: Description of the source, e.g. a player's
                name, 'own hand', or 'face-up'.
        """

        if card not in self.notes:
            self.notes[card] = shown_by   

    def show_matching_card(self, cards: list) -> str | None:
        """Return a card name from hand that matches the suggestion.

        If no cards match, return None. If exactly one card matches,
        return it automatically. If multiple cards match, prompt this
        player to choose which one to reveal.

        Args:
            cards: List of up to three card names from the current
                suggestion (suspect, weapon, room).

        Returns:
            The name of the card to show, or None if no match.
        """

        matches = [card for card in self.hand if card.name in cards]

        if not matches: 
            return None
        elif len(matches) == 1: 
            return matches[0].name
        
        print(
            f"\n{self.name}, you have multiple matching "
            f"cards. Which will you show?"
        )
        for i, card in enumerate(matches, 1):
            print(f"  {i}. {card.name}")
        while True:
            try:
                idx = int(input("Enter number: ").strip())
                if 1 <= idx <= len(matches):
                    return matches[idx - 1].name
                print(f"Please enter a number between 1 and {len(matches)}.")
            except ValueError:
                print("Invalid input: please enter a number.")
        
    
    def move_to(self, new_position: tuple | str | None) -> None:
        """Move the player token to new_position.

        Args:
            new_position: A corridor coordinate tuple, a room name
                string, or None to remove the player from the board.
        """

        self.position = new_position


# =============================================================================
# AI PROMPTS AND OUTPUTS (required per coursework specification)
# =============================================================================
# Tool: Claude (claude.ai, claude-sonnet-4-6)
#
# Prompt:
# "Write me docstrings for player.py
# [uploaded player.py]
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
# Output:
#
# Module docstring:
# """Player class definition for Cluedo game."""
#
# Player class docstring:
# """Represent a Cluedo player with state and game actions.
#
# Track a player's name, character token, board position, card
# hand, notesheet, active status, and whether they may suggest
# without moving.
#
# Attributes:
#     name: The player's entered name.
#     character: The Cluedo suspect token they are playing as.
#     position: Current board position, either a corridor
#         coordinate tuple, a room name string, or None before
#         setup.
#     hand: List of Card objects dealt to the player.
#     notes: Dict mapping card name to who showed it, used as
#         the player's CLUE sheet.
#     is_active: False after the player makes a wrong accusation.
#     can_suggest_without_moving: True if this player's token
#         was moved into a room by another player's suggestion,
#         allowing them to suggest without rolling first.
#
# Public methods:
#     record_seen_card: Record a card and who showed it.
#     show_matching_card: Return a matching card from hand.
#     move_to: Move the player token to a new position.
# """
#
# __init__ docstring:
# """Initialise a Player with a name and character.
#
# Args:
#     name: The player's entered name.
#     character: The Cluedo suspect token they will play as.
# """
#
# record_seen_card docstring:
# """Record a card that has been seen and who showed it.
#
# Do nothing if the card is already recorded, so that earlier
# entries such as own hand are not overwritten by later ones.
#
# Args:
#     card: The name of the card that was shown.
#     shown_by: Description of the source, e.g. a player's
#         name, 'own hand', or 'face-up'.
# """
#
# show_matching_card docstring:
# """Return a card name from hand that matches the suggestion.
#
# If no cards match, return None. If exactly one card matches,
# return it automatically. If multiple cards match, prompt this
# player to choose which one to reveal.
#
# Args:
#     cards: List of up to three card names from the current
#         suggestion (suspect, weapon, room).
#
# Returns:
#     The name of the card to show, or None if no match.
# """
#
# move_to docstring:
# """Move the player token to new_position.
#
# Args:
#     new_position: A corridor coordinate tuple, a room name
#         string, or None to remove the player from the board.
# """
#
# Adaptations made to AI output:
#   - Verified can_suggest_without_moving description matches
#     actual behaviour in play_turn() before applying
#   - Confirmed notes dict maps card name to shown_by string
#     by checking record_seen_card() implementation
# =============================================================================