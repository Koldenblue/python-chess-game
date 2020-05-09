#!/usr/bin/python3
#chess game
from colorama import Fore, Back, Style
import sys

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

# This next block of code is unnecessary at this point. Lists colors, pieces, and pieces belonging to each color.
pieceColors = ['w', 'b'] 
pieces = ['p', 'R', 'B', 'N', 'Q', 'K']
blackPieces = []
whitePieces = []
for piece in pieces:
    whitePieces.append(pieceColors[0] + piece)
    blackPieces.append(pieceColors[1] + piece)
allPieces = whitePieces + blackPieces


def setStartEndIndices(startLocation, endLocation):
    '''Useful variables that give the start and end rows and columns, as well as a system for indexing the rows and columns.'''
    #global startRow, endRow, startColumn, endColumn, startRowIndex, endRowIndex, startColumnIndex, endColumnIndex
    startRow = startLocation[0]
    endRow = endLocation[0]
    startColumn = startLocation[1]
    endColumn = endLocation[1]
    startRowIndex = rowString.find(startRow)
    endRowIndex = rowString.find(endRow)                         #  row 8 is index 8, row 1 is index 1
    startColumnIndex = columnString.find(startColumn)
    endColumnIndex = columnString.find(endColumn)                    # column a is index 1, h is 8
    return startRow, endRow, startColumn, endColumn, startRowIndex, endRowIndex, startColumnIndex, endColumnIndex
    '''Using the above function as a shortcut to define variables may cause problems, vs. just copy-pasting and defining the variables every time a movement function is called.'''
    '''For some reason using the above function for whitePawnMovement() is okay, but it gives an undefined local error for 'startRowIndex' when using for the bishopMovement() function?'''

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

def movePiece(board, piece, startLocation, endLocation):
    '''This function updates piece locations on the board after moving the pieces.'''
    board[startLocation] = ' '
    if board[endLocation] != ' ':
        print(board[endLocation] + ' has been captured!')
    board[endLocation] = piece

def whitePawnMovement(board, startLocation, endLocation):
    '''Rules for moving a white pawn.'''

    startRow, endRow, startColumn, endColumn, startRowIndex, endRowIndex, startColumnIndex, endColumnIndex = setStartEndIndices(startLocation, endLocation)

    try:
        if startRow == '2':       #If the pawn starts in row 2, rules dictate that it can move forward one or two spaces.
            if endRow == '3' and endColumn == startColumn:
                if board[endLocation] != ' ':       #moving forward one space to row 3 is valid, but only when the end location is empty.
                    validEndCheck = False
                else:
                    validEndCheck = True
            elif endRow == '4':     #if moving forward two spaces from row 2:
                if board[rowString[startRowIndex + 1] + endColumn] != ' ':  #First make sure the space in row three is an empty space. If not, valid end location is False.
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

def blackPawnMovement(board, startLocation, endLocation):
    '''Rules for moving a black pawn.'''
    # White and black pawn functions might be combined, but would require extra effort. Could use a "turn" function.
    startRow, endRow, startColumn, endColumn, startRowIndex, endRowIndex, startColumnIndex, endColumnIndex = setStartEndIndices(startLocation, endLocation)

    try:
        if startRow == '7':       #If the pawn starts in row 7, rules dictate that it can move forward one or two spaces.
            if endRow == '6' and endColumn == startColumn:
                if board[endLocation] != ' ':       #moving forward one space is valid, but only when the end location is empty.
                    validEndCheck = False
                else:
                    validEndCheck = True
            elif endRow == '5':     #if moving forward two spaces from row 7:
                if board[rowString[startRowIndex - 1] + endColumn] != ' ':  #First make sure the space in row 5 is an empty space. If not, valid end location is False.
                    validEndCheck = False
                elif board[endLocation] != ' ':     #The target space the pawn moves must also be empty.
                    validEndCheck = False
                elif endColumn == startColumn:    #If you stay in the same column when moving forward 2 spaces then valid end is true.
                    validEndCheck = True
                else:        #this final False condition only occurs if the pawn doesn't stay in the same column.
                    validEndCheck = False
            elif endRow == '6':
                if endColumn == columnString[startColumnIndex + 1] and board[endLocation].startswith('w'):  #if moving diagonally to the right, and there is a white piece, the move is valid
                    validEndCheck = True
                if endColumn == columnString[startColumnIndex - 1] and board[endLocation].startswith('w'):  #diagonally to left. must contain white piece.
                    validEndCheck = True
                else:
                    validEndCheck = False
            else:
                validEndCheck = False           #if a row besides 6 or 5 is selected.
        elif startColumn == endColumn:  #if the pawn moves forward in the same column:
            if board[endLocation] != ' ':   #first check the space is empty
                validEndCheck = False
            elif endRow != rowString[startRowIndex - 1]:  #check that the pawn only moves one space
                validEndCheck = False
            else:
                validEndCheck = True
        elif endColumn == columnString[startColumnIndex - 1] and endRow == rowString[startRowIndex - 1]:
            if board[endLocation].startswith('w'):               #Move diagonally to left. Must contain white piece.
                validEndCheck = True
            else:
                validEndCheck = False
        elif endColumn == columnString[startColumnIndex + 1] and endRow == rowString[startRowIndex - 1]:
            if board[endLocation].startswith('w'):    #move diagonally to right.
                validEndCheck = True
            else:
                validEndCheck = False
        else:
            validEndCheck = False
    except IndexError:
        validEndCheck = False
    return validEndCheck

