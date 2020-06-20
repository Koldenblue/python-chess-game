from Rook_class import Rook
from NullPiece_class import NullPiece

class Piece:
    def __init__(self, black, identity, position):
        ''' black is a bool. identity can be the class of the piece. 
        position is a Position(column, row) object.'''
        self.black = black
        self.identity = identity
        self.position = position
        
    def check_move(self, end_posn):
        '''Determines if rook movement from a start location to an end location is valid.
            end_posn is a position object corresponding to the target movement location for the rook.'''
        # if self.identity == rook:
        start_column = self.Position.column
        start_row = self.Position.row
        valid_end_check = False
        # If the rook does not move, return False.
        if start_column == end_posn.column and start_row == end_posn.row:
            return valid_end_check
        if start_column == end_posn.column or start_row == end_posn.row:
            valid_end_check = True
        return valid_end_check
