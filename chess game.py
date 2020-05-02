#chess game
from colorama import Fore, Back, Style
rows = tuple('87654321')        #a tuple of the rows.
columns = tuple('abcdefgh')     #a tuple of the columns.
rowString = '012345678'         #Row 1 is index 1, row 2 is index 2, etc.
columnString = '0abcdefgh'      #Column a is index 1, column b is index 2, etc.
chessboard = {}
positions = []
for rowNum in rows:     
    for columnLetter in columns:
        positions.append(rowNum + columnLetter)     #Positions is a list of all valid positions.
for position in positions:
    chessboard[position] = ' '      #Now chessboard is a dictionary of all positions with empty spaces as the values.

pieceColors = ['w', 'b']        #This block of code is unnecessary at this point. Lists of the colors, pieces, and pieces belonging to each color.
pieces = ['p', 'R', 'B', 'N', 'Q', 'K']
blackPieces = []
whitePieces = []
for piece in pieces:
    whitePieces.append(pieceColors[0] + piece)
    blackPieces.append(pieceColors[1] + piece)
allPieces = whitePieces + blackPieces       #Lists of the possible pieces. 

def setStartEndIndices(startLocation, endLocation):
    #Useful variables that give the start and end rows and columns, as well as a system for indexing the rows and columns.
    global startRow, endRow, startColumn, endColumn, startRowIndex, endRowIndex, startColumnIndex, endColumnIndex

    startRow = startLocation[0]
    endRow = endLocation[0]     
    startColumn = startLocation[1]
    endColumn = endLocation[1]
    startRowIndex = rowString.find(startRow)                                               
    endRowIndex = rowString.find(endRow)                         #  row 8 is index 8, row 1 is index 1                                 
    startColumnIndex = columnString.find(startColumn)
    endColumnIndex = columnString.find(endColumn)                    # column a is index 1, h is 8
'''Using the above function as a shortcut to define variables may cause problems, vs. just copy-pasting and defining the variables every time a movement function is called.'''
'''for some reason using the above function for whitePawnMovement() is okay, but it gives an undefined local error for 'startRowIndex' when using for the bishopMovement() function????'''

def visualBoard(playstate): 
    '''Prints a graphic version of all the pieces on the chessboard.'''        
    print('\n')
    for column in columns:
        print(column.center(7), end = '')       #First print the column letters.
    print('\n' + '_' + '_' * ((6*8)+8))         #Next print the line on top of the board.
    print('|', end = '')
    space = 0
    rowNum = 8
    for v in playstate.values():                    #Next print the board, using the pieces listed in the chessboard dictionary.
        if v.startswith('w'):                           
            print(Fore.CYAN + v.center(6) + Fore.WHITE + '|', end = '')
            space += 1
        elif v.startswith('b'):
            print(Fore.RED + v.center(6) + Fore.WHITE + '|', end = '' )
            space += 1
        else:                                           #For all spaces, print a colored red or white piece or an empty space. 
            print(v.center(6) + '|', end = '')
            space += 1
        if space == 64:                                 #There are 64 spaces on the board. At the end of the 64th space, row num '1' is printed.
            print('  ' + str(rowNum), end='')
        elif space % 8 == 0 and space < 64:             #at the end of each row of 8 spaces, print the row number, then subtract rowNum by 1 in order to get the next rowNum. Then print the lines between rows. 
            print('  ' + str(rowNum), end='')           
            rowNum -= 1
            print('\n', end = '')               #Note that rowNum '1' isn't printed, because if it were, then the next row of '|' and '-' is also printed.
            print('|' + (('-' * 6 +'|') * 8))
            print('|', end = '') 
    print('\n' + chr(175) + (chr(175) * ((6*8)+8)))         #Print the line on the bottom of the board.

def chessInit(board):  
    '''This function initializes the starting positions of the chessboard.'''
    for k in board.keys():
        board[k] = ' '     #Erase the board. 
    board['8a'] = 'bR'      #Then initialize the piece locations.
    board['8b'] = 'bB'
    board['8c'] = 'bN'
    board['8d'] = 'bQ'
    board['8e'] = 'bK'
    board['8f'] = 'bN'
    board['8g'] = 'bB'
    board['8h'] = 'bR'
    for k in board.keys():
        if k.startswith('7'):   #initializing the rows of pawns.
            board[k] = 'bp'
        if k.startswith('2'):
            board[k] = 'wp'
    board['1a'] = 'wR'
    board['1b'] = 'wB'
    board['1c'] = 'wN'
    board['1d'] = 'wQ'
    board['1e'] = 'wK'
    board['1f'] = 'wN'
    board['1g'] = 'wB'
    board['1h'] = 'wR'
    print(board)

