from Position_class import Position
from Rook_class import Rook
from Piece_class import Piece


class Board:
    columns = tuple('abcdefgh')
    rows = tuple('12345678')

    def __init__(self, space_list = [], space_dict = {}, space_array = []):
        '''Creates a board object consisting of 64 named spaces, a1 thru h8, 
        corresponding to 64 Position objects, (0,0) thru (7,7).'''
        self.space_list = space_list
        self.space_dict = space_dict
        self.space_array = space_array

        # Create space_list. space_list is a list of all spaces, a1 thru 8h.
        for row in range(8):
            for column in range(8):
                space_list.append(self.columns[column] + self.rows[row])

        # Create space_dict. space_dict is a dictionary with spaces a1 thru h8 as keys, 
        # and Position objects (0,0) thru (7,7) as values.
        x = 0
        y = 0
        for space in space_list:
            space_dict[space] = Position(x, y)
            x += 1
            if x > 7:
                x = 0
                y += 1
        
        # Create space_array. space_array is a 2d array of max size space_array[7][7].
        # The array indices correspond to the 64 board spaces. 
        # Outer array (first array) is columns. Inner array is rows.
        for column in range(8):
            row_list = []
            for row in range(8):
                row_list.append(None)
            space_array.append(row_list)

    def visual_board(self):
        '''Prints out a graphic representation of a chessboard.'''
        print("\n")
        print("   ", end="")
        for i in range(8):
            print(self.columns[i].center(7), end=" ")
        print("\n" + "  _" + "_" * (8*8))
        #print("  " + "|       " * 8 + "|")     # Enable to add one more empty space line at the top
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
        '''Prints out which board spaces correspond to which position objects. 
        For reference only.'''
        print_counter = 0
        for space in self.space_dict.keys():
            print_counter += 1
            print("{0} == {1}".format(space, self.space_dict[space]), end='    ')
            # Print out 8 objects per line:
            if print_counter > 7:
                print("\n")
                print_counter = 0


    def board_init(self):
        # Overlap: the piece object has a position, but the board also keeps track of pieces in an array?
        bR1 = Piece(True, Rook(), Position(0,0))
        self.space_array[0][0] = bR1
        bR2 = Piece(True, Rook(), Position(7,0))
        self.space_array[7][0] = bR2
        wR1 = Piece(False, Rook(), Position(0,7))
        wR2 = Piece(False, Rook(), Position(7,7))
        return bR1, bR2, wR1, wR2




