"""Card Class definition for Cluedo game."""

from dataclasses import dataclass

@dataclass
class Card: 
    """A card with a name and a category."""

    name: str
    """The card name e.g. 'Scarlett'."""

    category: str
    """The card category e.g. 'suspect', 'weapon', or 'room'."""

    def __str__(self) -> str:
        return "Category: " + self.category + ", Name: " + self.name
