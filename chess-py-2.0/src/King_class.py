from Piece_class import Piece

class King (Piece):
    '''Movement, check, checkmate, and castling rules for a King Piece.'''

    def __init__(self, black):
        '''Constructor for a King Piece. King always starts out of check.'''
        Piece.__init__(self, black)
        self.in_check = False
        if self.black:
            self.symbol = 'bK'
        else:
            self.symbol = 'wK'


    def eval_check(self, king_column, king_row, board_array):
        '''Evaluates whether or not a king is in check. Returns True if king is placed in check. Should be called after any movement.'''
        # Code for a black King. Color is checked at top of function so that it only has to be checked once.
        checks_king = False
        # Iterate over the column and row indices.
        for column, piece_list in enumerate(board_array):
            for row in range(len(piece_list)):
                # Use the column and row indices to determine if an enemy piece is at that location.
                # If enemy piece is present, determine if it can move to the given king location.
                if board_array[column][row].black != self.black:
                    checks_king = board_array[column][row].validate_move(column, row, king_column, king_row, board_array)
                    if checks_king:
                        return checks_king
        return checks_king


    def validate_move(self, start_column, start_row, end_column, end_row, board_array):
        '''Validates movement for a king piece.'''
        valid_end_check = False
        # Check to make sure the target space isn't already occupied by a friendly piece
        if board_array[end_column][end_row].black == self.black:
            return valid_end_check
        # if the king only moves one space, the move is valid:
        if abs(end_row - start_row) == 1:
            if abs(end_column - start_column) in [0, 1]:
                valid_end_check = True
        if abs(end_column - start_column) == 1:
            if abs(end_row - start_row) in [0, 1]:
                valid_end_check = True
        # Check to make sure the target space isn't already occupied by a friendly piece
        return valid_end_check