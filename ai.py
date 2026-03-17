import random
import shutil
import chess
import chess.engine

STOCKFISH_NAMES = ["stockfish", "stockfish.exe"]


def find_stockfish():
    for name in STOCKFISH_NAMES:
        path = shutil.which(name)
        if path:
            return path
    return None


class RandomBot:
    def pick_move(self, board):
        return random.choice(list(board.legal_moves))

    def close(self):
        pass


class StockfishBot:
    def __init__(self, path, time_limit=0.5):
        self.engine = chess.engine.SimpleEngine.popen_uci(path)
        self.time_limit = time_limit

    def pick_move(self, board):
        result = self.engine.play(board, chess.engine.Limit(time=self.time_limit))
        return result.move

    def close(self):
        self.engine.quit()


def create_bot(use_stockfish=True):
    if use_stockfish:
        path = find_stockfish()
        if path:
            try:
                return StockfishBot(path), "Stockfish"
            except Exception:
                pass
    return RandomBot(), "Random Bot"
