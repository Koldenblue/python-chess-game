from Position_class import Position
from Rook_class import Rook
from Piece_class import Piece
from NullPiece_class import NullPiece
from King_class import King
from Pawn_class import Pawn
import copy

class Board:
    '''Board keeps track of spaces, and the pieces on those spaces.'''
    columns = 'abcdefgh'
    rows = '12345678'
    BOARD_SIZE = 8
    MAX_ROW = BOARD_SIZE - 1
    MAX_COLUMN = BOARD_SIZE - 1

    def __init__(self):
        '''Creates a board object consisting of 64 named spaces, a1 thru h8, 
        corresponding to 64 Position objects, (0,0) thru (7,7).'''
        self.location_array = []
        self.space_dict = {}
        self.space_array = []
        self.space_list = []

        # Create space_list, then convert to tuple. space_list contains all spaces, a1 thru 8h.
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                self.space_list.append(self.columns[column] + self.rows[row])
        self.space_list = tuple(self.space_list)

        # Create space_dict. space_dict is a dictionary with spaces a1 thru h8 as keys, 
        # and Position objects (0,0) thru (7,7) as values.
        x = 0
        y = 0
        for space in self.space_list:
            self.space_dict[space] = Position(x, y)
            x += 1
            if x > self.MAX_COLUMN:
                x = 0
                y += 1

        # Create space_array. space_array is a 2d array of length [8][8].
        # The array will contain Piece objects.
        # The array indices correspond to the 64 board spaces. 
        # Outer array (first array) is columns. Inner array is rows.
        for column in range(self.BOARD_SIZE):
            row_list = []
            for row in range(self.BOARD_SIZE):
                row_list.append(None)
            self.space_array.append(row_list)

        # Create location_array. It is an array of lists of length 2, where location_array[i][0] is
        # the column index and location_array[i][1] is the row index.
        for posn in self.space_list:
            test_posn = self.get_indices(posn)
            self.location_array.append(test_posn)
        self.location_array = tuple(self.location_array)


    def get_indices(self, posn):
        '''Takes input positions, where 'posn' is in the format "a1" thru "h8".
        Returns indices for the column and row, which correspond to board_array indices.'''
        # Use space_dict to translate from 'a1-h8' format to column 0-7 and row 0-7, 
        # since space_dict contains Position(x, y) objects.
        column = self.space_dict[posn].column
        row = self.space_dict[posn].row
        return column, row


    def validate_move(self, start_column, start_row, end_column, end_row):
        '''A function that gets the piece at the start location.
        It then calls the move function to check if movement is valid.'''
        # Get the piece object at the start location
        starting_piece = self.space_array[start_column][start_row]
        if starting_piece == NullPiece():
            return False
        # Run the check move function, which depends on the identity of the piece.
        valid_end_check = starting_piece.validate_move(start_column, start_row, end_column, end_row, self.space_array)
        return valid_end_check


    def get_king_locations(self, board_array):
        found_bK = False
        found_wK = False
        for column, column_list in enumerate(board_array):
            for row in range(len(column_list)):
                if board_array[column][row].symbol == 'bK':
                    found_bK = True
                    bK_position = Position(column, row)
                elif board_array[column][row].symbol == 'wK':
                    found_wK = True
                    wK_position = Position(column, row)
            if found_bK and found_wK:
                break
        # Careful that bK is returned first, and wK second!
        return bK_position, wK_position


    def checks_kings(self, start_column, start_row, end_column, end_row):
        '''Returns king objects with the king.in_check property set to True or False, based on the 
        proposed move in the arguments.'''
        # First make the movement on a copy of the board.
        board_copy = self.move_mirror(start_column, start_row, end_column, end_row)

        bK = King(True)
        wK = King(False)
        assert(wK.in_check == False)
        assert(bK.in_check == False)
        # Next search the board copy for the king locations.
        bK_position, wK_position = self.get_king_locations(board_copy)
        # Once the kings have been found, evaluate whether they are placed in check.
        bK.in_check = bK.eval_check(bK_position.column, bK_position.row, board_copy)
        wK.in_check = wK.eval_check(wK_position.column, wK_position.row, board_copy)
        # Careful that bK is returned first, and wK second!
        return bK, wK


    def checkmates_king(self, black_turn):
        '''Gets location of a king in check. Checks if a king is in checkmate. black_turn is a boolean.'''
        # This function is called at the beginning of the turn, before movement can be entered.
        # Thus it should find checkmate status for the current player.
        # To do this, find if any possible movement by the current player results in a non-check state.

        # psuedocode: for each friendly piece, get a list of possible movement locations.
        # Next, use move-mirror to move the piece to each possible location.
        # Then check if the king is still in check.
        # Repeat until all moves are exhausted, or a possible movement is found.
        # Possibility: movement hint. Like mahjong? At least print out 'movement possible'.

        checkmate = True
        # Iterate over the column and row indices.
        for column, piece_list in enumerate(self.space_array):
            for row, piece_obj in enumerate(piece_list):
                # Get friendly pieces to test movement
                if piece_obj.black == black_turn:
                    # Get all valid movement locations.
                    possible_moves = piece_obj.get_end_locations(piece_obj, column, row, self.location_array, self.space_array)
                    # use move_mirror to find if any locations in possible_moves prevent checkmate.
                    # If the friendly piece is not a moving king, get the king locations.
                    if piece_obj.symbol != 'bK' and piece_obj.symbol != 'wK':
                        bK_position, wK_position = self.get_king_locations(self.space_array)
                        if black_turn:
                            king_column = bK_position.column
                            king_row = bK_position.row
                            king = King(True)
                        else:
                            king_column = wK_position.column
                            king_row = wK_position.row
                            king = King(False)
                        for end_location in possible_moves:
                            board_copy = self.move_mirror(column, row, end_location[0], end_location[1])
                            in_check = king.eval_check(king_column, king_row, board_copy)
                            if not in_check:
                                checkmate = False
                                break
                    # If the piece is a king:
                    else:
                        king = King(black_turn)
                        # get possible moves that king can make, then find if king is still in check.
                        for end_location in possible_moves:
                            board_copy = self.move_mirror(column, row, end_location[0], end_location[1])
                            in_check = king.eval_check(end_location[0], end_location[1], board_copy)
                            if not in_check:
                                checkmate = False
                                break
                if not checkmate:
                    break
            if not checkmate:
                break
        return checkmate


    def move(self, start_column, start_row, end_column, end_row):
        '''Moves a piece on the board. Prints when pieces have been captured.
        Prints out the new board state.'''
        starting_piece = self.space_array[start_column][start_row]
        self.space_array[start_column][start_row] = NullPiece()
        if self.space_array[end_column][end_row].black != None:
            print("{0} has been captured!".format(self.space_array[end_column][end_row].symbol))
        self.space_array[end_column][end_row] = starting_piece



    def move_mirror(self, start_column, start_row, end_column, end_row):
        '''Moves a piece on a copy of the board array.'''
        # Add [:] to make a copy, rather than simply referencing the same array!
        board_copy = copy.deepcopy(self.space_array)
        starting_piece = board_copy[start_column][start_row]
        board_copy[start_column][start_row] = NullPiece()
        board_copy[end_column][end_row] = starting_piece
        return board_copy

    def visual_board(self):
        '''Prints out a graphic representation of a chessboard.'''
        '''Should be replaced by the __str__ method below.'''
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


    def __str__(self):
        '''Returns a string and defines print() pertaining to printing out the chessboard.'''
        #Print out column letters:
        graphic = ''
        graphic += "\n"
        graphic += "   "
        for i in range(self.BOARD_SIZE):
            graphic += self.columns[i].center(7) + ' '

        # Print out line at top.
        graphic += "\n" + "  _" + "_" * (8 * 8) + '\n'
        # print("  " + "|       " * 8 + "|")     # Enable this line to add one more empty space line at the top

        # Print out row number. self.rows is printed out starting from the end, hence rows[-(i+1)]
        for i in range(self.BOARD_SIZE):
            graphic += self.rows[-(i + 1)] + ' '

            # Print out each space. Print the row numbers again after 8 spaces.
            # Print the symbols for each pieces. Printing starts at top, Positions(0,7) thru (7,7), and ends at bottom, Position(0,0) thru (7,0).
            for j in range(self.BOARD_SIZE):
                graphic += "|  " + self.space_array[j][-(i - self.MAX_ROW)].symbol + "   "

            # Print out the row number again at the end of the line.
            graphic += "| " + self.rows[-(i + 1)] + "\n" + "  "

            # Print out the horizontal lines between rows.
            for k in range(self.BOARD_SIZE):
                if i < 7:
                    # can possibly change underscore "_" to "-" here:
                    graphic += "|" + "_" * 7
                else:
                    graphic += "|" + "_" * 7

            # Print the right end of the board. Go to the next line.
            graphic += "|" + "\n" 

        #Print out column letters again:
        graphic += "   "
        for i in range(self.BOARD_SIZE):
            graphic += self.columns[i].center(7) + ' '
        graphic += "\n"
        return graphic


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
        self.space_array[4][7] = King(True)     # e8
        self.space_array[4][0] = King(False)    # e1
        # black pawns, a7 through h7:
        for i in range(self.BOARD_SIZE):
            self.space_array[i][6] = Pawn(True)
        # white pawns, a2 through h2:
        for j in range(self.BOARD_SIZE):
            self.space_array[j][1] = Pawn(False)

        #TODO: Initialize other pieces.

        # Finally, set empty spaces to contain NullPiece()s
        for i in range(len(self.space_array)):
            for j in range(len(self.space_array[i])):
                if self.space_array[i][j] == None:
                    self.space_array[i][j] = NullPiece()


    def space_points_ref(self):
        '''Prints out which board spaces correspond to which position objects. 
        No game purpose, for reference only.'''
        print_counter = 0
        # Create a new list in the proper order, a8 thru h8, a7 thru h7, etc. For easier reference.
        # space_list_ref is almost the same as self.space_list, but it is sorted differently.
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


    def test_init(self):
        '''Same as board_init, but initializes a custom board state for testing.'''
        # Reset space_array to None:
        for column in range(self.BOARD_SIZE):
            for row in range(self.BOARD_SIZE):
                self.space_array[column][row] = None

        # Initialize piece locations.
        #self.space_array[0][7] = Rook(True)
        self.space_array[3][6] = Rook(True)
        self.space_array[0][7] = Rook(False)
        self.space_array[0][5] = Rook(False)
        self.space_array[7][0] = Rook(False)
        self.space_array[4][7] = King(True)
        self.space_array[4][0] = King(False)
        # black pawns, a7 through h7:
        #for i in range(self.BOARD_SIZE):
        #    self.space_array[i][6] = Pawn(True)
        # white pawns, a2 through h2:
        for j in range(self.BOARD_SIZE):
            self.space_array[j][1] = Pawn(False)

        #TODO: Initialize other pieces.

        # Finally, set empty spaces to contain NullPiece()s
        for i in range(len(self.space_array)):
            for j in range(len(self.space_array[i])):
                if self.space_array[i][j] == None:
                    self.space_array[i][j] = NullPiece()