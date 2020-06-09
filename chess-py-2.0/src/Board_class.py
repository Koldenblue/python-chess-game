from Position_class import Position
from Rook_class import Rook
from Piece_class import Piece


class Board:
    columns = tuple('abcdefgh')
    rows = tuple('12345678')

    def __init__(self, space_list = [], space_dict = {}):
        '''Creates a board object consisting of 64 named spaces, a1 thru h8, 
        corresponding to 64 Position objects, (0,0) thru (7,7).'''
        self.space_list = space_list
        self.space_dict = space_dict

        # Make space_list into a list of all spaces, a1 thru 8h.
        for row in range(8):
            for column in range(8):
                space_list.append(self.columns[column] + self.rows[row])

        # Make space_dict a dictionary with spaces a1 thru h8 as keys, 
        # and Position objects (0,0) thru (7,7) as values.
        x = 0
        y = 0
        for space in space_list:
            space_dict[space] = Position(x, y)
            x += 1
            if x > 7:
                x = 0
                y += 1

    def visual_board(self):
        '''A funtion to print out a graphic representation of a chessboard.'''
        print("\n")
        print("   ", end="")
        for i in range(8):
            print(self.columns[i].center(7), end=" ")
        print("\n" + "  _" + "_" * (8*8))
        #print("  " + "|       " * 8 + "|")      # Adds one more empty space line at the top
        for i in range(8):
            print(self.rows[i], end=" ")
            for j in range(8):
                print("|", end=(" " * 7))
            print("|" + "\n" + "  ", end="") 
            for k in range(8):
                if i < 7:
                    # can possibly change underscore "_" to "-" here:
                    print("|" + "_" * 7, end="")
                else:
                    print("|" + "_" * 7, end="")
            print("|" + "\n", end="") 


    def space_points_ref(self):
        '''A funtion to print out which board spaces correspond to which position objects. Useful for reference only.'''
        print_counter = 0
        for space in self.space_dict.keys():
            print_counter += 1
            print("{0} == {1}".format(space, self.space_dict[space]), end='    ')
            # Print out 8 objects per line:
            if print_counter > 7:
                print("\n")
                print_counter = 0


    def board_init(self):
        bR1 = Rook(Piece(True, 'rook', Position(0,0)))
        bR2 = Rook(Piece(True, 'rook', Position(7,0)))
        wR1 = Rook(Piece(False, 'rook', Position(0,7)))
        wR2 = Rook(Piece(False, 'rook', Position(7,7)))
        return bR1, bR2, wR1, wR2






#print(chessboard.space_list)
#print("\n", chessboard.space_dict, "\n")
#print(chessboard.space_dict['a1'])