def movePiece(board, piece, startLocation, endLocation):
    '''This function updates piece locations on the board after moving the pieces.'''
    board[startLocation] = ' '
    if board[endLocation] != ' ':
        print(board[endLocation] + ' has been captured!')
    board[endLocation] = piece

def whitePawnMovement(board, startLocation, endLocation):
    '''Rules for moving a white pawn.'''
    
    setStartEndIndices(startLocation, endLocation)
    
    try:
        if startRow == '2':       #If the pawn starts in row 2, rules dictate that it can move forward one or two spaces.
            if endRow == '3' and endColumn == startColumn:  
                if board[endLocation] != ' ':       #moving forward one space to row 3 is valid, but only when the end location is empty. 
                    validEndCheck = False
                else:
                    validEndCheck = True
            elif endRow == '4':     #if moving forward two spaces from row 2:
                if board[rowString[endRowIndex + 1] + columnString[endColumnIndex]] != ' ':  #First make sure the space in row three is an empty space. If not, valid end location is False. 
                    validEndCheck = False
                elif board[endLocation] != ' ':     #The target space the pawn moves to in row four must also be empty. 
                    validEndCheck = False
                elif endColumn == startColumn:    #If you stay in the same column when moving forward 2 spaces then valid end is true.  
                    validEndCheck = True
                else:                               #this final False condition only occurs if the pawn doesn't stay in the same column.
                    validEndCheck = False
            elif endRow == '3':
                if endColumn == columnString[startColumnIndex + 1] and board[endLocation].startswith('b'):  #if moving diagonally to the right, and there is a black piece, the move is valid
                    validEndCheck = True  
                if endColumn == columnString[startColumnIndex - 1] and board[endLocation].startswith('b'):  #diagonally to left. must contain black piece. 
                    validEndCheck = True
                else:
                    validEndCheck = False
            else:                                
                validEndCheck = False           #if a row besides 3 or 4 is selected.
        elif startColumn == endColumn:  #if the pawn moves forward in the same column:
            if board[endLocation] != ' ':   #first check the space is empty
                validEndCheck = False
            elif endRow != rowString[startRowIndex + 1]:  #check that the pawn only moves one space
                #print(endRow)
                #rint( rowString[startRowIndex + 1])
                validEndCheck = False
            else:
                validEndCheck = True
        elif endColumn == columnString[startColumnIndex - 1] and endRow == rowString[startRowIndex + 1]:
            if board[endLocation].startswith('b'):               #Move diagonally to left. End column must contain black piece. 
                validEndCheck = True 
            else:
                validEndCheck = False
        elif endColumn == columnString[startColumnIndex + 1] and endRow == rowString[startRowIndex + 1]:
            if board[endLocation].startswith('b'):    #move diagonally to right. End column must contain black piece.            
                validEndCheck = True 
            else:
                validEndCheck = False
        else:
            validEndCheck = False
    except IndexError:
        validEndCheck = False
    return validEndCheck

#TODO: def blackPawnMovement(board, startLocation, endLocation):

