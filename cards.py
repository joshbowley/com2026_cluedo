"""Card class definition for Cluedo game."""

from dataclasses import dataclass


@dataclass
class Card:
    """Represent a single Cluedo card with a name and category.

    Used as a data container for suspect, weapon, and room cards.
    Implemented as a dataclass so equality and repr are generated
    automatically.

    Attributes:
        name: The card name e.g. 'Miss Scarlett'.
        category: The card category e.g. 'Suspect', 'Weapon',
            or 'Room'.

    Public methods:
        __str__: Return a human-readable string representation.
    """

    name: str

    category: str

    def __str__(self) -> str:
        """Return a formatted string showing category and name."""
        return "Category: " + self.category + ", Name: " + self.name


# =============================================================================
# AI PROMPTS AND OUTPUTS (required per coursework specification)
# =============================================================================
# Tool: Claude (claude.ai, claude-sonnet-4-6)
#
# Prompt:
# "Write me docstrings for cards.py
# [uploaded cards.py]
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
# """Card class definition for Cluedo game."""
#
# Card class docstring:
# """Represent a single Cluedo card with a name and category.
#
# Used as a data container for suspect, weapon, and room cards.
# Implemented as a dataclass so equality and repr are generated
# automatically.
#
# Attributes:
#     name: The card name e.g. 'Miss Scarlett'.
#     category: The card category e.g. 'Suspect', 'Weapon',
#         or 'Room'.
#
# Public methods:
#     __str__: Return a human-readable string representation.
# """
#
# __str__ docstring:
# """Return a formatted string showing category and name."""
#
# Adaptations made to AI output:
#   - Verified category values match actual usage in game.py
#     ('Suspect', 'Weapon', 'Room' with capitals) before applying
# =============================================================================