from Board import CheckersBoard
from Command import search_move, move
import sys
from Player import HumanPlayer, RandomPlayer, GreedyPlayer
from RedoUndo import CheckersState, MementoError
from Piece import BLACK, WHITE
import copy

class Manager():
    def __init__(self):
        self._play_turns = 1
        self.board = CheckersBoard()
        self._turn_color = 'WHITE'

    def _check_victory(self):
        # print(f'capture count {self.board.get_capture_count()}')
        if self.board.color_piece_count() is not None:
            return self.board.color_piece_count()
        elif self.board.get_capture_count() > 50:
            return "draw"
        else:
            return True
            

    def _init_player(self,player):
        if player == 'human':
            return HumanPlayer()
        elif player == 'random':
            return RandomPlayer()
        elif player == 'greedy':
            return GreedyPlayer()


    def run(self, player1 = 'human', player2 = 'human', memento = 'off'):
        print(self.board.__str__())
        player1 = self._init_player(player1)
        player2 = self._init_player(player2)

        if memento == 'on':
            self.memento = CheckersState(self.board)
        else:
            self.memento = None

        draw = False
        while self._check_victory() is True:
            # saves the current state at the beginning of the round

            og_board = copy.deepcopy(self.board)

            changed_state = False

            try:
                if self._play_turns % 2 == 0 :
                    if len(player2.find_all_piece(self.board, self._turn_color, self._play_turns)) == 0:
                        print("draw")
                        return
                    changed_state = player2.run(self.board, self._turn_color, self._play_turns, self.memento)
                elif self._play_turns % 2 == 1 :
                    if len(player1.find_all_piece(self.board, self._turn_color, self._play_turns)) == 0:
                        print("draw")
                        return
                    changed_state = player1.run(self.board, self._turn_color, self._play_turns, self.memento)
            except MementoError:
                print("nothing to undo/redo")
            else:
                # updates the turn variables
                if self.memento:
                    if not changed_state:
                        self.memento.save_state(og_board)

                    self.board = self.memento.board
                    self._turn_color = self.memento.color
                    self._play_turns = self.memento.turn
                else:
                    self._play_turns += 1
                    if self._turn_color == WHITE:
                        self._turn_color = BLACK
                    else:
                        self._turn_color = WHITE
        
        print(self._check_victory())




if __name__ == '__main__':
    try:
        player1 = sys.argv[1]
    except:
        player1 = 'human'
    try:
        player2 = sys.argv[2]
    except:
        player2 = 'human'
    try:
        memento = sys.argv[3]
    except:
        memento = 'off'
    manager = Manager()
    manager.run(player1, player2, memento)