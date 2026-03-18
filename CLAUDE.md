# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Terminal-based chess game (Python) with ANSI-colored Unicode board, UCI/SAN move input, and optional Stockfish AI opponent. Built on `python-chess` which handles all rules, move validation, and engine communication.

## Commands

```bash
pip install -r requirements.txt   # Install dependency (just `chess`/python-chess)
python main.py                    # Run the game
```

No tests, linter, or build system — it's a single-dependency terminal app.

## Architecture

Three files, each with a single responsibility:

- **`main.py`** — Game loop, input parsing (UCI + SAN), mode selection (PvP / PvAI), promotion prompts, undo/flip commands. Entry point.
- **`board_display.py`** — ANSI-colored board rendering with Unicode chess glyphs and move history sidebar. Uses outlined glyphs (`♔♕♖♗♘♙`, U+2654–U+2659) for both sides; white vs black is distinguished by ANSI foreground color. Outlined glyphs are used because the filled pawn (U+265F) has emoji presentation status and renders as emoji in many terminals.
- **`ai.py`** — Bot interface: `StockfishBot` (UCI engine, 0.5s time limit) with auto-discovery via `shutil.which`, falls back to `RandomBot` (random legal move).

## Key Design Decisions

- **Outlined Unicode glyphs only**: Both white and black pieces use outlined glyphs (U+2654–U+2659). The filled pawn (U+265F) has emoji presentation status and renders as emoji in many terminals. Color is conveyed via ANSI foreground color instead.
- **SAN is case-sensitive**: `parse_move` must not lowercase the input before trying SAN parsing — uppercase letters denote piece type (N=Knight, B=Bishop, etc.). Only the UCI path lowercases.
- **Bot protocol**: Bots implement `pick_move(board) -> chess.Move` and `close()`. The game loop calls `close()` in a `finally` block to shut down Stockfish cleanly.
- **Stockfish is optional**: The game works without it — AI mode just uses random moves as fallback.
