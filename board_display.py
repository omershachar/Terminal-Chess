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
DIM = "\033[2m"


def piece_char(piece):
    if piece is None:
        return " "
    return PIECE_SYMBOLS[piece.piece_type]


def piece_color(piece):
    if piece is None:
        return ""
    return WHITE_PC if piece.color == chess.WHITE else BLACK_PC


def _sq_bg(sq, rank, file, highlight_squares):
    if sq in highlight_squares:
        return HIGHLIGHT
    if (rank + file) % 2 == 1:
        return LIGHT_SQ
    return DARK_SQ


def _build_move_lines(board):
    """Build move list lines in two-column format (1. e4 e5)."""
    lines = []
    temp = board.copy()
    # Replay all moves to get SAN notation
    moves_san = []
    move_stack = list(board.move_stack)
    temp.reset()
    for move in move_stack:
        moves_san.append(temp.san(move))
        temp.push(move)

    # Pair into (white_move, black_move) per move number
    for i in range(0, len(moves_san), 2):
        num = i // 2 + 1
        white = moves_san[i]
        black = moves_san[i + 1] if i + 1 < len(moves_san) else ""
        lines.append(f"{num:>2}. {white:<7} {black}")

    return lines


def print_board(board, flipped=False, last_move=None):
    highlight_squares = set()
    if last_move:
        highlight_squares.add(last_move.from_square)
        highlight_squares.add(last_move.to_square)

    ranks = range(8) if flipped else range(7, -1, -1)
    files = range(7, -1, -1) if flipped else range(8)

    move_lines = _build_move_lines(board)
    # Show last 8 moves to fit beside the board, scroll if more
    if len(move_lines) > 8:
        visible_moves = move_lines[-8:]
        scroll_indicator = True
    else:
        visible_moves = move_lines
        scroll_indicator = False

    board_lines = []

    for rank in ranks:
        line = f" {rank + 1} "
        for file in files:
            sq = chess.square(file, rank)
            piece = board.piece_at(sq)
            bg = _sq_bg(sq, rank, file, highlight_squares)
            pc = piece_color(piece)
            ch = piece_char(piece)
            line += f"{bg}{pc} {ch} {RESET}"
        board_lines.append(line)

    file_labels = "abcdefgh" if not flipped else "hgfedcba"
    board_lines.append("   " + "".join(f" {c} " for c in file_labels))

    # Print board with move sidebar
    print()
    sidebar_header_printed = False
    for i, bline in enumerate(board_lines):
        sidebar = ""
        if i == 0:
            sidebar = f"  {DIM}Moves{RESET}"
            sidebar_header_printed = True
        elif i == 1 and scroll_indicator:
            sidebar = f"  {DIM}  ...{RESET}"
        elif sidebar_header_printed:
            # Offset: row 1 is header, row 2 might be "...", rest are moves
            move_idx = i - (2 if scroll_indicator else 1)
            if 0 <= move_idx < len(visible_moves):
                sidebar = f"  {DIM}{visible_moves[move_idx]}{RESET}"
        print(f"{bline}{sidebar}")
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
