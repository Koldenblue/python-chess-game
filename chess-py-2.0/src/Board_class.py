from Position_class import Position
from Rook_class import Rook
from Piece_class import Piece
from NullPiece_class import NullPiece

class Board:
    columns = tuple('abcdefgh')
    rows = tuple('12345678')
    MAX_ROW = 7
    MAX_COLUMN = 7

    def __init__(self, space_list = [], space_dict = {}, space_array = [], piece_dict = {}):
        '''Creates a board object consisting of 64 named spaces, a1 thru h8, 
        corresponding to 64 Position objects, (0,0) thru (7,7).'''
        self.space_list = space_list
        self.space_dict = space_dict
        self.space_array = space_array
        self.piece_dict = piece_dict

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

        for space in space_list:
            piece_dict[space] = NullPiece()

    def board_init(self):
        # Overlap: the piece object has a position, but the board also keeps track of pieces in an array?
        bR1 = Piece(True, Rook(), Position(0, 7))
        self.space_array[0][7] = bR1
        self.piece_dict['a8'] = bR1

        bR2 = Piece(True, Rook(), Position(7, 7))
        self.space_array[7][7] = bR2
        self.piece_dict['h8'] = bR2

        wR1 = Piece(False, Rook(), Position(0, 0))
        self.space_array[0][0] = wR1
        self.piece_dict['a1'] = wR1

        wR2 = Piece(False, Rook(), Position(7, 0))
        self.space_array[7][0] = wR2
        self.piece_dict['h1'] = wR2
        
        return bR1, bR2, wR1, wR2


    def visual_board(self):
        '''Prints out a graphic representation of a chessboard.'''

        #Print out column letters:
        print("\n")
        print("   ", end="")
        for i in range(8):
            print(self.columns[i].center(7), end=" ")

        # Print out line at top.
        print("\n" + "  _" + "_" * (8*8))
        #print("  " + "|       " * 8 + "|")     # Enable this line to add one more empty space line at the top

        # Print out row number.
        for i in range(8):
            print(self.rows[-(i+1)], end=" ")

            # Print out each space. Print the row numbers again after 8 spaces.
            for j in range(8):
                print("|", end=(" " * 7))
            print("| " + self.rows[-(i+1)] + "\n" + "  ", end="") 

            # Print out the horizontal lines between rows.
            for k in range(8):
                if i < 7:
                    # can possibly change underscore "_" to "-" here:
                    print("|" + "_" * 7, end="")
                else:
                    print("|" + "_" * 7, end="")

            # Print the right end of the board. Go to the next line.
            print("|" + "\n", end="") 

        #Print out column letters again:
        print("   ", end="")
        for i in range(8):
            print(self.columns[i].center(7), end=" ")


    def space_points_ref(self):
        '''Prints out which board spaces correspond to which position objects. 
        No game purpose, for reference only.'''
        print_counter = 0
        # Create a new list in the proper order, a8 thru h8, a7 thru h7, etc. For easier reference. 
        space_list_ref = []
        for i in range(8, 0, -1):
            for j in range(8):
                space_list_ref.append(self.columns[j] + str(i))
        for space in space_list_ref:
            print_counter += 1
            print("{0} == {1}".format(space, self.space_dict[space]), end='    ')
            # Print out 8 objects per line:
            if print_counter > 7:
                print("\n")
                print_counter = 0

