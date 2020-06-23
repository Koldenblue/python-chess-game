from Rook_class import Rook
from NullPiece_class import NullPiece

class Piece:
    def __init__(self, black, identity):
        ''' black is a bool. identity is the class of the piece.'''
        self.black = black
        self.identity = identity

    def check_move(self, start_column, start_row, end_column, end_row, board_array):
        '''Determines if rook movement from a start location to an end location is valid.
            end_posn is a position object corresponding to the target movement location for the rook.'''
                # Find the starting piece object stored in space_array.
        
        valid_end_check = False

        if self.identity == Rook():
            valid_end_check = self.identity.check_rook_move(start_column, start_row, end_column, end_row, board_array, self.black)

        return valid_end_check