def rookMovement(board, startLocation, endLocation):
    '''Rules for moving a Rook.'''

    startRow, endRow, startColumn, endColumn, startRowIndex, endRowIndex, startColumnIndex, endColumnIndex = setStartEndIndices(startLocation, endLocation)

    if board[startLocation].startswith('w'):
        turn = 'w'
    if board[startLocation].startswith('b'):
        turn = 'b'
    while True:
        if turn == 'b':              #first check that the endLocation can be moved to
            if board[endLocation].startswith('w') or board[endLocation] == ' ': # if moving a black rook, if the end location has a white piece or is empty, return true
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

    # Generate a list of the spaces inbetween the start and endpoint.
    # Either row, or column must stay the same.
    elif startColumn == endColumn:
        inBetweenSpaces = []
        for i in range( min(startRowIndex, endRowIndex), max(startRowIndex, endRowIndex)):
            inBetweenSpaces.append(str(rowString[i]) + startColumn)
        # inBetweenSpaces[0] will either be startLocation or endLocation.
        # Either way, it should be deleted.
        # Since the for loop counts up to, but doesn't include, the last space,
            # the remaining spaces in inBetweenSpaces are indeed the in between spaces.
        del inBetweenSpaces[0]

    elif startRow == endRow:      # if moving in a row, then the row doesn't change.
        inBetweenSpaces = []
        for i in range( min(startColumnIndex, endColumnIndex), max(startColumnIndex, endColumnIndex) ):
            inBetweenSpaces.append(startRow + str(columnString[i]))
        del inBetweenSpaces[0]

    # Finally, check that the inbetween spaces are empty.
    for space in inBetweenSpaces:
        if board[space] != ' ':
            validEndCheck = False
            return validEndCheck

    return validEndCheck

