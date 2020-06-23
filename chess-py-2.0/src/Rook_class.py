from Piece_class import Piece

class Rook (Piece):
    '''Defines movement associated with a rook.'''
    def __init__(self, black):
        Piece.__init__(self, black)
        if self.black:
            self.symbol = 'bR'
        else:
            self.symbol = 'wR'

    def check_move(self, start_column, start_row, end_column, end_row, board_array):
        ''' Returns True if movement of a rook is valid.'''
        valid_end_check = False
        # If the rook does not move at all, return False:
        if start_column == end_column and start_row == end_row:
            return valid_end_check

        # The rook must stay in either the same column or row (ie. move in a straight line).
        # If not, return False.
        elif start_column != end_column and start_row != end_row:
            return valid_end_check

        # If row or column is same, check that in between spaces are empty (contain a NullPiece)
        elif start_column == end_column:
            # interval == 1 if end_row is greater than start_row, else interval == -1
            interval = int(abs(end_row - start_row) / (end_row - start_row))
            for i in range(start_row + interval, end_row, interval):
                if board_array[start_column][i].black != None:
                    return valid_end_check
            # Check that the end location has an opposite color piece, or a NullPiece.
            if board_array[end_column][end_row].black == board_array[start_column][start_row].black:
                return valid_end_check
            valid_end_check = True
            return valid_end_check

        elif start_row == end_row:
            # interval == 1 if end greater than start, else interval == -1
            interval = int(abs(end_column - start_column) / (end_column - start_column))
            for i in range(start_column + interval, end_column, interval):
                if board_array[i][start_row].black != None:
                    return valid_end_check
            # Check that the end location has an opposite color piece, or a NullPiece.
            if board_array[end_column][end_row].black == board_array[start_column][start_row].black:
                return valid_end_check
            valid_end_check = True
            return valid_end_check