def rookMovement(board, startLocation, endLocation):   
    '''Rules for moving a Rook.'''
   
    setStartEndIndices(startLocation, endLocation)

    if board[startLocation].startswith('w'):
        turn = 'w'
    if board[startLocation].startswith('b'):
        turn = 'b'
    while True:
        if turn == 'b':              #first check that the endLocation can be moved to
            if board[endLocation].startswith('w') or board[endLocation] == ' ': #if moving a black rook, if the end location has a white piece or is empty, return true
                validEndCheck = True
            else:
                validEndCheck = False
            break
        elif turn == 'w':
            if board[endLocation].startswith('b') or board[endLocation] == ' ': 
                validEndCheck = True
            else:
                validEndCheck = False
            break

    if startRow != endRow and startColumn != endColumn:     #Next check: either the rook must stay in the same row, or in the same column.
        validEndCheck = False
    
    elif startColumn == endColumn:  #generate a list of the spaces inbetween the start and endpoint. Either row, or column must stay the same. 
        inBetweenSpaces = []
        for i in range( min(startRowIndex, endRowIndex), max(startRowIndex, endRowIndex)):
            inBetweenSpaces.append(str(rowString[i]) + startColumn)
        del inBetweenSpaces[0]    
        #print('inbetween = ' + str(inBetweenSpaces))
   
    elif startRow == endRow:      #if moving in a row, then the row doesn't change.
        inBetweenSpaces = []
        for i in range( min(startColumnIndex, endColumnIndex), max(startColumnIndex, endColumnIndex) ): 
            inBetweenSpaces.append(startRow + str(columnString[i]))
        del inBetweenSpaces[0]
        #print('inbetween = ' +str( inBetweenSpaces))
    
    for space in inBetweenSpaces:       #Finally, check that the inbetween spaces are empty.
        if board[space] != ' ':         #if the in-between space is not empty, move is invalid
            validEndCheck = False
            break 

    return validEndCheck

def bishopMovement(board, startLocation, endLocation):
    '''Rules for moving a bishop.'''
    startRow = startLocation[0]
    endRow = endLocation[0]     
    startColumn = startLocation[1]
    endColumn = endLocation[1]

    startRowIndex = rowString.find(startRow)                                                   
    endRowIndex = rowString.find(endRow)                         #  row 8 is index 8, row 1 is index 1                                 
    startColumnIndex = columnString.find(startColumn)
    endColumnIndex = columnString.find(endColumn)                    # column a is index 1, h is 8
    
    if board[startLocation].startswith('w'):
        turn = 'w'
    if board[startLocation].startswith('b'):
        turn = 'b'
   
    if turn == 'b':              #first check that the endLocation can be moved to
        if board[endLocation].startswith('w') or board[endLocation] == ' ': #if moving a black bishop, if the end location has a white piece or is empty, return true
            validEndCheck = True
        else:
            validEndCheck = False
            return validEndCheck
    if turn == 'w':
        if board[endLocation].startswith('b') or board[endLocation] == ' ': 
            validEndCheck = True
        else:
            validEndCheck = False
            return validEndCheck      
    inBetweenSpaces = []
   
    if startRowIndex < endRowIndex and startColumnIndex < endColumnIndex:    # if the bishop is moving diagonally up and to the right:
        while True:                 #These  loops return diagonal positions that a bishop can move to. 
            if startRowIndex == endRowIndex:       
                break               #if you hit the edge of the rows or columns, break the for loop
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex += 1          #increment rows and columns by one
            startColumnIndex += 1
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex]) # and then append the position to list of valid diagonal movement positions
    
    if startRowIndex > endRowIndex and startColumnIndex < endColumnIndex: # if the bishop is moving diagonally down and to the right
        while True:                
            if startRowIndex == endRowIndex:
                break
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex -= 1   
            print('startRow = ' + str(startRowIndex))       
            startColumnIndex += 1
            print('startColumnIndex = ' + str(startColumnIndex))
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex])

    if startRowIndex < endRowIndex and startColumnIndex > endColumnIndex: # if the bishop is moving diagonally up and to the left
        while True:                
            if startRowIndex == endRowIndex:
                break
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex += 1
            startColumnIndex -= 1
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex])

    if startRowIndex > endRowIndex and startColumnIndex > endColumnIndex: # if the bishop is moving diagonally down and to the left
        while True:                
            if startRowIndex == endRowIndex:
                break
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex -= 1
            startColumnIndex -= 1
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex])
    
    if endLocation not in inBetweenSpaces: 
        validEndCheck = False
        return validEndCheck

    del inBetweenSpaces[-1] #inBetweenSpaces[-1] is the destination space. Only the spaces in between the destination and start need to be checked to be empty. 
    #print(inBetweenSpaces) #for debugging
    for space in inBetweenSpaces:
        if board[space] != ' ':
            validEndCheck = False
            return validEndCheck

    return validEndCheck


