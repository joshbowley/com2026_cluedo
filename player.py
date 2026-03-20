"""
## Player 
Attributes:
- names 
- character
- position
- hand 
- notes
- is_active
- can_suggest_without_moving
Methods:
- move
- show_matching_card
- record_seen_card
- make_suggestion
- make_accusation
"""

class Player():
    def __init__(self, 
                 name, character, position, hand, notes, 
                 is_active, can_suggest_without_moving):
        
        self.name = name # player's entered name
        self.character = character # the Cluedo suspect/token they're playing as
        self.position = position # wherer they are now
        self.hand = hand # cards dealt to them
        self.notes=  notes # their CLUE sheet
        self.is_active = is_active # whether they are still in the game after a false accusation
        self.can_suggest_without_moving = can_suggest_without_moving # when another player moves token into a room
        

    def record_seen_card(self):
        # Add seen card to list. 
    
    def show_matching_card(self):
        # Show matching card for suggestions
    
    def move_to(new_position)
        # Update position parameter.