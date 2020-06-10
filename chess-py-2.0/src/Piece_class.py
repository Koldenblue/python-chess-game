class Piece:
    def __init__(self, black, identity, position):
        ''' black is a bool. identity is the name of the piece. 
        position is a Position(column, row) object.'''
        self.black = black
        self.identity = identity
        self.position = position

