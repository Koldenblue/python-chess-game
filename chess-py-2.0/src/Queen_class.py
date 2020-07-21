from Piece_class import Piece

class Queen(Piece):

    def __init__(self, black):
        Piece.__init__(self, black)
        if self.black:
            self.symbol = 'bQ'
        else:
            self.symbol = 'wQ'

    def validate_move(self, start_column, start_row, end_column, end_row, board_array):
        ''' Returns True if movement of a queen is valid.'''
        valid_end_check = False
        # An alternative way to do this would be to make a list of all valid spaces to move to, 
        # and then compare the target movement space against the list.
        # But that would likely take longer to compute.

        # If no movement is made, return false.
        if start_column == end_column and start_row == end_row:
            return valid_end_check
            
        if start_column == end_column:
            traveled_spaces = end_row - start_row
            # negative will either equal 1 or -1, depending on whether the queen moves up or down.
            negative = int(traveled_spaces / abs(traveled_spaces))
            # So if end_row < start row, then decrement i. Else increment i.
            for i in range(start_row + negative, end_row + negative, negative):
                # if a space is occupied:
                if board_array[start_column][i].black != None:
                    # if not yet at the end space, return false
                    if board_array[start_column][i] != board_array[end_column][end_row]:
                        return valid_end_check
                    # if at the endspace, but the color is the same color as the queen, return false
                    if board_array[start_column][i].black == board_array[start_column][start_row].black:
                        return valid_end_check
                # if the endspace is reached, already checked earlier that it is empty. So return true:
                if board_array[start_column][i] == board_array[end_column][end_row]:
                    valid_end_check = True
                    return valid_end_check
            # if the for loop finishes without reaching the endspace, return false.
            return valid_end_check

        # Simalar to above, except for left and right instead of up and down
        if start_row == end_row:
            traveled_spaces = end_column - start_column
            negative = int(traveled_spaces / abs(traveled_spaces))
            # Decrement or increment i.
            for i in range(start_column + negative, end_column + negative, negative):
                # if a space is occupied:
                if board_array[i][start_row].black != None:
                    # if not yet at the end space, return false
                    if board_array[i][start_row] != board_array[end_column][end_row]:
                        return valid_end_check
                    # if at the endspace, but the color is the same color as the queen, return false
                    if board_array[i][start_row].black == board_array[start_column][start_row].black:
                        return valid_end_check
                # if the endspace is reached, already checked earlier that it is empty. So return true:
                if board_array[i][start_row] == board_array[end_column][end_row]:
                    valid_end_check = True
                    return valid_end_check
            # if the for loop finishes without reaching the endspace, return false.
            return valid_end_check
        return valid_end_check