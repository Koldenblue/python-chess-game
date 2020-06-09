class Position:
    def __init__(self, x, y):
        '''Defines a coordinate on the chessboard, where the x axis changes with columns, and the y axis changes with rows.'''
        self.column = x 
        self.row = y
    
    def __str__(self):
        return "({0}, {1})".format(self.column, self.row)

    def isPosition(self, pt2):
        return (self.column == pt2.column) and (self.row == pt2.row)




'''Tests demonstrating deep equality between position objects:'''
#def isPosn(pt1, pt2):
#    return (pt1.column == pt2.column) and (pt1.row == pt2.row)

#pt1 = Position(1, 1)
#pt2 = Position(1, 1)
#print(pt1 == pt2)      # Returns False
#print(pt1 is pt2)      # returns False
#print(pt1.isPosition(pt2))     # returns True
#print(isPosn(pt1, pt2))     #returns True

