from Position_class import Position
from Rook_class import Rook
from Piece_class import Piece
from NullPiece_class import NullPiece
from King_class import King
from Pawn_class import Pawn
import copy

class Board:
    '''Board keeps track of spaces, and the pieces on those spaces.'''
    columns = tuple('abcdefgh')
    rows = tuple('12345678')
    MAX_ROW = 7
    MAX_COLUMN = 7
    BOARD_SIZE = 8


    def __init__(self, space_list = [], space_dict = {}, space_array = []):
        '''Creates a board object consisting of 64 named spaces, a1 thru h8, 
        corresponding to 64 Position objects, (0,0) thru (7,7).'''
        self.space_list = space_list
        self.space_dict = space_dict
        self.space_array = space_array

        # Create space_list. space_list is a list of all spaces, a1 thru 8h.
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                space_list.append(self.columns[column] + self.rows[row])

        # Create space_dict. space_dict is a dictionary with spaces a1 thru h8 as keys, 
        # and Position objects (0,0) thru (7,7) as values.
        x = 0
        y = 0
        for space in space_list:
            space_dict[space] = Position(x, y)
            x += 1
            if x > self.MAX_COLUMN:
                x = 0
                y += 1

        # Create space_array. space_array is a 2d array of length [8][8].
        # The array indices correspond to the 64 board spaces. 
        # Outer array (first array) is columns. Inner array is rows.
        for column in range(self.BOARD_SIZE):
            row_list = []
            for row in range(self.BOARD_SIZE):
                row_list.append(None)
            space_array.append(row_list)


    def get_indices(self, posn):
        '''Takes input positions in the format "a1" thru "h8".
        Returns indices for the column and row, which correspond to board_array indices.'''
        # Input position will be in format 'a1' etc.
        posn = posn.lower()

        # Use space_dict to translate format to column 0-7 and row 0-7, 
        # since space_dict contains Position(x, y) objects.
        column = self.space_dict[posn].column
        row = self.space_dict[posn].row
        return column, row


    def move(self, start_posn, end_posn):
        '''A function that gets the piece at the start location. 
        It then calls the move function to check if movement is valid.
        Finally, if movement is valid, it moves the piece.'''

        start_column, start_row = self.get_indices(start_posn)
        end_column, end_row = self.get_indices(end_posn)

        # Get the piece object at the start location
        starting_piece = self.space_array[start_column][start_row]
        if starting_piece == NullPiece():
            return False
        # Run the check move function, which depends on the identity of the piece.
        valid_end_check = starting_piece.validate_move(start_column, start_row, end_column, end_row, self.space_array)

        # If movement is valid, move the piece.
        # TODO: print out when piece has been captured.
        # TODO: Separate movement and validity checking into two functions?
        if valid_end_check:
            self.space_array[start_column][start_row] = NullPiece()
            self.space_array[end_column][end_row] = starting_piece
            self.visual_board()
            return True
        else:
            self.visual_board()
            return False

    def eval_check(self):
        print("*" * 100)
        board_copy = self.space_array
        for column in board_copy:
            if self.bK in column:
                print(print(column))


    def visual_board(self):
        '''Prints out a graphic representation of a chessboard.'''

        #Print out column letters:
        print("\n")
        print("   ", end="")
        for i in range(self.BOARD_SIZE):
            print(self.columns[i].center(7), end=" ")

        # Print out line at top.
        print("\n" + "  _" + "_" * (8 * 8))
        # print("  " + "|       " * 8 + "|")     # Enable this line to add one more empty space line at the top

        # Print out row number. self.rows is printed out starting from the end, hence rows[-(i+1)]
        for i in range(self.BOARD_SIZE):
            print(self.rows[-(i + 1)], end=" ")

            # Print out each space. Print the row numbers again after 8 spaces.
            # Print the symbols for each pieces. Printing starts at top, Positions(0,7) thru (7,7), and ends at bottom, Position(0,0) thru (7,0).
            for j in range(self.BOARD_SIZE):
                print("|  " + self.space_array[j][-(i - self.MAX_ROW)].symbol + "   ", end='')

            # Print out the row number again at the end of the line.
            print("| " + self.rows[-(i + 1)] + "\n" + "  ", end="") 

            # Print out the horizontal lines between rows.
            for k in range(self.BOARD_SIZE):
                if i < 7:
                    # can possibly change underscore "_" to "-" here:
                    print("|" + "_" * 7, end="")
                else:
                    print("|" + "_" * 7, end="")

            # Print the right end of the board. Go to the next line.
            print("|" + "\n", end="") 

        #Print out column letters again:
        print("   ", end="")
        for i in range(self.BOARD_SIZE):
            print(self.columns[i].center(7), end=" ")
        print("")


    def board_init(self):
        '''Initializes the board state for a new game.'''
        # Reset space_array to None:
        for column in range(self.BOARD_SIZE):
            for row in range(self.BOARD_SIZE):
                self.space_array[column][row] = None

        # Initialize piece locations.
        self.space_array[0][7] = Rook(True)     # a8
        self.space_array[7][7] = Rook(True)     # h8
        self.space_array[0][0] = Rook(False)    # a1
        self.space_array[7][0] = Rook(False)    # h1
        self.bK = copy.deepcopy(King(True))
        self.space_array[4][7] = self.bK     # e8
        self.space_array[4][0] = King(False)    # e1
        # black pawns, a7 through h7:
        for i in range(self.BOARD_SIZE):
            self.space_array[i][6] = Pawn(True)
        # white pawns, a2 through h2:
        for j in range(self.BOARD_SIZE):
            self.space_array[j][1] = Pawn(False)

        #TODO: Initialize other pieces.

        for i in range(len(self.space_array)):
            for j in range(len(self.space_array[i])):
                if self.space_array[i][j] == None:
                    self.space_array[i][j] = NullPiece()



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


