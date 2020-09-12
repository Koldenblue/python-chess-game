from Piece_class import Piece

class Knight (Piece):

    def __init__(self, black):
        '''Constructs a Knight piece with a color and associated movement functions.'''
        Piece.__init__(self, black)
        if self.black:
            self.symbol = 'bN'
        else:
            self.symbol = 'wN'

    def validate_move(self, start_column, start_row, end_column, end_row, board_array):
        '''Returns true if knight movement is valid.'''
        # Knights can move one column then two rows, two columns then one row, 
        # one row then two columns, or two rows then one column.
        # Also make sure end space is not occupied by piece of same color
        if abs(start_column - end_column) == 1 and abs(start_row - end_row) == 2:
            if board_array[start_column][start_row].black != board_array[end_column][end_row].black:
                return True
        if abs(start_column - end_column) == 2 and abs(start_row - end_row) == 1:
            if board_array[start_column][start_row].black != board_array[end_column][end_row].black:
                return True
        return False