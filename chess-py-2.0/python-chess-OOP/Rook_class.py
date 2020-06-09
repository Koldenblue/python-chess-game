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
            end is a position object corresponding to the target movement location for the rook.'''
        start_column = self.piece.position.column
        start_row = self.piece.position.row
        valid_end_check = False
        # If the rook does not move, return False.
        if start_column == end_posn.column and start_row == end_posn.row:
            return valid_end_check
        if start_column == end_posn.column or start_row == end_posn.row:
            valid_end_check = True
        return valid_end_check







"""
    def __init__(self, space, identity, white):
        '''space is a position object of format Position(x, y), where x corresponds to columns
            and y corresponds to rows.
            identity is the name of the piece.
            white is a bool that depends on the color of the piece.'''
        self.space = space
        self.identity = "rook"
        self.white = True

    def rook_move(self, end):
        '''Determines if rook movement from a start location to an end location is valid.
            end is a position object corresponding to the target movement location for the rook.'''
        start_column = self.space.column
        start_row = self.space.row
        valid_end_check = False
        if start_column == end.column or start_row == end.row:
            valid_end_check = True
        return valid_end_check

bR1 = Rook(Position(0,0), "rook", False)
bR2 = Rook(Position(7,0), "rook", False)
wR1 = Rook(Position(0,7), "rook", True)
wR2 = Rook(Position(7,7), "rook", True)

print(bR1.rook_move(Position(0,0)))
print(bR1.space.column)
"""