def bishopMovement(board, startLocation, endLocation):
    '''Rules for moving a bishop.'''

    startRow, endRow, startColumn, endColumn, startRowIndex, endRowIndex, startColumnIndex, endColumnIndex = setStartEndIndices(startLocation, endLocation)


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

    # If the bishop is moving diagonally up and to the right:
    if startRowIndex < endRowIndex and startColumnIndex < endColumnIndex:
        while True:
            # Increment the starting row and column until either the end row or end column is reached.
            # This loop will give all diagonal movement spaces between startLocation and endLocation.
            if startRowIndex == endRowIndex:
                break
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex += 1
            startColumnIndex += 1
            # Keep appending the diagonal movement positions until endLocation is reached.
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex]) 

    # If moving diagonally down and to the right:
    if startRowIndex > endRowIndex and startColumnIndex < endColumnIndex:
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
    
    # If moving diagonally up and to the left:
    if startRowIndex < endRowIndex and startColumnIndex > endColumnIndex: 
        while True:
            if startRowIndex == endRowIndex:
                break
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex += 1
            startColumnIndex -= 1
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex])
    
    # If moving diagonally down and to the left:
    if startRowIndex > endRowIndex and startColumnIndex > endColumnIndex: 
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
    endRowIndex = rowString.find(endRow)    #unused variable          # row 8 is index 8, row 1 is index 1
    startColumnIndex = columnString.find(startColumn)
    endColumnIndex = columnString.find(endColumn)      # unused variable      # column a is index 1, h is 8

    if board[startLocation].startswith('w'):
        turn = 'w'
    if board[startLocation].startswith('b'):
        turn = 'b'

    if turn == 'b':              # first check that the endLocation can be moved to
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
    try:        # making a list of the eight possible spaces a knight can move to
        validEndLocations.append(rowString[startRowIndex + 2] + columnString[startColumnIndex + 1])
    except IndexError:
        pass    # IndexError will occur if the knight is too close to the edge of the board i.e. the knight can't move off the board
    try:
        # Make sure the knight can't "wrap" around to the other side of the board with a negative index.
        if startRowIndex - 2 > 0:
            validEndLocations.append(rowString[startRowIndex - 2] + columnString[startColumnIndex + 1])
    except IndexError:
        pass
    try:
        if startColumnIndex - 1 > 0:
            validEndLocations.append(rowString[startRowIndex + 2] + columnString[startColumnIndex - 1])
    except IndexError:
        pass
    try:
        if startRowIndex - 2 > 0 and startColumnIndex - 1 > 0:
            validEndLocations.append(rowString[startRowIndex - 2] + columnString[startColumnIndex - 1])
    except IndexError:
        pass
    try:
        validEndLocations.append(rowString[startRowIndex + 1] + columnString[startColumnIndex + 2])
    except IndexError:
        pass
    try:
        if startRowIndex - 1 > 0:
            validEndLocations.append(rowString[startRowIndex - 1] + columnString[startColumnIndex + 2])
    except IndexError:
        pass
    try:
        if startColumnIndex - 2 > 0:
            validEndLocations.append(rowString[startRowIndex + 1] + columnString[startColumnIndex - 2])
    except IndexError:
        pass
    try:
        if startRowIndex - 1 > 0 and startColumnIndex - 2 > 0:
            validEndLocations.append(rowString[startRowIndex - 1] + columnString[startColumnIndex - 2])
    except IndexError:
        pass
    # print(validEndLocations) #print for debugging
    # Already checked earlier to make sure the endLocation was empty or has a piece of the opposite color.
    # Now just have to check that endLocation is valid.
    if endLocation in validEndLocations:
        validEndCheck = True
    else:
        validEndCheck = False
    return validEndCheck

def queenMovement(board, startLocation, endLocation):
    '''Rules for moving a queen.'''
    startRow = startLocation[0]
    endRow = endLocation[0]
    startColumn = startLocation[1]
    endColumn = endLocation[1]
    startRowIndex = rowString.find(startRow)
    endRowIndex = rowString.find(endRow)  # Row 8 is index 8, row 1 is index 1
    startColumnIndex = columnString.find(startColumn)
    endColumnIndex = columnString.find(endColumn)  # Column a is index 1, h is 8

    if board[startLocation].startswith('w'):
        turn = 'w'
    if board[startLocation].startswith('b'):
        turn = 'b'

    if turn == 'b':
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

    inBetweenSpaces = []

    # If the queen is moving diagonally up and to the right:
    if startRowIndex < endRowIndex and startColumnIndex < endColumnIndex:
        while True:
            # Increment the starting row and column until either the end row or end column is reached.
            # This loop will give all diagonal movement spaces between startLocation and endLocation.
            if startRowIndex == endRowIndex:
                break
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex += 1
            startColumnIndex += 1
            # Keep appending the diagonal movement positions until endLocation is reached.
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex])
        # The destination space needs to be removed, as it is not "in between".
        del inBetweenSpaces[-1]

    # If moving diagonally down and to the right:
    if startRowIndex > endRowIndex and startColumnIndex < endColumnIndex:
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
        del inBetweenSpaces[-1]

    # If moving diagonally up and to the left:
    if startRowIndex < endRowIndex and startColumnIndex > endColumnIndex: 
        while True:
            if startRowIndex == endRowIndex:
                break
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex += 1
            startColumnIndex -= 1
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex])
        del inBetweenSpaces[-1]

    # If moving diagonally down and to the left:
    if startRowIndex > endRowIndex and startColumnIndex > endColumnIndex: 
        while True:
            if startRowIndex == endRowIndex:
                break
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex -= 1
            startColumnIndex -= 1
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex])
        del inBetweenSpaces[-1]

    if startColumn == endColumn:
        for i in range(min(startRowIndex, endRowIndex), max(startRowIndex, endRowIndex)):
            inBetweenSpaces.append(str(rowString[i]) + startColumn)
        # inBetweenSpaces[0] will either be startLocation or endLocation.
        # Either way, it should be deleted, since it is not "in between".
        # Since the for loop counts up to, but doesn't include, the last space,
            # the remaining spaces in inBetweenSpaces are indeed the in between spaces.
        del inBetweenSpaces[0]

    if startRow == endRow:
        for i in range(min(startColumnIndex, endColumnIndex), max(startColumnIndex, endColumnIndex)):
            inBetweenSpaces.append(startRow + str(columnString[i]))
        del inBetweenSpaces[0]

    # Finally, check that the inbetween spaces are empty.
    for space in inBetweenSpaces:
        if board[space] != ' ':
            validEndCheck = False
            return validEndCheck

    # If the code reaches this point, validEndCheck returns True.
    return validEndCheck

