class Rook:
    '''Defines movement associated with a rook.'''

    def __init__(self):
        '''This is a piece object.'''


    def check_rook_move(self, start_column, start_row, end_column, end_row, board_array, black):
        ''' Retruns True if movement of a rook is valid.'''
        valid_end_check = False
        # If the rook does not move at all, return False:
        if start_column == end_column and start_row == end_row:
            return valid_end_check

        # The rook must stay in either the same column or row (ie. move in a straight line).
        # If not, return False.
        if start_column != end_column and start_row != end_row:
            return valid_end_check

        


        return valid_end_check