from Piece_class import Piece

class NullPiece (Piece):
    '''Represents an empty space.'''
    def __init__(self):
        self.symbol = '  '
        self.black = None

    def validate_move(self, start_column, start_row, end_column, end_row, board_array):
        '''Represents that NullPiece()s have no movement. Function is  available but currently unused.'''
        return False