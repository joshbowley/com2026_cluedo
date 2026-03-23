"""
## Game 
Attributes: 
- players
- board
- cards
- solution
- face_up_cards
- current_turn
- winner
Methods: 
- setup
- deal_cards
- run
- play_turn
- handle_suggestion
- handle_accusation
- print_summary

"""       
        
class Game():
    def __init__(self):
        pass

    def setup():
        # Initial game setup. 

        # ask for number of players, 
        # their names 
        # and characters. 

        # every player starts in their specified starting position.

        # every player starts with empty hand and notesheet.

        # each player rolls dice, highest goes first.

        pass

    def deal_cards():
        # three categories of cards: suspects, weapons, rooms.
        # solution is one card from each category.
        # remaining cards are dealt to players.
        # leftover cards are face up on the side of the board.

        pass


    def run():
        # start first player's turn, then move to next player in turn order until end condition met

        pass
    
    def play_turn():
        # check if player is eliminated
        ## if eliminated, skip turn and move to next player
        ## if not eliminated, continue

        # check if player has been moved into another room by another player since their last turn. 
        ## if so: allow them to choose either: stay and suggest, or roll and move as normal.
        ### if stay and suggest: resolve suggestion by checking players in order to the left. then advance turn. 
        ### if roll and move: continue. 

        # roll dice

        # show valid moves based on dice roll and current position.

        # move player token to new position.
        ## if in room: allow suggestion. Resolves suggestion by checking players in order to the left. then advance turn.
        ## if in corridor: advance turn.
        ## if in central room: optionally accuse. 
        ### if accusation correct: end game and declare winner.
        ### if accusation wrong: eliminate player. Check if all players eliminated. 
        #### if all players eliminated: end game with no winner.
        #### if not all players eliminated: advance turn.

        pass
    
    def handle_suggestion():
        # suggestion logic

        pass
    
    def handle_accusation():
        # accusation logic

        pass
    
    def print_summary():
        # print summary with 'p' key input

        pass
