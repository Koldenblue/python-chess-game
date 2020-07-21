class Piece:
    def __init__(self, black=True):
        '''A chess piece. black is a bool corresponding to the color of the piece.'''
        self.black = black

    # Possible functions: piece count tracking
    # captured piece tracking

    def get_end_locations(self, piece_obj, start_column, start_row, end_location_array, board_array):
        '''A function that returns an array of all valid movement locations for a given piece.'''
        possible_moves = []
        for location in end_location_array:
            valid_move = piece_obj.validate_move(start_column, start_row, location[0], location[1], board_array)
            if valid_move:
                possible_moves.append(location)
        return possible_moves
