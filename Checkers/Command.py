from Piece import Piece, PEASANT, KING, WHITE, BLACK
from Board import CheckersBoard

# board = CheckersBoard()
# piece20 = board.board[3][3]
# color = piece20.get_color()
# rank = piece20.get_rank()
# location = piece20.get_location()
# board.find_piece((0,0))

class command:

    def split(self, word):
        return [char for char in word]

    def split_position(self, position):
        position = self.split(position)
        col = ord(position[0]) - ord('a')
        row = int(position[1])-1
        return (row, col)


    def _find_piece(self, piece_to_move):
        location = self.split_position(piece_to_move)

        return self.board.find_piece(location)



class search_move(command):
    def __init__(self, piece, board,turn):

        self.board = board
        self.piece = self._find_piece(piece)
        self.turn = turn


    def execute(self):
        if self.piece == None:
            return 'No piece at that location'
        elif self.piece.get_color() != self.turn:
            return 'That is not your piece'
        else:
            return self.piece.search_move(self.board)

        
class move(command):
    def __init__(self, board, piece, move_type, move):

        self.board = board
        self.piece = self._find_piece(piece)
        self.move_type = move_type
        self.move = move

    def execute(self):
        ori_location = self.piece.get_location()
        self.piece.change_location(self.move['arr pos'])
        self.piece.king_promotion(self.move['arr pos'])
        self.board.change_board(self.piece, ori_location, self.move_type, self.move)
        self.board.change_capture_count(self.move_type)
















