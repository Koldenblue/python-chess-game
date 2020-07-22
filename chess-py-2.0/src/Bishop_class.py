from Piece_class import Piece

class Bishop(Piece):

    def __init__(self, black):
        Piece.__init__(self, black)
        if self.black:
            self.symbol = 'bB'
        else:
            self.symbol = 'wB'

    def validate_move(self, start_column, start_row, end_column, end_row, board_array):
        ''' Returns True if movement of a bishop is valid.'''
        valid_end_check = False

        # If no movement is made, return false.
        if start_column == end_column and start_row == end_row:
            return valid_end_check

        if Piece.diagonal_line_movement:
            return True

        return valid_end_check