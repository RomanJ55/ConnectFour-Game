from tkinter import *
from constants import MARGIN, CELL_WIDTH

WIDTH = MARGIN*2 + CELL_WIDTH*7
HEIGHT = MARGIN*2 + CELL_WIDTH*6


class Connect_Four_UI(Frame):
    def __init__(self, board):
        self.connectfour = board
        self.parent = Tk()
        Frame.__init__(self, self.parent)

        self.row, self.col = -1, -1
        self.__initialize()

    def __initialize(self):
        self.parent.title("Connect Four")
        self.parent.option_add("*Font", "comicsans 15")
        self.pack(fill=BOTH)

        # UI Elements
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.canvas_top = Canvas(self, width=WIDTH-MARGIN * 2, height=50)
        self.canvas_top.place(x=MARGIN, y=MARGIN//3)
        Misc.lift(self.canvas_top)
        self.button = Button(self, text="Show possible moves",
                             command=self.__draw_possible_moves)
        self.button.pack(side=BOTTOM)

        self.__draw_board()
        self.__draw_pieces()

        self.canvas_top.bind("<Button-1>", self.__clicked)

    def __draw_board(self):
        for i in range(8):
            # vertical
            x0 = MARGIN + i*CELL_WIDTH
            y0 = MARGIN
            x1 = MARGIN + i*CELL_WIDTH
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill="BLACK", width=10)

            # horizontal
            x0 = MARGIN
            y0 = MARGIN + i*CELL_WIDTH
            x1 = WIDTH-MARGIN
            y1 = MARGIN + i*CELL_WIDTH
            self.canvas.create_line(x0, y0, x1, y1, fill="BLACK", width=10)

    def __draw_pieces(self):
        self.canvas_top.delete("arrows")
        self.canvas.delete("turncol")
        for i in range(7):
            for j in range(6):
                piece = self.connectfour.board[j][i]
                if piece != None:
                    x0 = MARGIN + i*CELL_WIDTH
                    y0 = MARGIN + j*CELL_WIDTH
                    x1 = MARGIN + (i+1)*CELL_WIDTH
                    y1 = MARGIN + (j+1)*CELL_WIDTH

                    self.canvas.create_oval(
                        x0+6, y0+6, x1-6, y1-6, fill=piece.color)

        self.canvas.create_text(
            425, 725, fill=self.connectfour.get_turn(), tag="turncol", text=f"{self.connectfour.get_turn().upper()} Turn", font="comicsans 30")

        # check if game has ended after the last move
        x, y = self.game_end()
        if x != 0 and x != False:
            self.canvas.create_text(
                WIDTH//2, 40, text="Game ended!", font="comicsans 40", fill="grey")
            if x == 3:
                self.canvas.create_text(
                    WIDTH//2, 720, text="Game tied!", font="comicsans 40", fill="grey")
            else:
                self.canvas.create_text(
                    WIDTH//2, 720, text=f"{y.upper()} won!", font="comicsans 40", fill="grey")
            self.canvas.delete("turncol")
            self.button.destroy()
            self.canvas_top.destroy()

    def __draw_possible_moves(self):
        moves = self.connectfour.get_possible_moves()
        turn = self.connectfour.get_turn()
        for move in moves:
            x0 = 55 + move*CELL_WIDTH
            y0 = 15
            x1 = 55 + move*CELL_WIDTH
            y1 = MARGIN//2 + 10
            self.canvas_top.create_line(
                x0, y0, x1, y1, tag="arrows", arrow="last", fill=turn, width=5)

    def __add_piece(self, row, col):
        self.connectfour.add_piece(row, col)
        self.__draw_pieces()

    def __clicked(self, event):
        x, y, = event.x, event.y
        if x < CELL_WIDTH:
            cell_col = 0
        else:
            cell_col = x//CELL_WIDTH
        cell_row = 5
        self.__add_piece(cell_row, cell_col)

    def game_end(self):
        if self.connectfour.is_winner():
            x, y = self.connectfour.is_winner()
            return x, y
        elif self.connectfour.is_board_full():
            return 3, ""
        else:
            return 0, ""