def kingMovement(board, startLocation, endLocation):
    '''Rules for moving a king.'''
    startRow = startLocation[0]
    endRow = endLocation[0]
    startColumn = startLocation[1]
    endColumn = endLocation[1]
    startRowIndex = rowString.find(startRow)
    endRowIndex = rowString.find(endRow)  # Row 8 is index 8, row 1 is index 1
    startColumnIndex = columnString.find(startColumn)
    endColumnIndex = columnString.find(endColumn)  # Column a is index 1, h is 8

    if board[startLocation].startswith('w'):
        turn = 'w'
    if board[startLocation].startswith('b'):
        turn = 'b'

    if turn == 'b':
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
    for row in range(-1, 2):
        for column in range(-1, 2):
            try:
                validEndLocations.append(rowString[startRowIndex + row] + columnString[startColumnIndex + column])
            except IndexError:
                pass
    # Already checked earlier that the piece is moving to a valid board location.
    # So validEndLocations can include spaces like 70 or 0h, but this doesn't matter.
    for space in validEndLocations:
        if space == startLocation:
            validEndLocations.remove(space)

    print(validEndLocations)
    if endLocation not in validEndLocations:
        validEndCheck = False
        return validEndCheck

    return validEndCheck

def whiteMove(board):
    '''This function asks what white piece to move to where. The function provides rules for valid movement.'''
    while True:
        #Always print the board at the start of the loop, except when game is first started.
        visualBoard(board)
        startLocation = input(Fore.CYAN + 'White turn!' + Fore.RESET + ' Location of piece you would like to move? Enter row, then column.\n')
        if startLocation.lower() == 'exit':
            raise Exception('Exiting program!') # Need to handle exiting better.
        if startLocation not in board.keys():
            print('Invalid location! Please enter row, then column. E.g. "1a"\n')
            continue
        elif not board[startLocation].startswith('w'):
            print('There is no white chess piece at that location. Please enter a valid location.\n')
            continue
        elif board[startLocation].startswith('w'):          #picked a valid start location containing a white piece.
            piece = board[startLocation]
            endLocation = input('To what location would you like to move this piece?\n')  #after picking a valid start location, pick an end location confined by the movement rules
            if endLocation.lower() == 'exit':
                raise Exception('Exiting program!')
            if endLocation not in board.keys():
                print('Invalid location! Please enter a valid row, then column. E.g. "1a"')
                continue
            if board[startLocation] == 'wp':
                validEndCheck = whitePawnMovement(board, startLocation, endLocation)
            if board[startLocation] == 'wR':
                validEndCheck = rookMovement(board, startLocation, endLocation)
            if board[startLocation] == 'wB':
                validEndCheck = bishopMovement(board, startLocation, endLocation)
            if board[startLocation] == 'wN':
                validEndCheck = knightMovement(board, startLocation, endLocation)
            if board[startLocation] == 'wQ':
                validEndCheck = queenMovement(board, startLocation, endLocation)
            if board[startLocation] == 'wK':
                validEndCheck = kingMovement(board, startLocation, endLocation)
            if not validEndCheck:
                print('Invalid move!')
                continue
            else:
                movePiece(board, piece, startLocation, endLocation)
                break


