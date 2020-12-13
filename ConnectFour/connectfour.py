
class Piece(object):
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.color = "white"  # default

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color


class Board(object):
    def __init__(self):
        # Initialize a 7x6 matrix of Piece objects
        self.board = [[Piece(r, c) for c in range(7)] for r in range(6)]
        self.turn = "red"  # red starts

    def __get_row(self, row):
        return [piece.row for piece in self.board[row]]

    def __get_column(self, column):
        return [self.board[row][column].column for row in range(6)]

    def __change_turn(self):
        if self.turn == "red":
            self.turn = "blue"
        else:
            self.turn = "red"

    def get_turn(self):
        return self.turn

    def get_possible_moves(self):
        moves = []
        for i in range(7):
            for j in range(1):
                piece = self.board[j][i]
                if piece.color == "white":
                    moves.append(i)

        return moves

    def is_occupied(self, piece):
        row, col = piece.row, piece.column
        if self.board[row][col].color != "white":
            return True
        else:
            return False

    def add_piece(self, row, col):
        piece = Piece(row, col)
        piece.set_color(self.get_turn())
        if self.is_occupied(piece):
            if piece.row != 0:
                piece.row -= 1
                self.add_piece(piece.row, piece.column)
        else:
            self.board[row][col] = piece
            self.__change_turn()

    def is_board_full(self):
        for row in self.board:
            for piece in row:
                if piece.color == "white":
                    return False
        return True

    def is_winner(self):
        boardHeight = len(self.board[0])
        boardWidth = len(self.board)
        # vertical
        for y in range(boardHeight):
            for x in range(boardWidth - 3):
                if self.board[x][y].color == "red" and self.board[x+1][y].color == "red" and self.board[x+2][y].color == "red" and self.board[x+3][y].color == "red":
                    return True, "red"

                if self.board[x][y].color == "blue" and self.board[x+1][y].color == "blue" and self.board[x+2][y].color == "blue" and self.board[x+3][y].color == "blue":
                    return True, "blue"

        # horizontal
        for x in range(boardWidth):
            for y in range(boardHeight - 3):
                if self.board[x][y].color == "red" and self.board[x][y+1].color == "red" and self.board[x][y+2].color == "red" and self.board[x][y+3].color == "red":
                    return True, "red"

                if self.board[x][y].color == "blue" and self.board[x][y+1].color == "blue" and self.board[x][y+2].color == "blue" and self.board[x][y+3].color == "blue":
                    return True, "blue"

        # / diagonal
        for x in range(boardWidth - 3):
            for y in range(3, boardHeight):
                if self.board[x][y].color == "red" and self.board[x+1][y-1].color == "red" and self.board[x+2][y-2].color == "red" and self.board[x+3][y-3].color == "red":
                    return True, "red"
                if self.board[x][y].color == "blue" and self.board[x+1][y-1].color == "blue" and self.board[x+2][y-2].color == "blue" and self.board[x+3][y-3].color == "blue":
                    return True, "blue"

        # \ diagonal
        for x in range(boardWidth - 3):
            for y in range(boardHeight - 3):
                if self.board[x][y].color == "red" and self.board[x+1][y+1].color == "red" and self.board[x+2][y+2].color == "red" and self.board[x+3][y+3].color == "red":
                    return True, "red"
                if self.board[x][y].color == "blue" and self.board[x+1][y+1].color == "blue" and self.board[x+2][y+2].color == "blue" and self.board[x+3][y+3].color == "blue":
                    return True, "blue"
        return False
