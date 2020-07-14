class Position:
    def __init__(self, x, y):
        '''Defines a coordinate on the chessboard, where the x axis changes with columns, 
        and the y axis changes with rows.'''
        self.column = x 
        self.row = y
    
    def __str__(self):
        '''Allows the print command to be used to print out a Position in the format "(x, y)".'''
        return "({0}, {1})".format(self.column, self.row)

    def __eq__(self, pt2):
        '''Overloads the equality operator so that two Position objects are equal if they 
        have the same x and y coordinates. Otherwise, they would be considered two different objects.'''
        return (self.column == pt2.column) and (self.row == pt2.row)

'''Sample tests demonstrating deep equality between position objects:'''
'''
pt1 = Position(1, 1)
pt2 = Position(1, 1)
print(pt1 == pt2)      # Returns True
'''
