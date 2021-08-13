from Piece import WHITE, BLACK
import copy

class MementoError(Exception):
    pass

class Memento():
    # holds critical information of game in a stack
    def __init__(self):
        pass

class CheckersState(Memento):
    def __init__(self, board):
        self.redo_stack = []
        self.undo_stack = []
        self.board = board
        self.turn = 1
        self.color = WHITE

    def save_state(self, board):
        self.undo_stack.append(board)
        self.turn += 1

        if self.color == BLACK:
            self.color = WHITE
        else:
            self.color = BLACK
    

    def redo(self):
        if self.redo_stack:
            board = self.redo_stack.pop()
            self.undo_stack.append(copy.deepcopy(board))
            self.turn += 1
            if self.color == BLACK:
                self.color = WHITE
            else:
                self.color = BLACK
            returned_board = self.redo_stack.pop()
            self.board = returned_board

            return returned_board
        else:
            raise MementoError
    def undo(self, curr_board):
        if self.undo_stack:
            board = self.undo_stack.pop()
            self.redo_stack.append(copy.deepcopy(curr_board))
            self.redo_stack.append(copy.deepcopy(board))
            self.turn -= 1

            if self.color == BLACK:
                self.color = WHITE
            else:
                self.color = BLACK
            self.board = board

            return board
        else:
            raise MementoError

    def next(self):
        self.redo_stack.clear()
