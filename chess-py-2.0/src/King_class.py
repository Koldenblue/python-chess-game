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
        if self.black:
            # Iterate over the column and row indices.
            for column, piece_list in enumerate(board_array):
                for row in range(len(piece_list)):
                    # Use the column and row indices to determine if a white piece is at that location.
                    # If a white piece is present, determine if it can move to the given black king location.
                    if board_array[column][row].black == False:
                        checks_king = board_array[column][row].validate_move(column, row, king_column, king_row, board_array)
                        if checks_king:
                            return checks_king
            return checks_king

        # Code for a white King. Similar to black King code.
        if self.black == False:
            for column, piece_list in enumerate(board_array):
                for row in range(len(piece_list)):
                    if board_array[column][row].black == True:
                        checks_king = board_array[column][row].validate_move(column, row, king_column, king_row, board_array)
                        if checks_king:
                            return checks_king
            return checks_king


    def eval_checkmate(self, board_array, black_turn):
        '''If a king is in check, this function should be called, and will return true if checkmate.
        baord_array is the current board state. black_turn is a boolean.'''
        for column, column_list in enumerate(board_array):
            for row in range(len(column_list)):
                # If the piece belongs to the current player:
                # psuedocode: First check to see if the king can move.
                # Use the above eval_check function to see if the king is still in check.
                # Next loop through same color pieces and get possible movements.
                # Maybe create a new piece function to get an array of all possible movement locations?
                # Finally, loop through the possible movement locations and see if any cause eval_check to return false.
                # If not, checkmate.
                if board_array[column][row].black == black_turn:
                    can_move = board_array[column][row].validate_move()
                    still_checked = eval_check()
        return False


    def validate_move(self, start_column, start_row, end_column, end_row, board_array):
        #TODO
        valid_end_check = False
        return valid_end_check