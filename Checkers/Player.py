from Command import search_move, move
import random

class player():
    def __init__(self):
        pass

    def _str_location(self, location):
        #print(location[1])
        return f'{chr(location[1]+97)}{location[0]+1}'


    def _str_moves(self, move_type, all_moves, piece_to_move):
        for num, move in enumerate(all_moves):
            arr_pos = self._str_location(move['arr pos'])
            translation = {39: None}
            # string = f'{num}: {move_type}: {piece_to_move}->{move}'
            if move_type == 'basic moves':
                string = f'{num}: {move_type}: {piece_to_move}->{arr_pos}'
            elif move_type == 'jump moves':
                cap = [self._str_location(x).strip('"\'') for x in move['cap pos']]
                string = f'{num}: {move_type}: {piece_to_move}->{arr_pos}, capturing {cap}'
            print (string.translate(translation))  # remove the ''


    def combine_position(self, position):
        row = str(position[0]+1)
        col = chr(position[1]+ord('a'))
        string = col+row
        return string


    def find_all_piece(self, board, turn_color, play_turns):
        all_pieces = []
        for row in range(8):
            for col in range(8):
                row_col = (row, col)
                piece_to_move = self.combine_position(row_col)
                a = search_move(piece=piece_to_move, board=board, turn=turn_color)
                try:
                    move_type, all_moves = a.execute()
                    # print(all_moves)
                    # self._str_moves(move_type, all_moves, piece_to_move)
                except:
                    pass
                else:
                    all_pieces.append([piece_to_move, a])
        all_pieces_moves = []

        for piece in all_pieces:
            move_type, all_moves = piece[1].execute()
            #self._str_moves(move_type, all_moves, piece[0])
            all_pieces_moves.append({'move type': move_type, 'all moves': all_moves, 'piece to move': piece[0]})

        return all_pieces_moves

    def apply_state(self, memento, curr_board):
        if memento:
            state = input("undo, redo, or next\n")
            if state == 'undo':
                board = memento.undo(curr_board)
                print(board)
                return True
            elif state == 'redo':
                board = memento.redo()
                print(board)
                return True
            elif state == 'next':
                memento.next()
                return False
            else:
                raise ValueError
        return False

    def read_text(self):
        with open('seed.txt', 'r') as seed:
            return seed.read()


    def move(self, board, turn_color, play_turns, all_pieces_moves):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
        


class HumanPlayer(player):
    def __init__(self):
        pass

    def select_piece(self, board, turn_color, play_turns):
        print('Select a piece to move')
        piece_to_move = input()
        a = search_move(piece=piece_to_move, board=board, turn=turn_color)
        self.find_move(board, turn_color, play_turns, piece_to_move, a)

    def find_move(self, board, turn_color, play_turns, piece_to_move, a):
        try:
            move_type, all_moves = a.execute()
            # print(all_moves)
            self._str_moves(move_type, all_moves, piece_to_move)

        except:
            print(a.execute())
            self.select_piece(board, turn_color, play_turns)
        else:
            all_pieces_moves = self.find_all_piece(board, turn_color, play_turns)
            jump_count = 0
            for all_pieces_move in all_pieces_moves:
                if all_pieces_move['move type'] == 'jump moves':
                    jump_count += 1
            if move_type == 'jump moves':
                self.move(board, turn_color, play_turns, piece_to_move, move_type, all_moves)
            elif move_type == 'basic moves' and jump_count != 0 :
                print('That piece cannot move')
                self.select_piece(board, turn_color, play_turns)
            elif move_type == 'basic moves' and jump_count == 0 :
                self.move(board, turn_color, play_turns, piece_to_move, move_type, all_moves)

    def move(self,board, turn_color, play_turns, piece_to_move, move_type, all_moves):
        print('Select a move by entering the corresponding index')
        index = input()
        index = int(index)
        b = move(board=board, piece=piece_to_move, move_type=move_type, move=all_moves[index])
        b.execute()
        print(board)


    def run(self, board, turn_color, play_turns, memento):
        print(f'Turn {play_turns}, {turn_color.lower()}')
        if not self.apply_state(memento, board):
            self.select_piece(board, turn_color, play_turns)
            return False
        return True



class RandomPlayer(player):
    def __init__(self):
        pass

    def move(self,  board, turn_color, play_turns, all_pieces_moves):
        print(board)
        seed = self.read_text()
        random.seed(int(seed))
        index_of_piece = random.randint(0,len(all_pieces_moves)-1)
        index_of_move = random.randint(0,len(all_pieces_moves[index_of_piece]['all moves'])-1)
        b = move(board=board, piece=all_pieces_moves[index_of_piece]['piece to move'],
                 move_type=all_pieces_moves[index_of_piece]['move type'],
                 move=all_pieces_moves[index_of_piece]['all moves'][index_of_move])
        b.execute()


    def run(self, board, turn_color, play_turns, memento):
        print(f'Turn {play_turns}, {turn_color.lower()}')
        if not self.apply_state(memento, board):
            all_pieces_moves = self.find_all_piece(board, turn_color, play_turns)
            self.move(board, turn_color, play_turns, all_pieces_moves)
            return False
        return True











class GreedyPlayer(player):
    def __init__(self):
        pass

    def move(self, board, turn_color, play_turns, all_pieces_moves):
        max_len = 0
        index_of_piece = 0
        index_of_move = 0
        seed = self.read_text()
        random.seed(int(seed))
        print(board)
        for index, moves in enumerate(all_pieces_moves):
            if moves['move type'] == 'jump moves':
                for index2, captures in enumerate(moves['all moves']):
                    if len(captures['cap pos']) > max_len:
                        index_of_piece = index
                        index_of_move = index2
            else: 
                index_of_piece = random.randint(0,len(all_pieces_moves)-1)
                index_of_move = random.randint(0,len(all_pieces_moves[index_of_piece]['all moves'])-1)

        b = move(board=board, piece=all_pieces_moves[index_of_piece]['piece to move'],
                 move_type=all_pieces_moves[index_of_piece]['move type'],
                 move=all_pieces_moves[index_of_piece]['all moves'][index_of_move])
        b.execute()

    def run(self, board, turn_color, play_turns, memento):
        print(f'Turn {play_turns}, {turn_color.lower()}')
        if not self.apply_state(memento, board):
            all_pieces_moves = self.find_all_piece(board, turn_color, play_turns)
            self.move(board, turn_color, play_turns, all_pieces_moves)
            return False
        return True


