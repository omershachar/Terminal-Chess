import chess

# Outlined (white) Unicode chess glyphs U+2654–U+2659 for both sides.
# These do NOT have emoji presentation status, so they render as text in terminals.
# White vs black is distinguished by ANSI foreground color.
PIECE_SYMBOLS = {
    chess.KING:   "\u2654",  # ♔
    chess.QUEEN:  "\u2655",  # ♕
    chess.ROOK:   "\u2656",  # ♖
    chess.BISHOP: "\u2657",  # ♗
    chess.KNIGHT: "\u2658",  # ♘
    chess.PAWN:   "\u2659",  # ♙
}

# ANSI colors — lighter backgrounds so pieces stand out
RESET = "\033[0m"
LIGHT_SQ = "\033[48;2;180;160;130m"  # warm light tan
DARK_SQ = "\033[48;2;120;90;60m"    # warm brown
HIGHLIGHT = "\033[48;2;170;170;80m"  # soft yellow highlight for last move
WHITE_PC = "\033[1;38;2;255;255;255m"  # bold bright white
BLACK_PC = "\033[1;38;2;30;30;30m"     # bold near-black


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

    # Each square is 5 chars wide, 3 lines tall for a square aspect ratio
    print()
    for rank in ranks:
        # Top padding line
        print("   ", end="")
        for file in files:
            sq = chess.square(file, rank)
            bg = _sq_bg(sq, rank, file, highlight_squares)
            print(f"{bg}     {RESET}", end="")
        print()

        # Middle line with piece
        print(f" {rank + 1} ", end="")
        for file in files:
            sq = chess.square(file, rank)
            piece = board.piece_at(sq)
            bg = _sq_bg(sq, rank, file, highlight_squares)
            pc = piece_color(piece)
            ch = piece_char(piece)
            print(f"{bg}{pc}  {ch}  {RESET}", end="")
        print()

        # Bottom padding line
        print("   ", end="")
        for file in files:
            sq = chess.square(file, rank)
            bg = _sq_bg(sq, rank, file, highlight_squares)
            print(f"{bg}     {RESET}", end="")
        print()

    file_labels = "abcdefgh" if not flipped else "hgfedcba"
    print("   " + "".join(f"  {c}  " for c in file_labels))
    print()


def _sq_bg(sq, rank, file, highlight_squares):
    if sq in highlight_squares:
        return HIGHLIGHT
    if (rank + file) % 2 == 1:
        return LIGHT_SQ
    return DARK_SQ


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
