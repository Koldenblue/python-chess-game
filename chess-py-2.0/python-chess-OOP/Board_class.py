from Position_class import Position

class Board:
    def __init__(self, space_list = [], space_dict = {}):
        '''Creates a board object consisting of 64 named spaces, a1 thru h8, 
        corresponding to 64 Position objects, (0,0) thru (7,7).'''
        self.space_list = space_list
        self.space_dict = space_dict

        # Make space_list into a list of all spaces, a1 thru 8h.
        columns = tuple('abcdefgh')
        rows = tuple('12345678')
        for row in range(8):
            for column in range(8):
                space_list.append(columns[column] + rows[row])

        # Make space_dict a dictionary with spaces a1 thru h8 as keys, and Position objects (0,0) thru (7,7) as values.
        x = 0
        y = 0
        for space in space_list:
            space_dict[space] = Position(x, y)
            x += 1
            if x > 7:
                x = 0
                y += 1

    def visualBoard(self):
        '''A funtion to print out a graphic representation of a chessboard.'''
        print("\n")

    def space_points_ref(self):
        '''A funtion to print out which board spaces correspond to which position objects. Useful for reference only.'''
        print_counter = 0
        for space in self.space_dict.keys():
            print_counter += 1
            print("{0} == {1}".format(space, self.space_dict[space]), end='    ')
            # Print out 8 objects per line:
            if print_counter > 7:
                print("\n")
                print_counter = 0


chessboard = Board()
chessboard.space_points_ref()
#print(chessboard.space_list)
#print("\n", chessboard.space_dict, "\n")
#print(chessboard.space_dict['a1'])
