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

        if card not in self.notes:
            self.notes[card] = shown_by        
    
    def show_matching_card(self, cards: list) -> str | None:
        """Show a card from the player's hand that matches one of the suggested cards, if any."""

        matches = [card for card in self.hand if card.name in cards]

        if not matches: 
            return None
        elif len(matches) == 1: 
            return matches[0].name
        
        print(f"\n{self.name}, you have multiple matching cards. Which will you show?")
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
        """Move player token to new position."""

        self.position = new_position

