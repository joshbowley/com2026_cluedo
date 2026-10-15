# Cluedo — Command-Line Implementation (Python)

A fully playable, turn-based implementation of the Cluedo board game for 2–6 players, run entirely in the terminal. Built as the major coursework for COM2016B, Programming with Python, at the University of Exeter.

## Highlights

- **Movement by breadth-first search** over a hand-encoded adjacency map of the 24×25 board, covering all nine rooms, corridors, doorways and secret passages.
- **Board stored as a 2D list** rather than a dictionary: the board is a fixed size, so a list of lists is faster and uses less memory (reasoning in the design log).
- **Composition over inheritance:** `Game` owns a `Board`, `Player`s and dice rather than extending them; dataclasses for simple value objects such as `Card`.
- **156 pytest tests** across board movement, player state and game behaviour.
- **Robust input handling:** invalid input is re-prompted, never crashes the game.
- **Sphinx documentation**, PEP 8 and PEP 257 compliant.
- **Live coloured ASCII board** using `colorama`.

## Requirements

- Python 3.10 or higher (uses `X | Y` type hints)
- Install dependencies:

```
pip install -r code/requirements.txt
```

## How to run

```
python code/main.py
```

## How to play

- Each turn, roll two dice and pick a destination from the numbered list. Reachable squares are highlighted in green on the board.
- Make a suggestion from any room. Make an accusation from the Central Room.
- A wrong accusation removes you from taking turns, but you still answer other players' suggestions.
- Type `p` at any prompt to see your notesheet.

## Tests

```
pytest code/
```

## Documentation

Sphinx docs are in `docs/`. To rebuild them:

```
cd docs
make html
```

Then open `docs/build/html/index.html`.

## Code structure

| File | Responsibility |
|---|---|
| `main.py` | Entry point |
| `game.py` | Game lifecycle: setup, turns, suggestions, accusations |
| `board.py` | Board layout, adjacency map and BFS movement |
| `display.py` | Coloured ASCII board rendering |
| `player.py` | Player state: hand, notesheet, position |
| `cards.py` | `Card` dataclass |
| `dice.py` | Dice rolling |
| `endcondition.py` | `EndCondition` enum |

## Design and report

- Design decisions and research: [`design_log and brief/design_log.md`](design_log%20and%20brief/design_log.md)
- Final report: [`COM2026_B_Cluedo_Report.pdf`](COM2026_B_Cluedo_Report.pdf)

## AI assistance

Developed under the AI-assisted coursework category. All prompts and outputs are documented in comment blocks at the bottom of each `.py` file.

## Author

Joshua Bowley, BSc Physics, University of Exeter
