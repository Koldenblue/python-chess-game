class Piece:
    def __init__(self, black=True):
        '''A chess piece. black is a bool corresponding to the color of the piece.'''
        self.black = black

        # Possible functions: piece count tracking
        # captured piece tracking