"""Game Class for Cluedo game logic and flow control."""   

import random
from board import Board, _STARTING_POSITIONS
from cards import Card
from dice import roll
from display import render
from endcondition import EndCondition
from player import Player    

_SUSPECTS = [
    Card("Miss Scarlett", "Suspect"),
    Card("Prof Plum",     "Suspect"),
    Card("Mrs Peacock",   "Suspect"),
    Card("Rev Green",     "Suspect"),
    Card("Mrs White",     "Suspect"),
    Card("Col Mustard",   "Suspect"),
]
 
_WEAPONS = [
    Card("Candlestick", "Weapon"),
    Card("Knife",       "Weapon"),
    Card("Lead Pipe",   "Weapon"),
    Card("Revolver",    "Weapon"),
    Card("Rope",        "Weapon"),
    Card("Wrench",      "Weapon"),
]
 
_ROOMS = [
    Card("Kitchen",      "Room"),
    Card("Ballroom",     "Room"),
    Card("Conservatory", "Room"),
    Card("Billiard Room","Room"),
    Card("Library",      "Room"),
    Card("Study",        "Room"),
    Card("Hall",         "Room"),
    Card("Lounge",       "Room"),
    Card("Dining Room",  "Room"),
]
 
_CHARACTERS = [card.name for card in _SUSPECTS]
        
