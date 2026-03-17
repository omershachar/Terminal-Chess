# Plan: Rebuild Terminal-Chess into a Playable Game

## Approach
Use **`python-chess`** (`chess` on PyPI) — it handles all the hard parts:
move generation, validation, check/checkmate/stalemate, special moves (castling,
en passant, promotion), PGN export, and UCI engine communication. We just build
the terminal UI and game loop on top.

## Steps

### 1. Install dependency
- `pip install chess`
- That's it. One dependency. Pure Python.

### 2. Rewrite `helpers.py` → board display
- Replace the hand-rolled board array with `python-chess`'s `chess.Board`
- Keep the Unicode piece rendering (reuse the existing mapping)
- Add rank/file labels, current turn indicator, last move highlight
- Add color using ANSI escape codes (light/dark squares)

### 3. Rewrite `main.py` → game loop
- Display board → prompt for input → parse move → apply → repeat
- Input format: UCI notation (`e2e4`) — simple and unambiguous
- Show legal moves hint on invalid input
- Handle special cases automatically (python-chess does this):
  - Castling (`e1g1`)
  - En passant
  - Pawn promotion (prompt user to pick piece)
- Detect and announce: check, checkmate, stalemate, draw

### 4. Add AI opponent (optional/simple)
- Use `chess.engine` to communicate with **Stockfish** via UCI if installed
- Fallback: random legal move bot (no external engine needed)
- Let user choose: PvP (2 humans) or PvAI at game start

### 5. Clean up
- Delete `Testing.py` (unused placeholder)
- Update `README.md` with usage instructions
- Add a `requirements.txt`

## File structure after rebuild
```
Terminal-Chess/
├── main.py           # Game loop, user input, mode selection
├── board_display.py  # Board rendering with Unicode + ANSI colors
├── ai.py             # AI opponent (random fallback + Stockfish if available)
├── requirements.txt  # chess
├── .gitignore
└── README.md
```

## What we get for free from python-chess
- All piece movement rules (including edge cases)
- Legal move generation & validation
- Check / checkmate / stalemate / insufficient material / 50-move rule
- FEN & PGN support
- Castling rights tracking
- En passant tracking
- Pawn promotion handling
- Board string representation
