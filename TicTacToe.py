from copy import deepcopy
from typing import Final, Literal, Optional

Entry = Literal["X", "O", "."]
TIC: Final[Entry] = "X"
TAC: Final[Entry] = "O"
EMPTY: Final[Entry] = "."
Point = tuple[int, int]
GameState = dict[tuple[int, int], Entry]

INT32_MIN: Final[int] =  -2_147_483_648
INT32_MAX: Final[int] = 2_147_483_647
LOSING: Final[int] = -1
WINNING: Final[int] = +1
TIE = 0

class Board:
    player: Entry = TIC
    opponent: Entry = TAC
    size: Final[int] = 3
    fields: GameState = {}

    def __init__(self, other=None):
        if other:
            self.__dict__ = deepcopy(other.__dict__)
            return
        self.fields = {}
        for y in range(self.size):
            for x in range(self.size):
                self.fields[x, y] = EMPTY

    def move(self, x: int, y: int):
        """
        Returns a new board with the move executed
        """
        assert (
            x < self.size and y < self.size and self.fields[x, y] == EMPTY
        ), "Invalid move"
        board = Board(self)
        board.fields[x, y] = board.player
        (board.player, board.opponent) = (board.opponent, board.player)
        return board

    def minimax(self, is_opponent_move: bool)-> tuple[int, Optional[Point]]:
        """
        Calculate the minimax value of a board

        Params:
            is_opponent_move: if it's the opponent's move.
            i.e. whether to maximize or minimize the value

        Returns:
            the score of the current board
            and the move that leads to such score
        
        Recursion stop when either the game is won or tied

        WINING and LOSING and `opponent` are relative to the bot/algorithms perspective.
        """
        won, _ = self.won()
        if won:
            if is_opponent_move:
                return (LOSING, None)
            return (WINNING, None)
        elif Board.no_empty(self.fields):
            return (TIE, None)
        elif is_opponent_move:
            best = (INT32_MIN, None)
            for x, y in self.fields:
                if self.fields[x, y] == EMPTY:
                    # Depth first search, essentially
                    #
                    # the next move is my move, should maximize it
                    value, _ = self.move(x, y).minimax(False)
                    if value > best[0]:
                        best = (value, (x, y))
                        if value == WINNING:
                            break
            return best
        else:
            best = (INT32_MAX, None)
            for x, y in self.fields:
                if self.fields[x, y] == EMPTY:
                    value, _ = self.move(x, y).minimax(True)
                    if value < best[0]:
                        best = (value, (x, y))
                        if value == LOSING:
                            break
            return best

    def best(self):
        """
        The best move
        """
        return self.minimax(True)[1]

    @staticmethod
    def no_empty(fields: GameState) -> bool:
        """
        Check if there are no empty fields left
        """
        for x, y in fields:
            if fields[x, y] == EMPTY:
                return False
        return True

    def won(self) -> tuple[bool, list[Point]]:
        """
        Check if the current player has won
        """
        # horizontal
        for y in range(self.size):
            winning = []
            for x in range(self.size):
                if self.fields[x, y] == self.opponent:
                    winning.append((x, y))
            if len(winning) == self.size:
                return True, winning
        # vertical
        for x in range(self.size):
            winning = []
            for y in range(self.size):
                if self.fields[x, y] == self.opponent:
                    winning.append((x, y))
            if len(winning) == self.size:
                return True, winning
        # diagonal
        winning = []
        for y in range(self.size):
            x = y
            if self.fields[x, y] == self.opponent:
                winning.append((x, y))
        if len(winning) == self.size:
            return True, winning
        # other diagonal
        winning = []
        for y in range(self.size):
            x = self.size - 1 - y
            if self.fields[x, y] == self.opponent:
                winning.append((x, y))
        if len(winning) == self.size:
            return True, winning
        # default
        return False, []

    def __str__(self) -> str:
        string = ""
        for y in range(self.size):
            for x in range(self.size):
                string += self.fields[x, y]
            string += "\n"
        return string