class Game():
    """Game with setup, turn management, suggestion and accusation handling, 
    and end condition checking for Cluedo game.

    Attributes:
        - 
    
    
    """

    def __init__(self):
        self.board = Board()
        self.players: list[Player] = []
        self.solution: dict[str, Card] = {}
        self.face_up_cards: list[Card] = []
        self.current_positions: dict[str, tuple | str] = {}
        self._turn_index: int = 0
        self._current_player: Player | None = None

    def setup(self):
        # Initial game setup. 
        print("Welcome to Cluedo!")

        # ask for number of players,    

        while True: 
            try:
                count = int(input("How many players? (2 to 6): \n").strip())
                if 2 <= count <= 6:
                    break
                print("  Please enter a number between 2 and 6. \n")
            except ValueError:
                print("  Invalid input: please enter a number. \n")

        self._AVAILABLE_CHARACTERS = _CHARACTERS.copy()

        for i in range(count): 
            print(f"\nPlayer {i+1}: \n")

            while True:
                name = input("Enter your name: ").strip()
                if name:
                    break
                print("Name can't be empty.")
 
            # Character choice
            print("Available characters:")
            for idx, char in enumerate(self._AVAILABLE_CHARACTERS, 1):
                print(f"{idx}. {char}")
 
            while True:
                try:
                    choice = int(input("  Choose a character (enter number): ").strip())
                    if 1 <= choice <= len(self._AVAILABLE_CHARACTERS):
                        character = self._AVAILABLE_CHARACTERS.pop(choice - 1)
                        break
                    print(f"Please enter a number between 1 and {len(self._AVAILABLE_CHARACTERS)}.")
                except ValueError:
                    print("Invalid input: please enter a number.")
 
            player = Player(name, character)
            player.move_to(_STARTING_POSITIONS[character])
            self.current_positions[character] = _STARTING_POSITIONS[character]
            self.players.append(player)
            print(f"{name} will play as {character}.")

        self.deal_cards()

        # Show face-up cards
        if self.face_up_cards:
            print("Face-up cards (everyone can see these)")
            for card in self.face_up_cards:
                print(f"  {card.name} ({card.category})")
            # Every player notes face-up cards automatically
            for player in self.players:
                for card in self.face_up_cards:
                    player.record_seen_card(card.name, "face-up")
 
        # Each player notes their own hand
        for player in self.players:
            for card in player.hand:
                player.record_seen_card(card.name, "own hand")
 
        #  Determine turn order by dice roll
        print("\nRolling for turn order (highest goes first)")
        rolls: list[tuple[int, Player]] = []
        for player in self.players:
            input(f"Press Enter for {player.name} ({player.character}) to roll.")
            roll_1 = roll()
            roll_2 = roll()
            total = roll_1 + roll_2
            print(f"  {player.name} rolled {roll_1} and {roll_2}, for a total of {total}.")
            rolls.append((total, player))
 
        # Sort descending; stable sort keeps original order on ties
        rolls.sort(key=lambda x: x[0], reverse=True)
        self.players = [p for _, p in rolls]
 
        print("\nTurn order")
        for i, player in enumerate(self.players, 1):
            print(f"{i}. {player.name} ({player.character})")
               

    def deal_cards(self):
        """Separate cards into categories, seal one of each in the envelope,
        shuffle the rest, deal evenly to players, and set aside any leftovers.
        """
        # Shuffle each category independently then pick solution cards
        suspects = _SUSPECTS.copy()
        weapons  = _WEAPONS.copy()
        rooms    = _ROOMS.copy()
        random.shuffle(suspects)
        random.shuffle(weapons)
        random.shuffle(rooms)
 
        self.solution = {
            "Suspect": suspects.pop(),
            "Weapon":  weapons.pop(),
            "Room":    rooms.pop(),
        }
 
        print("\nThe murder envelope has been sealed. \n")
 
        # Combine remaining cards and shuffle
        deck = suspects + weapons + rooms
        random.shuffle(deck)
 
        # Deal round-robin
        num_players = len(self.players)
        for i, card in enumerate(deck):
            self.players[i % num_players].hand.append(card)
 
        # Cards that don't divide evenly become face-up
        remainder_start = (len(deck) // num_players) * num_players
        self.face_up_cards = deck[remainder_start:]
 
        # Print hand sizes
        for player in self.players:
            print(f"{player.name} dealt {len(player.hand)} card(s).")


    def run(self):
        """Start the game loop, cycling through active players until an
        EndCondition is reached.
        """  

        print("The game begins!")
 
        render(self.current_positions)
 
        while True:
            player = self.players[self._turn_index]
 
            if not player.is_active:
                # Eliminated players still answer suggestions but skip their turn
                self._advance_turn()
                continue
 
            result = self.play_turn(player)
 
            if result in (EndCondition.CORRECT_ACCUSATION, EndCondition.ALL_ELIMINATED):
                print(f"Suspect : {self.solution['Suspect'].name}")
                print(f"Weapon  : {self.solution['Weapon'].name}")
                print(f"Room    : {self.solution['Room'].name}")
                if result == EndCondition.CORRECT_ACCUSATION:
                    print(f"That is correct! {player.name} wins!")

                else:
                    print("\nAll players have been eliminated. No winner.")
                break
            else: 
                self._advance_turn()
    
    def play_turn(self, player: Player) -> EndCondition | None:
        """Execute one full turn for *player*.
 
        Handles the special case where the player was moved into a room by
        another player's suggestion (can_suggest_without_moving), rolling and
        moving, in-room suggestions, corridor end-of-turn, and Central Room
        accusations.
 
        Args:
            player: The Player whose turn it is.
 
        Returns:
            An EndCondition if the game should end, otherwise None.
        """
        self._current_player = player 

        print(f"{player.name}'s turn ({player.character})")
        print(f"Position: {player.position}")
        print("(Type 'p' at any move/choice prompt to see game summary.)\n")
 
        #  Special case: moved into room by another player 
        if player.can_suggest_without_moving:
            room = player.position  # already a room string
            print(f"You were moved into {room} by another player's suggestion.")
            choice = self._prompt_choice(
                "Would you like to:\n"
                "   1. Stay and make a suggestion\n"
                "   2. Roll the dice and move normally\n"
                "Enter choice (1 or 2): ",
                valid=["1", "2"],
            )
            player.can_suggest_without_moving = False
 
            if choice == "1":
                self.handle_suggestion(player, room)
                return None
 
        #  Roll and move 
        input("Press Enter to roll the dice... ")
        die_1, die_2 = roll(), roll()
        total = die_1 + die_2
        print(f"Rolled {die_1} + {die_2} = {total}")
 
        # Build blocked list: corridor positions of other active players
        blocked = [
            p.position
            for p in self.players
            if p is not player and isinstance(p.position, tuple)
        ]
 
        valid_moves = self.board.get_valid_moves(player.position, total, blocked)
 
        if not valid_moves:
            print("No valid moves available. Turn skipped.")
            return None
 
        # Display board with current positions
        render(self.current_positions)
 
        # Show valid moves to the player
        print("\nValid moves:")
        for idx, move in enumerate(valid_moves, 1):
            print(f"{idx}. {move}")
 
        # Prompt player to pick a destination
        while True:
            raw = input("Choose a destination (enter number): ").strip()
            if raw.lower() == "p":
                self.print_summary(self._current_player)
                continue
            try:
                idx = int(raw)
                if 1 <= idx <= len(valid_moves):
                    destination = valid_moves[idx - 1]
                    break
                print(f"Please enter a number between 1 and {len(valid_moves)}.")
            except ValueError:
                print("Invalid input: please enter a number.")
 
        # Move the player
        player.move_to(destination)
        self.current_positions[player.character] = destination
        render(self.current_positions)
 
        #  In a room 
        if self.board.is_room(destination):
            if destination == "Central Room":
                # Accusation (optional — player may decline)
                print(f"\nYou are in the Central Room.")
                choice = self._prompt_choice(
                    "Would you like to make an accusation? (y/n): ",
                    valid=["y", "n"],
                )
                if choice == "y":
                    return self.handle_accusation(player)
            else:
                print(f"\nYou entered {destination}.")
                self.handle_suggestion(player, destination)
 
        return None
    
    def handle_suggestion(self, player: Player, room: str) -> None:
        """Resolve a suggestion made by player in room."""
        print(f"\nSuggestion in {room}")

        suspect_names = [c.name for c in _SUSPECTS]
        print("Suspects:")
        for i, name in enumerate(suspect_names, 1):
            print(f"  {i}. {name}")
        suspect = self._prompt_from_list("Name a suspect: ", suspect_names)

        weapon_names = [c.name for c in _WEAPONS]
        print("Weapons:")
        for i, name in enumerate(weapon_names, 1):
            print(f"  {i}. {name}")
        weapon = self._prompt_from_list("Name a weapon: ", weapon_names)

        print(f'\n{player.name} suggests: "{suspect}, with the {weapon}, in the {room}."')

        # Move the named suspect token into this room
        moved = self._find_player_by_character(suspect)
        if moved and moved is not player:
            moved.move_to(room)
            moved.can_suggest_without_moving = True
            self.current_positions[suspect] = room
            print(f"{suspect}'s token has been moved to {room}.")

        # Check players left to right
        start_idx = self.players.index(player)
        card_shown = False

        for offset in range(1, len(self.players)):
            responder = self.players[(start_idx + offset) % len(self.players)]
            shown = responder.show_matching_card([suspect, weapon, room])
            if shown:
                print(f"\n{responder.name} shows {player.name} a card.")
                player.record_seen_card(shown, responder.name)
                card_shown = True
                break
            else:
                print(f"{responder.name}: \"I cannot answer.\"")

        if not card_shown:
            print("No player could disprove the suggestion.")
    
    def handle_accusation(self, player: Player) -> EndCondition:
        """Resolve a formal accusation from *player*.
 
        Prompts for three cards, checks against the solution, and returns
        the appropriate EndCondition.
 
        Args:
            player: The player making the accusation.
 
        Returns:
            CORRECT_ACCUSATION if the guess matches the solution,
            WRONG_ACCUSATION if not (also eliminates the player), or
            ALL_ELIMINATED if no active players remain after elimination.
        """
        print(f"\nAccusation")
        print(f"Choose carefully — a wrong accusation eliminates you!\n")
 
        suspect_names = [c.name for c in _SUSPECTS]
        weapon_names  = [c.name for c in _WEAPONS]
        room_names    = [c.name for c in _ROOMS]
 
        print("Suspects:")
        for i, name in enumerate(suspect_names, 1):
            print(f"{i}. {name}")
        suspect = self._prompt_from_list("Accuse which suspect? ", suspect_names)
 
        print("Weapons:")
        for i, name in enumerate(weapon_names, 1):
            print(f"{i}. {name}")
        weapon = self._prompt_from_list("With which weapon? ", weapon_names)
 
        print("Rooms:")
        for i, name in enumerate(room_names, 1):
            print(f"{i}. {name}")
        room = self._prompt_from_list("In which room? ", room_names)
 
        print(f'\n{player.name} accuses: "{suspect}, with the {weapon}, in the {room}."')
 
        correct = (
            suspect == self.solution["Suspect"].name
            and weapon  == self.solution["Weapon"].name
            and room    == self.solution["Room"].name
        )
 
        if correct:
            return EndCondition.CORRECT_ACCUSATION
 
        # Wrong accusation — eliminate player
        print(f"\nThe accusation is WRONG. {player.name} is eliminated.")
        print(f"{player.name} will no longer take turns but may still")
        print(f"show cards when other players make suggestions.")
        player.is_active = False
 
        active = [p for p in self.players if p.is_active]
        if not active:
            return EndCondition.ALL_ELIMINATED
 
        return EndCondition.WRONG_ACCUSATION
    
    def print_summary(self, current_player: Player | None = None) -> None:
        """Print a summary of the current game state.
 
        Shows the board, all player positions and statuses, and — if
        current_player is provided — that player's notesheet.
 
        Args:
            current_player: The player whose notesheet to display, or None
                            to skip the notesheet section.
        """
        print("\n" + "=" * 60)
        print("  GAME SUMMARY")
        print("=" * 60)
 
        render(self.current_positions)
 
        print("\n  --- Players ---")
        for p in self.players:
            status = "active" if p.is_active else "ELIMINATED"
            print(f"{p.name} ({p.character}) — {status} — at {p.position}")
 
        if self.face_up_cards:
            print("\nFace-up cards")
            for card in self.face_up_cards:
                print(f"{card.name} ({card.category})")
 
        if current_player:
            print(f"\n{current_player.name}'s notesheet")
            self._print_notesheet(current_player)
 
        print("=" * 60 + "\n")

    def _print_notesheet(self, player: Player) -> None:
        """Render a formatted notesheet for *player*.
 
        Shows every card name alongside its known status: own hand,
        shown by a named player, face-up, or unknown.
 
        Args:
            player: The player whose notes to display.
        """

        col_w = 20
 
        print(f"  {'Card':<{col_w}} Status")
        print(f"  {'-' * col_w} ------")
 
        for category_label, category_cards in [
            ("Suspects", _SUSPECTS),
            ("Weapons",  _WEAPONS),
            ("Rooms",    _ROOMS),
        ]:
            print(f"  {category_label}")
            for card in category_cards:
                note = player.notes.get(card.name, "?")
                print(f"    {card.name:<{col_w - 2}} {note}")

    
    def _advance_turn(self) -> None:
        """Move the turn index forward by one, wrapping around."""
        self._turn_index = (self._turn_index + 1) % len(self.players)
 
    def _prompt_choice(self, prompt: str, valid: list[str]) -> str:
        """Prompt the user until they enter one of the *valid* options.
 
        Typing 'p' at any prompt triggers print_summary instead of
        returning a value.
 
        Args:
            prompt: The string displayed to the user.
            valid: List of accepted response strings (case-insensitive).
 
        Returns:
            The valid response entered by the user.
        """
        while True:
            raw = input(prompt).strip().lower()
            if raw == "p":
                self.print_summary(self._current_player)
                continue
            if raw in valid:
                return raw
            print(f"  Please enter one of: {', '.join(valid)}")
 
    def _prompt_from_list(self, prompt: str, options: list[str]) -> str:
        """Prompt the user to pick from a numbered list of *options*.
 
        Args:
            prompt: The string displayed to the user.
            options: The list of string options to choose from.
 
        Returns:
            The chosen option string.
        """
        while True:
            raw = input(prompt).strip()
            if raw.lower() == "p":
                self.print_summary(self._current_player)
                continue
            try:
                idx = int(raw)
                if 1 <= idx <= len(options):
                    return options[idx - 1]
                print(f"Please enter a number between 1 and {len(options)}.")
            except ValueError:
                print("Invalid input — please enter a number.")
 
    def _find_player_by_character(self, character: str) -> Player | None:
        """Return the Player currently playing as *character*, or None.
 
        Args:
            character: The character name to search for.
 
        Returns:
            The matching Player, or None if not found.
        """
        for p in self.players:
            if p.character == character:
                return p
        return None

        # =============================================================================
# AI PROMPTS AND OUTPUTS (required per coursework specification)
# =============================================================================
# Tool: Claude (claude.ai, claude-sonnet-4-6)
#
# Prompt 1:
# "Here is the current state of my Cluedo project [uploaded files].
#  Implement run() in game.py following the
#  pseudocode already in the file comments."
#
# Output 1: Initial implementation of run().
# def run(self) -> None:
#       """Start the game loop, cycling through active players until an
#        EndCondition is reached.
#        """
#        print("\n" + "=" * 60)
#        print("  The game begins!")
#        print("=" * 60)
# 
#        render(self.current_positions)
# 
#        while True:
#            player = self.players[self._turn_index]
# 
#            if not player.is_active:
#                # Eliminated players still answer suggestions but skip their turn
#                self._advance_turn()
#                continue
# 
#            result = self.play_turn(player)
# 
#            if result == EndCondition.CORRECT_ACCUSATION:
#                print("\n" + "=" * 60)
#                print(f"  {player.name} wins! The solution was:")
#                print(f"    Suspect : {self.solution['suspect'].name}")
#                print(f"    Weapon  : {self.solution['weapon'].name}")
#                print(f"    Room    : {self.solution['room'].name}")
#                print("=" * 60)
#                break
# 
#            if result == EndCondition.ALL_ELIMINATED:
#                print("\n" + "=" * 60)
#                print("  All players have been eliminated. No winner.")
#                print(f"  The solution was:")
#                print(f"    Suspect : {self.solution['suspect'].name}")
#                print(f"    Weapon  : {self.solution['weapon'].name}")
#                print(f"    Room    : {self.solution['room'].name}")
#                print("=" * 60)
#                break
# 
#            self._advance_turn()
#
#
#
#
#
# Prompt 2:
#  Now implement play_turn() in game.py following this
#  pseudocode: 
#  1. Check if player is elimated from accusing, but still allowed to answer suggestions
#    - If eliminated, then advance turn. 
#    - If not eliminated, continue.  
#  2. Check if player has been moved into another room by other player's suggestion since their last turn. 
#    - If has been moved, allow them to choose to either: stay and suggest, or roll and move. 
#        - If stay and suggest, resolve suggestion by checking players in order to the left. Then advance turn. 
#        - If roll and move, continue.
#    - If haven't been moved, continue.
#  3. Roll dice. 
#  4. Show valid moves. 
#  5. Move player. 
#    - If in room, allow suggestion. Resolve suggestion by checking players in order to the left. Then advance turn. 
#    - If in corridor, advance turn. 
#    - If in center of board, optionally accuse.
#        - If accusation correct, end game and player wins. 
#        - If accusation incorrect, mark player as eliminated. Advance turn. "
#
# Output 2: Initial implementation of run().
# def play_turn(self, player: Player) -> EndCondition | None:
#        """Execute one full turn for *player*.
# 
#        Handles the special case where the player was moved into a room by
#        another player's suggestion (can_suggest_without_moving), rolling and
#        moving, in-room suggestions, corridor end-of-turn, and Central Room
#        accusations.
# 
#        Args:
#            player: The Player whose turn it is.
# 
#        Returns:
#            An EndCondition if the game should end, otherwise None.
#        """
#        print("\n" + "-" * 60)
#        print(f"  {player.name}'s turn ({player.character})")
#        print(f"  Position: {player.position}")
#        print("-" * 60)
#        print("  (Type 'p' at any move/choice prompt to see game summary.)\n")
# 
#        # ── Special case: moved into room by another player ────────────────────
#        if player.can_suggest_without_moving:
#            room = player.position  # already a room string
#            print(f"  You were moved into {room} by another player's suggestion.")
#            choice = self._prompt_choice(
#                "  Would you like to:\n"
#                "    1. Stay and make a suggestion\n"
#                "    2. Roll the dice and move normally\n"
#                "  Enter choice (1 or 2): ",
#                valid=["1", "2"],
#            )
#            player.can_suggest_without_moving = False
# 
#            if choice == "1":
#               self.handle_suggestion(player, room)
#               return None
#
#        # ── Roll and move ──────────────────────────────────────────────────────
#        input("  Press Enter to roll the dice... ")
#        steps = roll() + roll()
#        print(f"  Rolled {steps}")
# 
#        # Build blocked list: corridor positions of other active players
#        blocked = [
#            p.position
#            for p in self.players
#            if p is not player and isinstance(p.position, tuple)
#        ]
# 
#        valid_moves = self.board.get_valid_moves(player.position, steps, blocked)
# 
#        if not valid_moves:
#            print("  No valid moves available. Turn skipped.")
#            return None
# 
#        # Display board with current positions
#        render(self.current_positions)
# 
#        # Show valid moves to the player
#        print("\n  Valid moves:")
#        for idx, move in enumerate(valid_moves, 1):
#            print(f"    {idx}. {move}")
# 
#        # Prompt player to pick a destination
#       while True:
#            raw = input("  Choose a destination (enter number): ").strip()
#            if raw.lower() == "p":
#                self.print_summary(player)
#                continue
#            try:
#                idx = int(raw)
#                if 1 <= idx <= len(valid_moves):
#                    destination = valid_moves[idx - 1]
#                    break
#                print(f"  Please enter a number between 1 and {len(valid_moves)}.")
#            except ValueError:
#                print("  Invalid input — please enter a number.")
# 
#        # Move the player
#        player.move_to(destination)
#        self.current_positions[player.character] = destination
#        render(self.current_positions)
# 
#        # ── In a room ──────────────────────────────────────────────────────────
#        if self.board.is_room(destination):
#            if destination == "Central Room":
#                # Accusation (optional — player may decline)
#                print(f"\n  You are in the Central Room.")
#                choice = self._prompt_choice(
#                    "  Would you like to make an accusation? (y/n): ",
#                    valid=["y", "n"],
#                )
#                if choice == "y":
#                    return self.handle_accusation(player)
#            else:
#                print(f"\n  You entered {destination}.")
#                self.handle_suggestion(player, destination)
# 
#        return None
#
#
#   def _prompt_choice(self, prompt: str, valid: list[str]) -> str:
#        """Prompt the user until they enter one of the *valid* options.
# 
#        Typing 'p' at any prompt triggers print_summary instead of
#        returning a value.
# 
#        Args:
#            prompt: The string displayed to the user.
#            valid: List of accepted response strings (case-insensitive).
# 
#        Returns:
#            The valid response entered by the user.
#        """
#        while True:
#            raw = input(prompt).strip().lower()
#            if raw == "p":
#                self.print_summary()
#                continue
#            if raw in valid:
#                return raw
#            print(f"  Please enter one of: {', '.join(valid)}")
#
# =============================================================================
