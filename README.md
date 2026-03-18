# Terminal Chess

A fully playable chess game in your terminal with ANSI-colored board, Unicode pieces, move history sidebar, and AI opponent.

## Setup

```bash
pip install -r requirements.txt
```

## Play

```bash
python main.py
```

## Modes

- **Player vs Player** — two humans, same terminal
- **Player vs AI (White)** — you play White against the computer
- **Player vs AI (Black)** — you play Black against the computer

The AI uses Stockfish if installed, otherwise falls back to a random-move bot.

## Controls

| Command     | Action                          |
|-------------|---------------------------------|
| `e2e4`      | Move in UCI notation            |
| `Nf3`       | Move in algebraic notation      |
| `O-O`       | Kingside castle                 |
| `moves`     | Show all legal moves            |
| `undo`      | Take back last move             |
| `flip`      | Flip the board                  |
| `quit`      | Exit the game                   |

## Requirements

- Python 3.8+
- `chess` (python-chess)
- Stockfish (optional, for stronger AI)
