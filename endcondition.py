"""End condition enumeration for Cluedo game."""

from enum import Enum, auto

class EndCondition(Enum):
    """Enumerate the possible end conditions of a Cluedo game.

    Returned by handle_accusation() and used by run() to determine
    whether the game loop should terminate and how to report the
    result.

    Members:
        CORRECT_ACCUSATION: A player matched all three solution
            cards and wins the game.
        WRONG_ACCUSATION: A player guessed incorrectly and is
            eliminated from taking further turns.
        ALL_ELIMINATED: Every player has made a wrong accusation
            and the game ends with no winner.
    """
    CORRECT_ACCUSATION = auto()
    WRONG_ACCUSATION = auto() # player eliminated from game
    ALL_ELIMINATED = auto() # everyone made false accusations


# =============================================================================
# AI PROMPTS AND OUTPUTS (required per coursework specification)
# =============================================================================
# Tool: Claude (claude.ai, claude-sonnet-4-6)
#
# Prompt:
# "Write me docstrings for endcondition.py
# [uploaded endcondition.py]
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
# """End condition enumeration for Cluedo game."""
#
# EndCondition class docstring:
# """Enumerate the possible end conditions of a Cluedo game.
#
# Returned by handle_accusation() and used by run() to determine
# whether the game loop should terminate and how to report the
# result.
#
# Members:
#     CORRECT_ACCUSATION: A player matched all three solution
#         cards and wins the game.
#     WRONG_ACCUSATION: A player guessed incorrectly and is
#         eliminated from taking further turns.
#     ALL_ELIMINATED: Every player has made a wrong accusation
#         and the game ends with no winner.
# """
#
# Adaptations made to AI output:
#   - Verified member descriptions match actual game logic in
#     handle_accusation() and run() before applying
# =============================================================================