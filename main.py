import chess
from board_display import print_board, print_status
from ai import create_bot


def clear_screen():
    print("\033[2J\033[H", end="")


def get_promotion_piece():
    pieces = {"q": chess.QUEEN, "r": chess.ROOK, "b": chess.BISHOP, "n": chess.KNIGHT}
    while True:
        choice = input("  Promote to (q/r/b/n): ").strip().lower()
        if choice in pieces:
            return pieces[choice]
        print("  Invalid choice. Enter q, r, b, or n.")


def parse_move(board, text):
    text = text.strip()

    # Try UCI format (e.g. e2e4) — UCI is case-insensitive
    try:
        move = chess.Move.from_uci(text.lower())
        if move in board.legal_moves:
            return move
    except ValueError:
        pass

    # Try SAN format (e.g. Nf3, O-O) — SAN is case-sensitive
    try:
        move = board.parse_san(text)
        return move
    except (ValueError, chess.InvalidMoveError, chess.IllegalMoveError, chess.AmbiguousMoveError):
        pass

    # Check if it's a pawn promotion without specifying piece
    if len(text) == 4:
        for suffix in ["q", "r", "b", "n"]:
            try:
                move = chess.Move.from_uci(text.lower() + suffix)
                if move in board.legal_moves:
                    piece = get_promotion_piece()
                    return chess.Move.from_uci(text + {
                        chess.QUEEN: "q", chess.ROOK: "r",
                        chess.BISHOP: "b", chess.KNIGHT: "n"
                    }[piece])
            except ValueError:
                pass

    return None


def select_mode():
    print("  Terminal Chess")
    print("  ─────────────")
    print("  1) Player vs Player")
    print("  2) Player vs AI (you play White)")
    print("  3) Player vs AI (you play Black)")
    print()
    while True:
        choice = input("  Select mode (1/2/3): ").strip()
        if choice in ("1", "2", "3"):
            return int(choice)
        print("  Invalid choice.")


def game_loop():
    clear_screen()
    mode = select_mode()

    board = chess.Board()
    bot = None
    bot_name = None
    bot_color = None
    flipped = False

    if mode == 2:
        bot, bot_name = create_bot()
        bot_color = chess.BLACK
        print(f"\n  AI: {bot_name}")
    elif mode == 3:
        bot, bot_name = create_bot()
        bot_color = chess.WHITE
        flipped = True
        print(f"\n  AI: {bot_name}")

    last_move = None

    try:
        while not board.is_game_over():
            clear_screen()
            print_board(board, flipped=flipped, last_move=last_move)
            print_status(board)

            # AI turn
            if bot and board.turn == bot_color:
                print(f"  {bot_name} is thinking...")
                move = bot.pick_move(board)
                board.push(move)
                last_move = move
                continue

            # Human turn
            try:
                text = input("  Your move: ").strip()
            except EOFError:
                break

            if text.lower() in ("quit", "exit", "q"):
                print("  Game ended.")
                break
            if text.lower() == "moves":
                moves = sorted(board.san(m) for m in board.legal_moves)
                print("  Legal moves:", ", ".join(moves))
                input("  Press Enter to continue...")
                continue
            if text.lower() == "flip":
                flipped = not flipped
                continue
            if text.lower() == "undo":
                if len(board.move_stack) >= (2 if bot else 1):
                    board.pop()
                    if bot:
                        board.pop()
                    last_move = board.peek() if board.move_stack else None
                continue

            move = parse_move(board, text)
            if move is None:
                print("  Invalid move. Type 'moves' to see legal moves.")
                input("  Press Enter to continue...")
                continue

            board.push(move)
            last_move = move

        # Game over screen
        clear_screen()
        print_board(board, flipped=flipped, last_move=last_move)
        print_status(board)
        print(f"  Game over. Result: {board.result()}")
        print()

    finally:
        if bot:
            bot.close()


if __name__ == "__main__":
    game_loop()
