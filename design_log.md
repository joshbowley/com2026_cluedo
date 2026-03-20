# Design Log for COM2016 Cluedo

### 19.03.2026

## Common elements of a computer game: [1]

- Initial setup: get the game ready to play. This might mean setting the pieces on a chess board, dealing out cards, or rolling dice to see who goes first.

- Gameplay: flow of gameplay is controlled by a game loop, which keeps the game moving and doesn't end until the game is over. The game loop ensures that the following happens: 
    - The user input is gathered and processed
    - The game stage is updated based on readtions to the user input. This may include checking for end-of-game conditions. 
    - Any required output changes are made to reflect the new game state. 
    - Game loop repeats

- Game ending: how the game ends depends on the game itself. Whether capturing the enemy king in checkmate, achieving a certain score in a card game, or having your piece cross the line in a board game, certain conditions determine the end of the game and the winner. 

All games have a game loop. For example, in a chess game, you first set the pieces on the board and declare the current player. Then the game loop begins: 

- Current player moves a piece, updating the game state.
- Checkmate conditions is checked to determine if the game is over. 
- The current player is updated and the loop starts again. 

Real-world games blur the lines between the individual elements of a game. For example, moves in chess update both the game state and the game output. Despite this, the key elements of the game are always present. With them in mind, you can begin writing your own game. 


## Description of the Cluedo Game: [1] [2] [3]

Note for further consideration: 

If in room, and other player tokens are on exits of room, is player in room able to exit? If not, are they able to make a suggestion or do they forfit their turn until other players move? How to track if player has just entered a room versus was in same room from previous turn? 

- Game setup: 
    - Game asks for number of players.
    - Requests names for each user.
    - Player tokens are put in starting positions. 
    - WHO, WHAT, and WHERE cards are seperated and shuffled.
    - Top card from each pile is put into the Yellow Murder Envelope.
    - Remaining cards are combined and shuffled.
    - Cards are dealt evenly among other players. If cards don't divide exactly between players, leftover cards are put face up at the side of the board.
    - Each player crosses off the cards they have been dealt and any leftover cards that are faceup on the table from their CLUE sheet. 
    - **(Red bonus cards are shuffled and placed at the side of the board for bonus moves during play. Not included in original CLUE gameplay).
    - Every player rolls the dice. Highest roller goes first. 

- Player's Turn: 
    - Roll the dice. 
    - Check valid moves (if moved to a room by other player last turn, staying where you are and asking a question counts as a valid move). 
    - Move character token to a valid space. 
    - IF (in room): 
        - Stop and ask a CLUE question about one suspect, one weapon, and room character token is in. 
        - Bring the suspect's character token and weapon token being asked about into the room. 
        - The player on your left must be the first to try to answer your question. If they have any of the cards you asked about they must show one of them. Never show more than one card. 
        - If they don't have any of the cards asked about, they say "I cannot answer"
        - Question is passed left to the next player. 
        - Repeat until either one card is shown or have cycled through every player. 
        - If shown card, mark it off CLUE sheet. 
        - End turn. 
    - IF (in corridor):
        - End turn.
    - IF (center of board): 
        - Select which WHO, WHAT, WHERE cards for accusation.  
        - Read accusation aloud: "I accuse WHO, with the WHAT in the WHERE".
        - Check cards in Envelope. 
        - IF (accusation correct): 
            - WIN
        - IF (accusation incorrect):
            - Player is 'removed' (return cards to the Envelope. Keep cards hidden and keep answering other player's questions. Do not ask any further questions or make any further accusations).
            - Game loop continues.    
    - **IF(red bonus card):
        - Pick up top red bonus card. 
        - Follow instructions on card.
        - Place card in discard pile. 
        - End turn. 
    - Move to next player's turn. 


### 20.03.2026

## Key objects/parts of the game:

- Players.
- WHO, WHAT, WHERE cards. 
- Dice.
- **(Red bonus cards).
- Board. 

## Thoughts about inheritance/OOP considerations:

Player class -> player object defined in setup

Card class -> seperate WHO, WHAT and WHERE classes **(red bonus card class) -> specific cards

Location class -> room class, corridor and center of board instances -> specific rooms

Dice class




# Bibliography

[1] python-hangman: [realpython.com/python-hangman/](https://realpython.com/python-hangman/) (Accessed 19.03.2026)

[2] CLUE The Classic Mystery Game: [hasbro.com/common/documents/dad2885d1c](https://www.hasbro.com/common/documents/dad2885d1c4311ddbd0b0800200c9a66/2BFAEC9E5056900B102C3859E9AC6332.pdf) (Accessed 19.03.2026)

[3] How to Play Cluedo: [asmodee.co.uk/blogs/news/cluedo-rules](https://www.asmodee.co.uk/blogs/news/cluedo-rules) (Accessed 19.03.2026)