def knightMovement(board, startLocation, endLocation):
    startRow = startLocation[0]
    endRow = endLocation[0]     
    startColumn = startLocation[1]
    endColumn = endLocation[1]

    startRowIndex = rowString.find(startRow)                                                   
    endRowIndex = rowString.find(endRow)                         #  row 8 is index 8, row 1 is index 1                                 
    startColumnIndex = columnString.find(startColumn)
    endColumnIndex = columnString.find(endColumn)                    # column a is index 1, h is 8

    if board[startLocation].startswith('w'):
        turn = 'w'
    if board[startLocation].startswith('b'):
        turn = 'b'
   
    if turn == 'b':              #first check that the endLocation can be moved to
        if board[endLocation].startswith('w') or board[endLocation] == ' ': 
            validEndCheck = True
        else:
            validEndCheck = False
            return validEndCheck
    if turn == 'w':
        if board[endLocation].startswith('b') or board[endLocation] == ' ': 
            validEndCheck = True
        else:
            validEndCheck = False
            return validEndCheck     
    validEndLocations = []        
    try:
        
#def queenMovement(board, startLocation, endLocation):

#def kingMovement(board, startLocation, endLocation):


def whiteMove(board):
    '''This function asks what white piece to move to where. The function provides rules for valid movement.'''
    while True:
        startLocation = input(' White turn! Location of piece you would like to move? Enter row, then column.\n')
        if startLocation not in board.keys():   
            print('Invalid location! Please enter row, then column. E.g. "1a"')
            continue
        elif not board[startLocation].startswith('w'):
            print('There is no white chess piece at that location. Please enter a valid location.')
            continue
        elif board[startLocation].startswith('w'):          #picked a valid start location containing a white piece.
            piece = board[startLocation]          
            endLocation = input('To what location would you like to move this piece?\n')        #after picking a valid start location, pick an end location confined by the movement rules
            if board[startLocation] == 'wp':        
                validEndCheck = whitePawnMovement(board, startLocation, endLocation)   
            if board[startLocation] == 'wR':
                validEndCheck = rookMovement(board, startLocation, endLocation)
            if board[startLocation] == 'wB':
                validEndCheck = bishopMovement(board, startLocation, endLocation)                  
            if not validEndCheck:
                print('Invalid move!')
                visualBoard(board)
                continue        
            if validEndCheck:
                movePiece(board, piece, startLocation, endLocation)
                visualBoard(board)
                #break          #need to come back to this later, to end white's turn
                continue

#def blackMove(board):





testBoard = {'8a': 'bR', '8b': 'bB', '8c': 'bN', '8d': 'bQ', '8e': 'bK', '8f': 'bN', '8g': 'bB', '8h': 'bR', 
'7a': 'bp', '7b': 'bp', '7c': 'bp', '7d': 'bp', '7e': 'bp', '7f': 'bp', '7g': 'bp', '7h': 'bp', '6a': 'wp',
 '6b': ' ', '6c': ' ', '6d': ' ', '6e': ' ', '6f': ' ', '6g': ' ', '6h': ' ', '5a': ' ', '5b': ' ', '5c': ' ', 
 '5d': ' ', '5e': ' ', '5f': ' ', '5g': ' ', '5h': ' ', '4a': ' ', '4b': ' ', '4c': ' ', '4d': ' ', '4e': ' ', '4f': ' ', 
 '4g': ' ', '4h': ' ', '3a': 'bp', '3b': 'wp', '3c': ' ', '3d': ' ', '3e': ' ', '3f': ' ', '3g': ' ', '3h': ' ', '2a': 'wp', 
 '2b': 'wp', '2c': 'wp', '2d': 'wp', '2e': 'wp', '2f': ' ', '2g': 'wp', '2h': ' ', '1a': 'wR', '1b': 'wB', '1c': 'wN', '1d': 'wQ', '1e': 'wK', '1f': 'wN', '1g': 'wB', '1h': 'wR'}


visualBoard(testBoard)
whiteMove(testBoard)

#chessInit(chessboard)
#visualBoard(chessboard)
#print('Welcome to Kevin's chess game! Press any key to continue. Press ctrl-c at any time to exit.')
#Input()
#print('White player moves first. Piece locations are denoted by row, then column. E.g. the white King, "wK", is initially located at 1e.')
#whiteMove(chessboard)

#TODO:
''' Rules for castling, for when a pawn reaches the opposite end of the board, rules for check and checkmate, rules for switching a bishop with a pawn, 
rules for turn structure and winning, quitting out of the game, starting a new game, possibly AI movement'''