def blackMove(board):
    '''This function asks what black piece to move to where. The function provides rules for valid movement.'''
    while True:
        visualBoard(board)
        startLocation = input(Fore.RED + 'Black turn! ' + Fore.RESET + 'Location of piece you would like to move? Enter row, then column.\n')
        if startLocation.lower() == 'exit':
            raise Exception('Exiting program!') # Need to handle exiting better.
        if startLocation not in board.keys():
            print('Invalid location! Please enter row, then column. E.g. "1a"\n')
            continue
        elif not board[startLocation].startswith('b'):
            print('There is no black chess piece at that location. Please enter a valid location.\n')
            continue
        elif board[startLocation].startswith('b'):          #picked a valid start location containing a white piece.
            piece = board[startLocation]
            endLocation = input('To what location would you like to move this piece?\n')  #after picking a valid start location, pick an end location confined by the movement rules
            if endLocation.lower() == 'exit':
                raise Exception('Exiting program!')
            if endLocation not in board.keys():
                print('Invalid location! Please enter a valid row, then column. E.g. "1a"')
                continue
            if board[startLocation] == 'bp':
                validEndCheck = blackPawnMovement(board, startLocation, endLocation)
            if board[startLocation] == 'bR':
                validEndCheck = rookMovement(board, startLocation, endLocation)
            if board[startLocation] == 'bB':
                validEndCheck = bishopMovement(board, startLocation, endLocation)
            if board[startLocation] == 'bN':
                validEndCheck = knightMovement(board, startLocation, endLocation)
            if board[startLocation] == 'bQ':
                validEndCheck = queenMovement(board, startLocation, endLocation)
            if board[startLocation] == 'bK':
                validEndCheck = kingMovement(board, startLocation, endLocation)
            if not validEndCheck:
                print('Invalid move!')
                continue
            else:
                movePiece(board, piece, startLocation, endLocation)
                break

# A test chessboard that can be set up for testing purposes.
testBoard = {'8a': 'bR', '8b': 'bB', '8c': 'bN', '8d': 'bQ', '8e': 'bK', '8f': 'bN', '8g': 'bB', '8h': 'bR',
    '7a': 'bp', '7b': 'bp', '7c': 'bp', '7d': 'bp', '7e': 'bp', '7f': 'bp', '7g': 'bp', '7h': 'bp',
    '6a': 'wp', '6b': ' ', '6c': ' ', '6d': ' ', '6e': ' ', '6f': ' ', '6g': ' ', '6h': ' ',
    '5a': ' ', '5b': ' ', '5c': ' ', '5d': 'wQ', '5e': ' ', '5f': ' ', '5g': 'wK', '5h': ' ',
    '4a': ' ', '4b': ' ', '4c': ' ', '4d': ' ', '4e': ' ', '4f': ' ', '4g': ' ', '4h': ' ',
    '3a': 'bp', '3b': 'wp', '3c': ' ', '3d': ' ', '3e': ' ', '3f': ' ', '3g': ' ', '3h': ' ',
    '2a': 'wp', '2b': 'wp', '2c': 'wp', '2d': 'wp', '2e': 'wp', '2f': 'wN', '2g': 'wp', '2h': ' ',
    '1a': 'wR', '1b': 'wB', '1c': 'wN', '1d': 'wQ', '1e': 'wK', '1f': 'wN', '1g': 'wB', '1h': 'wK'}

# Welcome Screen.
print('\n\n' + Fore.GREEN + Back.BLACK + ('~' * 131) + Fore.RESET + Back.RESET)
print('Welcome to Kevin\'s chess game! Be sure your window is wide enough to avoid graphical errors with the board!')
print('Type "exit" at any time to quit.')  # Exiting is inelegant, but works when entering start or end locations.
print('White player moves first. Piece locations are denoted by row, then column. E.g. the white King, "wK", is initially located at 1e.')
print(Fore.GREEN + Back.BLACK + ('~' * 131) + Fore.RESET + Back.RESET)

# Initialize the chessboard. Note that 'testboard' can instead be used for debugging.
# May want to implement saving, instead of initializing board always.
chessInit(chessboard)

# Main program loop.
while True:
    whiteMove(testBoard)
    # blackMove(testBoard)


'''visualBoard(testBoard)
##try:
blackMove(testBoard)
#except Exception as exitMessage:
#    print(exitMessage)  # The except clause will still result in the remaining code being executed.
#try:
whiteMove(testBoard)
#except Exception as exitMessage:
 #   print(exitMessage)  # The except clause will still result in the remaining code being executed.

visualBoard(testBoard)'''


# Updated: 5/9/2020 4:30 pm

#TODO:
''' Rules for castling, for when a pawn reaches the opposite end of the board, rules for check and checkmate, rules for switching a bishop with a pawn,
rules for turn structure and winning, quitting out of the game, starting a new game, possibly AI movement'''

