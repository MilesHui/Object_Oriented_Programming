from Piece import Piece, PEASANT, KING, WHITE, BLACK

LENGTH = 8
WIDTH = 8


class AbstractBoard():
    def __init__(self, columns, rows):
        self.board = [[None for _ in range(columns)] for _ in range(rows)]
        self.populate_board()

    def populate_board(self):
        raise NotImplementedError()

    def __str__(self):
        display = []
        i = 0
        for row in range(LENGTH):
            display.append((row+1).__str__())
            for column in range(WIDTH):
                space = self.board[row][column]
                if space == None:
                    if i % 2 == 0:
                        display.append(u' \u25FB') 
                    elif i % 2 == 1:
                        display.append(u' \u25FC') 
                else:
                    display.append(self.board[row][column].__str__())
                i += 1
            i += 1
            display.append("\n")
        display.append(" ")

        i = 0
        while i < WIDTH:
            char = chr(ord('a') + i)
            display.append(" " + char)
            i += 1

        return "".join(display)


class CheckersBoard(AbstractBoard):
    def __init__(self):
        """ Initializes a 8 x 8 checkers board and populates it with the starting configuration of pieces"""
        super().__init__(LENGTH, WIDTH)
        self.populate_board()

    def populate_board(self):
        """ This method sets up the initial board in the checkers game."""

        for x in range(0, 7, 2):
            for row in range(3):
                column = x + ((row) % 2)
                self.board[row][column] = self.create_piece((row, column), PEASANT, BLACK)
                self.board[row + 5][WIDTH - column - 1] = self.create_piece((row + 5, WIDTH - column - 1), PEASANT, WHITE)

        self.black_piece_count = 12
        self.white_piece_count = 12
        self._capture_count = 1

    def change_board(self, piece, ori_location, move_type, move):
        self.board[move['arr pos'][0]][move['arr pos'][1]] = piece
        self.board[ori_location[0]][ori_location[1]] = None
        if move_type == 'jump moves':
            for cap in move['cap pos']:
                color = self.find_piece(cap).get_color()
                self.board[cap[0]][cap[1]] = None
                if color == BLACK:
                    self.black_piece_count -= 1
                elif color == WHITE:
                    self.white_piece_count -= 1

    def create_piece(self, location, rank, color):
        return Piece(location, rank, color)

    def find_piece(self, location):
        if 0 <= location[0] <= 7 and location[1] >= 0 and location[1] <= 7:
            return self.board[location[0]][location[1]]
        else:
            return None

    def valid_location(self, location):
        if location[0] >= 0 and location[0] <= 7 and location[1] >= 0 and location[1] <= 7:
            return True
        else:
            return False

    def color_piece_count(self):
        if self.white_piece_count == 0:
            return 'black has won'
        elif self.black_piece_count == 0:
            return 'white has won'
        else:
            return None

    def change_capture_count(self, move_type):
        """
        for judge draw
        """
        if move_type == 'jump moves':
            self._capture_count = 1
        else:
            self._capture_count +=1
        return self._capture_count

    def get_capture_count(self):
        return self._capture_count
