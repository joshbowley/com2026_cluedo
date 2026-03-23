"""Player Class definition for Cluedo game."""

class Player:
    """Player with name, character, position, hand of cards, notesheet, and active status.
    
    Attributes:
        name: The player's entered name.
        character: The Cluedo suspect/token they're playing as.
        position: Current position on the board, either a room name or corridor coordinate.
        hand: Cards dealt to the player.
        notes: The player's CLUE sheet tracking seen cards.
        is_active: Whether the player is still active after a false accusation.
        can_suggest_without_moving: True if moved into a room by another player's suggestion.
    """
    def __init__(self, name: str, character: str):
        
        self.name: str = name 

        self.character: str = character 

        self.position: tuple | str | None = None 

        self.hand: list = [] 

        self.notes: dict = {} 

        self.is_active: bool = True 

        self.can_suggest_without_moving: bool = False         
        

    def record_seen_card(self, card: str, shown_by: str) -> None:
        """Record a card that has been shown to the player, and who showed it."""

        pass

        
    
    def show_matching_card(self, cards: list) -> None:
        """Show a card from the player's hand that matches one of the suggested cards, if any."""

        pass

        
    
    def move_to(self, new_position: tuple | str | None) -> None:
        """Move player token to new position."""

        self.position = new_position

