import copy
import random


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

    def possible_moves(self, board):
        possible = set()
        for row in board[::-1]:
            for piece in row:
                if not self.is_occupied(piece):
                    move = (piece.column, piece.row)
                    if move[1] == 5:
                        possible.add(move)
                    else:
                        tempmove = move[0], (move[1]+1)
                        if (tempmove) not in possible:
                            tempmove = move[0], (move[1]+2)
                        if (tempmove) not in possible:
                            tempmove = move[0], (move[1]+3)
                        if (tempmove) not in possible:
                            tempmove = move[0], (move[1]+4)
                        if (tempmove) not in possible:
                            tempmove = move[0], (move[1]+5)
                        if (tempmove) not in possible:
                            possible.add(move)
        return possible

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

    def ai_add_piece(self, row, col):
        piece = Piece(col, row)
        piece.set_color(self.get_turn())
        self.board[col][row] = piece
        self.__change_turn()

    def is_board_full(self):
        for row in self.board:
            for piece in row:
                if piece.color == "white":
                    return False
        return True

    def is_winner(self, board):
        boardHeight = len(board[0])
        boardWidth = len(board)
        # vertical
        for y in range(boardHeight):
            for x in range(boardWidth - 3):
                if board[x][y].color == "red" and board[x+1][y].color == "red" and board[x+2][y].color == "red" and board[x+3][y].color == "red":
                    return True, "red"

                if board[x][y].color == "blue" and board[x+1][y].color == "blue" and board[x+2][y].color == "blue" and board[x+3][y].color == "blue":
                    return True, "blue"

        # horizontal
        for x in range(boardWidth):
            for y in range(boardHeight - 3):
                if board[x][y].color == "red" and board[x][y+1].color == "red" and board[x][y+2].color == "red" and board[x][y+3].color == "red":
                    return True, "red"

                if board[x][y].color == "blue" and board[x][y+1].color == "blue" and board[x][y+2].color == "blue" and board[x][y+3].color == "blue":
                    return True, "blue"

        # / diagonal
        for x in range(boardWidth - 3):
            for y in range(3, boardHeight):
                if board[x][y].color == "red" and board[x+1][y-1].color == "red" and board[x+2][y-2].color == "red" and board[x+3][y-3].color == "red":
                    return True, "red"
                if board[x][y].color == "blue" and board[x+1][y-1].color == "blue" and board[x+2][y-2].color == "blue" and board[x+3][y-3].color == "blue":
                    return True, "blue"

        # \ diagonal
        for x in range(boardWidth - 3):
            for y in range(boardHeight - 3):
                if board[x][y].color == "red" and board[x+1][y+1].color == "red" and board[x+2][y+2].color == "red" and board[x+3][y+3].color == "red":
                    return True, "red"
                if board[x][y].color == "blue" and board[x+1][y+1].color == "blue" and board[x+2][y+2].color == "blue" and board[x+3][y+3].color == "blue":
                    return True, "blue"
        return False, ""

    def get_best_move(self, moves):
        # copy the current board for our simulations
        board = copy.deepcopy(self.board)
        moves_dict = {i: 0 for i in moves}

        for move in moves:
            if moves_dict[move] == 0:
                board[move[1]][move[0]].set_color(self.get_turn())
                win, winner_color = self.is_winner(board)
                # check if AI can win
                if win:
                    if winner_color == self.get_turn():
                        moves_dict[move] = 50
                        return move
                else:
                    # check if the player can win next turn
                    board[move[1]][move[0]].set_color("red")
                    win, winner_color = self.is_winner(board)
                    if win and winner_color == "red":
                        moves_dict[move] = 40
                    else:
                        # mark as "just visited" if its not a "winning/
                        # prevent player from winning" move
                        moves_dict[move] = 1
                        board[move[1]][move[0]].set_color("white")

        counter = 0
        for move, value in moves_dict.items():
            if value > counter:
                best = move
                counter = value
        # if all our moves are equally good/bad we pick one at random
        if counter == 1:
            best = random.choice(list(moves_dict.keys()))
        return best
