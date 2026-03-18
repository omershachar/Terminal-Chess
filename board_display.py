import chess

# Unicode chess symbols — use filled glyphs for both sides to avoid emoji rendering.
# White vs black is distinguished by ANSI text color, not glyph style.
PIECE_SYMBOLS = {
    chess.PAWN:   "♟︎",
    chess.KNIGHT: "♞︎",
    chess.BISHOP: "♝︎",
    chess.ROOK:   "♜︎",
    chess.QUEEN:  "♛︎",
    chess.KING:   "♚︎",
}

# ANSI colors
RESET = "\033[0m"
LIGHT_SQ = "\033[48;2;120;100;80m"   # muted dark tan
DARK_SQ = "\033[48;2;70;55;40m"     # deep brown
HIGHLIGHT = "\033[48;2;100;100;50m" # dim olive highlight for last move
WHITE_PC = "\033[38;5;255m"  # bright white text
BLACK_PC = "\033[38;5;232m"  # near-black text
BOLD = "\033[1m"


def piece_char(piece):
    if piece is None:
        return " "
    return PIECE_SYMBOLS[piece.piece_type]


def piece_color(piece):
    if piece is None:
        return ""
    return WHITE_PC if piece.color == chess.WHITE else BLACK_PC


def print_board(board, flipped=False, last_move=None):
    highlight_squares = set()
    if last_move:
        highlight_squares.add(last_move.from_square)
        highlight_squares.add(last_move.to_square)

    ranks = range(8) if flipped else range(7, -1, -1)
    files = range(7, -1, -1) if flipped else range(8)

    print()
    for rank in ranks:
        print(f" {rank + 1} ", end="")
        for file in files:
            sq = chess.square(file, rank)
            piece = board.piece_at(sq)
            is_light = (rank + file) % 2 == 1

            if sq in highlight_squares:
                bg = HIGHLIGHT
            elif is_light:
                bg = LIGHT_SQ
            else:
                bg = DARK_SQ

            pc = piece_color(piece)
            ch = piece_char(piece)
            print(f"{bg}{pc} {ch} {RESET}", end="")
        print()

    file_labels = "abcdefgh" if not flipped else "hgfedcba"
    print("   " + "".join(f" {c} " for c in file_labels))
    print()


def print_status(board):
    turn = "White" if board.turn == chess.WHITE else "Black"

    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        print(f"  Checkmate! {winner} wins!")
    elif board.is_stalemate():
        print("  Stalemate! It's a draw.")
    elif board.is_insufficient_material():
        print("  Draw by insufficient material.")
    elif board.can_claim_fifty_moves():
        print("  Draw claimable by 50-move rule.")
    elif board.is_repetition(3):
        print("  Draw claimable by threefold repetition.")
    elif board.is_check():
        print(f"  {turn} is in check!")
    else:
        print(f"  {turn} to move.")
