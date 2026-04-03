# Cluedo — Command-Line Implementation

A fully playable, turn-based implementation of the Cluedo board game for 2–6 players, written in Python and run entirely in the terminal. Developed as coursework for COM2016B.

---

## Requirements

- Python 3.10 or higher
- Windows only — `colorama` colour output is not supported on macOS or Linux

```
pip install -r code/requirements.txt
```

---

## How to Run

```
python code/main.py
```

---

## Gameplay

Players take turns rolling two dice and selecting a destination from a numbered list, highlighted in green on the board. Suggestions can be made from any room; accusations from the Central Room. A wrong accusation eliminates the player from taking turns but they remain to answer suggestions. Type `p` at any prompt to view your notesheet.

---

## Module Overview

| File | Responsibility |
|---|---|
| `main.py` | Entry point |
| `game.py` | Game lifecycle: setup, turns, suggestions, accusations |
| `board.py` | Board layout and BFS-based movement |
| `display.py` | Coloured ASCII board rendering via `colorama` |
| `player.py` | Player state: hand, notesheet, position |
| `cards.py` | `Card` dataclass |
| `dice.py` | `roll()` function |
| `endcondition.py` | `EndCondition` enum |

---

## Testing

```
pytest code/
```

Covers board movement, game state, and player behaviour across `test_board.py`, `test_game.py`, and `test_player.py`.

---

## AI Assistance

Developed under the AI-assisted coursework category. All prompts and outputs are documented in comment blocks at the bottom of each `.py` file.