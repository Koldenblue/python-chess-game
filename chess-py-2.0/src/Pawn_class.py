from Piece_class import Piece

class Pawn (Piece):
    def __init__(self, black):
        Piece.__init__(self, black)
        if self.black:
            self.symbol = 'bp'
        else:
            self.symbol = 'wp'
    
    def validate_move(self, start_column, start_row, end_column, end_row, board_array):
        '''Returns true if movement of a pawn is valid.'''
        # Note that the given arguments for columns and rows are indices 0-7,
        # while chessboard notation of rows is 1-8!
        # This is where using Board.space_points_ref() is useful!
        valid_end_check = False
        # Pawn can only stay in the same column, or move one column over to capture a piece. 
        if abs(start_column - end_column) > 1:
            return valid_end_check

        if self.black:
            # black pawn can only move downwards (row must decrease)
            if end_row >= start_row:
                return valid_end_check
            # If black pawn is in starting row 6, it can move forward two spaces if those spaces are empty.
            if start_column == end_column:
                if start_row == 6:
                    if end_row == 5:
                        if board_array[end_column][end_row].black == None:
                            valid_end_check = True
                            return valid_end_check
                    if end_row == 4:
                        if board_array[end_column][end_row].black == None and board_array[end_column][end_row + 1] == None:
                            valid_end_check = True
                            return valid_end_check
                    return valid_end_check
                # If pawn has already moved, it can only move one space forward, and only if that space is empty.
                if start_row < 6:
                    if end_row != start_row - 1:
                        return valid_end_check
                    if board_array[end_column][end_row].black != None:
                        return valid_end_check
                    else:
                        valid_end_check = True
                        return valid_end_check
            # Black pawns can move diagonally, but only to capture white pieces.
            if abs(start_column - end_column) == 1:
                if end_row != start_row - 1:
                    return valid_end_check
                if board_array[end_column][end_row].black == False:
                    valid_end_check = True
                    return valid_end_check
                else:
                    return valid_end_check


        #TODO: white pawn
        if not self.black:
            # white pawn can only move upwards (row must increase)
            if end_row <= start_row:
                return valid_end_check

            # If white pawn is in starting row 1, it can move forward two spaces if those spaces are empty.
            if start_column == end_column:
                if start_row == 1:
                    if end_row == 2:
                        if board_array[end_column][end_row].black == None:
                            valid_end_check = True
                            return valid_end_check
                    if end_row == 3:
                        if board_array[end_column][end_row].black == None and board_array[end_column][end_row + 1] == None:
                            valid_end_check = True
                            return valid_end_check
                    return valid_end_check
                # If pawn has already moved, it can only move one space forward, and only if that space is empty.
                if start_row > 1:
                    if end_row != start_row + 1:
                        return valid_end_check
                    if board_array[end_column][end_row].black != None:
                        return valid_end_check
                    else:
                        valid_end_check = True
                        return valid_end_check
            # white pawns can move diagonally, but only to capture black pieces.
            if abs(start_column - end_column) == 1:
                if end_row != start_row + 1:
                    return valid_end_check
                if board_array[end_column][end_row].black:
                    valid_end_check = True
                    return valid_end_check
                else:
                    return valid_end_check