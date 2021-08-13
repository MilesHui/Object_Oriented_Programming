BLACK, WHITE = ("BLACK", "WHITE")
KING, PEASANT = ("KING", "PEASANT")

class Piece():
    def __init__(self, location, rank, color):
        self.location = location
        self.rank = rank
        self.color = color

    def __str__(self):
        if self.color == WHITE:
            if self.rank == PEASANT:
                return u' \u2686'
            elif self.rank == KING:
                return u' \u2687'
        else:
            if self.rank == PEASANT:
                return u' \u2688'
            elif self.rank == KING:
                return u' \u2689'

    def get_location(self):
        return self.location

    def get_rank(self):
        return self.rank

    def get_color(self):
        return self.color

    def change_location(self, new_location):
        self.location = new_location

    def king_promotion(self, new_location):
        if new_location[0] == 0 or new_location[0] == 7:
            self.rank = KING






    def search_one_direction(self, location, direction, board):
        """
        Based the given location, and given direction: NE, NW, SE, SW,
        search whether there are nearby piece or space

        This function will return a list of nearby position, nearby pieces and searching direction
        """
        if direction == 'NE':
            next_pos = (location[0] - 1, location[1] + 1)
            next_pos_2 = (location[0] - 2, location[1] + 2) # the potential location to jump to
        elif direction == 'NW':
            next_pos = (location[0] - 1, location[1] - 1)
            next_pos_2 = (location[0] - 2, location[1] - 2)
        elif direction == 'SE':
            next_pos = (location[0] + 1, location[1] + 1)
            next_pos_2 = (location[0] + 2, location[1] + 2)
        elif direction == 'SW':
            next_pos = (location[0] + 1, location[1] - 1)
            next_pos_2 = (location[0] + 2, location[1] - 2)

        return [next_pos, board.find_piece(next_pos), next_pos_2, board.find_piece(next_pos_2),direction, location]

    def search_all_direction(self, location, jump_moves_in, board):
        '''
        location: the location of selected piece
        jump_moves_in: Because the following jump is related to the previous jump (KING could not jump back), so we
                        put in the previous jump
        board: instance of board

        This function will return the potential basic moves or jump moves
        based moves willbe a dictionary of arriving location, e.g. [{1,2}, {1,4}]
        jump moves will be a dictionary of several things
        e.g.[{'cap pos': [(2, 4)], 'cap piece': [<Piece.Piece object at 0x000001EBC8A82160>], 'arr pos': (1, 5), 'dir': 'NE'},
        {'cap pos': [(2, 2)], 'cap piece': [<Piece.Piece object at 0x000001EBC8A82100>], 'arr pos': (1, 1), 'dir': 'NW'}]
        the explanation can be seen below
        '''
        adjacence = []
        basic_moves_out = []
        jump_moves_out = []

        # decide which direction to search, black and white are different
        if self.color == 'BLACK':
            if jump_moves_in is None or jump_moves_in['dir'] != 'NW':
                adjacence.append(self.search_one_direction(location,'SE', board))
            if jump_moves_in is None or jump_moves_in['dir'] != 'NE':
                adjacence.append(self.search_one_direction(location,'SW', board))
        elif self.color == 'WHITE':
            if jump_moves_in is None or jump_moves_in['dir'] != 'SW':
                adjacence.append(self.search_one_direction(location,'NE', board))
            if jump_moves_in is None or jump_moves_in['dir'] != 'SE':
                adjacence.append(self.search_one_direction(location,'NW', board))

        # decide which direction to search, king is different
        if self.rank == 'KING':
            if self.color == 'BLACK':
                if jump_moves_in is None or jump_moves_in['dir'] != 'SW':
                    adjacence.append(self.search_one_direction(location,'NE', board))
                if jump_moves_in is None or jump_moves_in['dir'] != 'SE':
                    adjacence.append(self.search_one_direction(location,'NW', board))
            elif self.color == 'WHITE':
                if jump_moves_in is None or jump_moves_in['dir'] !='NW':
                    adjacence.append(self.search_one_direction(location,'SE', board))
                if jump_moves_in is None or jump_moves_in['dir'] != 'NE':
                    adjacence.append(self.search_one_direction(location,'SW', board))


        # adjacence will be a list of list, the format of list is like the output of search_one_direction
        for adj in adjacence:
            if board.valid_location(adj[0]):
                basic_moves_out_one = {'arr pos': None}
                # arr pos is the arriving position, which is the adjacenced position

                if adj[1]==None:
                    basic_moves_out_one['arr pos'] = adj[0]
                    basic_moves_out.append(basic_moves_out_one)

                elif board.valid_location(adj[2]):

                    if (adj[1].get_color() != self.color) & (adj[3] == None):

                        if jump_moves_in is not None:
                            jump_moves_out_one = jump_moves_in.copy()
                            jump_moves_out_one['cap pos'] = jump_moves_in['cap pos'].copy()
                            jump_moves_out_one['cap piece'] = jump_moves_in['cap piece'].copy()

                        else:
                            jump_moves_out_one = {'cap pos': [], 'cap piece': [], 'arr pos': None, 'dir': None}
                            # cap pos: captured position
                            # cap piece: captured piece
                            # arr pos: arriving position: the position that will jump to
                            # dir: the dir that will jump to


                        jump_moves_out_one['cap pos'].append(adj[0]) # position that is captured
                        jump_moves_out_one['cap piece'].append(adj[1]) # piece that is captured

                        jump_moves_out_one['arr pos']= adj[2]  # arriving position
                        jump_moves_out_one['dir']= adj[4] # direction
                        jump_moves_out.append(jump_moves_out_one)


        return basic_moves_out, jump_moves_out

    def search_double_jump(self, jump_moves_in, board):
        """
        jump_moves_in is previous jump move (jump move is represented as a list of dictionaries as before)
        this function wil return a list of dictionaries that can show all potential moves incluing double moves
        """
        all_jumps = []
        fail_count = 0

        for jump_in in jump_moves_in:
            _, jump_moves_out = self.search_all_direction(jump_in['arr pos'], jump_in, board)
            if jump_moves_out == []:
                jump_moves_out = [jump_in]
                fail_count +=1
            all_jumps.extend(jump_moves_out)

        if fail_count == len(jump_moves_in):
            return all_jumps
        else:
            return self.search_double_jump(all_jumps, board)

    def search_move(self, board):

        # first get basic move and jump moves
        basic_moves, jump_moves = self.search_all_direction(self.location, None, board)

        #based on jump moves, get all double jumps
        all_jumps = []
        if jump_moves:
            all_jumps = self.search_double_jump(jump_moves, board)
        # if there is double jumps, can only keep double jump
        if all_jumps:
            return 'jump moves', all_jumps
        elif jump_moves:
            return 'jump moves', jump_moves
        elif basic_moves:
            return 'basic moves', basic_moves
        else:
            return 'That piece cannot move'






