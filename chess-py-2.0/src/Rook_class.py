from Piece_class import Piece

class Rook (Piece):
    '''Defines movement associated with a rook.'''
    #TODO add in bool for can_castle, initially set to true, and becomes false after any movement.
    def __init__(self, black):
        Piece.__init__(self, black)
        if self.black:
            self.symbol = 'bR'
        else:
            self.symbol = 'wR'

    def validate_move(self, start_column, start_row, end_column, end_row, board_array):
        ''' Returns True if movement of a rook is valid.'''

        valid_end_check = False
        # If the rook does not move at all, return False:
        if start_column == end_column and start_row == end_row:
            return valid_end_check

        return Piece.straight_line_movement(start_column, start_row, end_column, end_row, board_array)