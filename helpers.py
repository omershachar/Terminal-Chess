def print_board(board, flipped=False):
    # Unicode pieces
    pieces = {
        "R": "♜", "N": "♞", "B": "♝", "Q": "♛", "K": "♚", "P": "♟",
        "r": "♖", "n": "♘", "b": "♗", "q": "♕", "k": "♔", "p": "♙", ".": "∙"
    }

    # Rotate board if flipped    
    if flipped:
        board = board[::-1]

    for i, row in enumerate(board, 1):
        print(9 - i if not flipped else i, end=" ")
        print(" ".join(pieces[cell] for cell in row))
    print("  a b c d e f g h\n")

# Initialize the board
chess_board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]

# Print board from opponent's perspective
print_board(chess_board, flipped=False)
# print_board(chess_board, flipped=True)