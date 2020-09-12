from datetime import datetime

class Piece:
    COLOR_BLACK = 'red'
    COLOR_WHITE = 'cyan'

    def __init__(self, black=True):
        '''A chess piece. black is a bool corresponding to the color of the piece.'''
        self.black = black

    def get_end_locations(self, piece_obj, start_column, start_row, end_location_array, board_array):
        '''A function that returns an array of all valid movement locations for a given piece.'''
        possible_moves = []
        for location in end_location_array:
            valid_move = piece_obj.validate_move(start_column, start_row, location[0], location[1], board_array)
            if valid_move:
                possible_moves.append(location)
        return possible_moves

    def straight_line_movement(self, start_column, start_row, end_column, end_row, board_array):
        '''Returns true if movement in a straight line is valid. Useful for rooks and queens. This function is 
        inherited for use by specific pieces.'''
        valid_end_check = False
        # If row or column is same, check that in between spaces are empty (contain a NullPiece)
        if start_column == end_column:
            # interval == 1 if end_row is greater than start_row, else interval == -1
            interval = int(abs(end_row - start_row) / (end_row - start_row))
            # If any space in between has a color, it is not empty, so return false.
            for i in range(start_row + interval, end_row, interval):
                if board_array[start_column][i].black != None:
                    return valid_end_check
            # Check that the end location has an opposite color piece, or a NullPiece.
            # Return false if the pieces are the same color.
            if board_array[end_column][end_row].black == board_array[start_column][start_row].black:
                return valid_end_check
            valid_end_check = True
            return valid_end_check

        # Same as above if statement, except for moving within a row.
        if start_row == end_row:
            interval = int(abs(end_column - start_column) / (end_column - start_column))
            for i in range(start_column + interval, end_column, interval):
                if board_array[i][start_row].black != None:
                    return valid_end_check
            if board_array[end_column][end_row].black == board_array[start_column][start_row].black:
                return valid_end_check
            valid_end_check = True
            return valid_end_check

        return valid_end_check


    def diagonal_line_movement(self, start_column, start_row, end_column, end_row, board_array):
        '''Returns true if movement in a diagonal line is valid. Useful for bishops and queens. 
        This function is inherited for use by specific pieces.'''
        valid_end_check = False
        if start_column == end_column or start_row == end_row:
            return valid_end_check

        # Get the number of columns moved. It should be equal to the number of rows moved.
        column_interval = int(abs(end_column - start_column))
        row_interval = int(abs(end_row - start_row))
        if column_interval != row_interval:
            return valid_end_check

        # 1 if end is greater than start, else -1
        negative_row = int(abs(end_row - start_row) / (end_row - start_row))
        negative_column = int(abs(end_column - start_column) / (end_column - start_column))
        # Find if the spaces between the start and end are occupied. If occupied, return false.
        for c in range(start_column + negative_column, end_column, negative_column):
            for r in range(start_row + negative_row, end_row, negative_row):
                if board_array[c][r].black != None:
                    return valid_end_check 

        # Make sure the end location is not occupied by a friendly piece.
        if board_array[end_column][end_row].black == board_array[start_column][start_row].black:
            return valid_end_check

        # if all the above conditions are passed, return true.
        return True

    # Possible functions: piece count tracking
    # captured piece tracking