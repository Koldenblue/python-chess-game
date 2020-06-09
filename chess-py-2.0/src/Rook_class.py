from Piece_class import Piece
from Position_class import Position

class Rook:
    '''Defines movement associated with a rook'''

    def __init__(self, piece):
        '''This is a piece object, with three attributes. First is black = true/false.
            Second is piece identity. Third is a Position(column, row) object.'''
        self.piece = Piece(True, 'rook', Position(0,0))

    def rook_move(self, end_posn):
        '''Determines if rook movement from a start location to an end location is valid.
            end_posn is a position object corresponding to the target movement location for the rook.'''
        start_column = self.piece.position.column
        start_row = self.piece.position.row
        valid_end_check = False
        # If the rook does not move, return False.
        if start_column == end_posn.column and start_row == end_posn.row:
            return valid_end_check
        if start_column == end_posn.column or start_row == end_posn.row:
            valid_end_check = True
        return valid_end_check
