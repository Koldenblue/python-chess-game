#!/usr/bin/python3
#chess game
from colorama import Fore, Back, Style
import sys

rows = tuple('87654321')        #a tuple of the rows.
columns = tuple('abcdefgh')     #a tuple of the columns.
rowString = '012345678'         #Row 1 is index 1, row 2 is index 2, etc.
columnString = '0abcdefgh'      #Column a is index 1, column b is index 2, etc.


# Positions is a list of all valid positions.
# It is used as keys to populate chessboard{}, which has positions as the keys and empty spaces as the values.
positions = []
chessboard = {}
for rowNum in rows:
    for columnLetter in columns:
        positions.append(rowNum + columnLetter)
for position in positions:
    chessboard[position] = ' '

# current_turn is used for checking spaces threatened by the king, in order to avoid an infinite loop
current_turn = 'w'

# A global bool that gets marked True when the threatenedBy functions are called,
# so that the threatenedBy() functions will not check for 'check' when finding valid movements.
checkingForThreatened = False

# The kings start the game not in check.
# These variables need to be used to limit possible moves during a turn, if a king is in check.
whiteKingInCheck = False
blackKingInCheck = False

def visualBoard(playstate):
    '''Prints a graphic version of all the pieces on the chessboard.'''
    print('\n')
    for column in columns:
        print(column.center(7), end = '')       # First print the column letters.
    print('\n' + '_' + '_' * ((6*8)+8))         # Next print the line on top of the board.
    print('|', end = '')
    space = 0
    rowNum = 8
    for v in playstate.values():                # Next print the board, using the pieces listed in the chessboard dictionary.
        if v.startswith('w'):
            print(Fore.CYAN + v.center(6) + Fore.WHITE + '|', end = '')
            space += 1
        elif v.startswith('b'):
            print(Fore.RED + v.center(6) + Fore.WHITE + '|', end = '' )
            space += 1
        else:                                   # For all spaces, print a colored red or cyan piece or an empty space.
            print(v.center(6) + '|', end = '')
            space += 1
        if space == 64:                         # There are 64 spaces on the board. At the end of the 64th space, row num '1' is printed.
            print('  ' + str(rowNum), end='')
        elif space % 8 == 0 and space < 64:     # At the end of each row of 8 spaces, print the row number, then subtract rowNum by 1 in order to get the next rowNum. Then print the lines between rows.
            print('  ' + str(rowNum), end='')
            rowNum -= 1
            print('\n', end = '')               # Note that rowNum '1' isn't printed, because if it were, then the next row of '|' and '-' is also printed.
            print('|' + (('-' * 6 +'|') * 8))
            print('|', end = '')
    print('\n' + chr(175) + (chr(175) * ((6*8)+8)))         #Print the line on the bottom of the board.

def chessInit(board):
    '''This function initializes the starting positions of the chessboard.'''
    for k in board.keys():
        board[k] = ' '      # Erase the board.
    board['8a'] = 'bR'      # Then initialize the piece locations.
    board['8b'] = 'bB'
    board['8c'] = 'bN'
    board['8d'] = 'bQ'
    board['8e'] = 'bK'
    board['8f'] = 'bN'
    board['8g'] = 'bB'
    board['8h'] = 'bR'
    for k in board.keys():
        if k.startswith('7'):   # Initializing the rows of pawns.
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
    # If a king was moved, the keys for the kingLocation global variables need to be updated.
    if piece == 'wK': 
        global globalWhiteKing
        globalWhiteKing = endLocation
    if piece == 'bK':
        global globalBlackKing
        globalBlackKing = endLocation

def whitePawnMovement(board, startLocation, endLocation):
    '''Rules for moving a white pawn.'''

    startRow = startLocation[0]
    endRow = endLocation[0]
    startColumn = startLocation[1]
    endColumn = endLocation[1]
    startRowIndex = rowString.find(startRow)
    # row 8 is index 8, row 1 is index 1
    startColumnIndex = columnString.find(startColumn)
    # column a is index 1, h is 8

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
                elif endColumn == columnString[startColumnIndex - 1] and board[endLocation].startswith('b'):  #diagonally to left. must contain black piece.
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

    # Finally, check whether any kings are placed in check. Temporarily move the piece in order to do this.
    # This code gets passed over if one of the threatenedBy() functions called this movement function. 
    # In other words, this code is only checked if the piece in question is the user entered piece!
    global checkingForThreatened
    global whiteKingInCheck
    global blackKingInCheck
    if checkingForThreatened == False:
        if current_turn == 'w':
            tempMovingPiece = board[startLocation]
            tempRemovedPiece = board[endLocation]
            board[endLocation] = 'wp'
            board[startLocation] = ' '
            if whiteKingCheck(board, globalWhiteKing):
                print("White King would be in check!")
                validEndCheck = False
            elif blackKingCheck(board, globalBlackKing):
                print(Fore.RED + "Black King is in check!" + Fore.RESET)
                blackKingInCheck = True
            board[startLocation] = 'wp'
            board[endLocation] = tempRemovedPiece
    checkingForThreatened = False

    return validEndCheck

def blackPawnMovement(board, startLocation, endLocation):
    '''Rules for moving a black pawn.'''
    # White and black pawn functions might be combined, but would require extra effort. Could use a "turn" function.
    startRow = startLocation[0]
    endRow = endLocation[0]
    startColumn = startLocation[1]
    endColumn = endLocation[1]
    startRowIndex = rowString.find(startRow)
    # row 8 is index 8, row 1 is index 1
    startColumnIndex = columnString.find(startColumn)
    # column a is index 1, h is 8

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
                elif endColumn == columnString[startColumnIndex - 1] and board[endLocation].startswith('w'):  #diagonally to left. must contain white piece.
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
    
    global whiteKingInCheck
    global blackKingInCheck
    global checkingForThreatened
    if checkingForThreatened == False:
        if current_turn == 'b':
            tempRemovedPiece = board[endLocation]
            board[endLocation] = 'bp'
            board[startLocation] = ' '
            if blackKingCheck(board, globalBlackKing):
                print("Black King would be in check!")
                validEndCheck = False
            elif whiteKingCheck(board, globalWhiteKing):
                print(Fore.CYAN + "White King is in check!" + Fore.RESET)
                blackKingInCheck = True
            board[startLocation] = 'bp'
            board[endLocation] = tempRemovedPiece
    checkingForThreatened = False
    return validEndCheck

def rookMovement(board, startLocation, endLocation):
    '''Rules for moving a Rook.'''

    startRow = startLocation[0]
    endRow = endLocation[0]
    startColumn = startLocation[1]
    endColumn = endLocation[1]
    startRowIndex = rowString.find(startRow)
    endRowIndex = rowString.find(endRow)                         #  row 8 is index 8, row 1 is index 1
    startColumnIndex = columnString.find(startColumn)
    endColumnIndex = columnString.find(endColumn)                    # column a is index 1, h is 8

    # Could possibly use a 'turn' function instead. Also these rules can be written more concisely.
    # Could just use 'else' instead of elif, but 'elif' makes conditions clearer.
    if board[startLocation].startswith('w'):
        turn = 'w'
    elif board[startLocation].startswith('b'):
        turn = 'b'
    # First check that the endLocation can be moved to
    # If moving a black rook and the end location has a white piece or is empty, is valid

    if turn == 'b':
        if board[endLocation].startswith('w') or board[endLocation] == ' ':
            validEndCheck = True
        else:
            validEndCheck = False
            return validEndCheck

    elif turn == 'w':
        if board[endLocation].startswith('b') or board[endLocation] == ' ':
            validEndCheck = True
        else:
            validEndCheck = False
            return validEndCheck



    if startRow != endRow and startColumn != endColumn:     #Next check: either the rook must stay in the same row, or in the same column.
        validEndCheck = False
        return validEndCheck

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
        for i in range( min(startColumnIndex, endColumnIndex), max(startColumnIndex, endColumnIndex)):
            inBetweenSpaces.append(startRow + str(columnString[i]))
        del inBetweenSpaces[0]

    # Finally, check that the inbetween spaces are empty.
    for space in inBetweenSpaces:
        if board[space] != ' ':
            validEndCheck = False
            return validEndCheck

    # Finally, check whether any kings are placed in check. Temporarily move the piece in order to do this.
    global checkingForThreatened
    global whiteKingInCheck
    global blackKingInCheck
    if checkingForThreatened == False:
        if current_turn == 'w':
            tempRemovedPiece = board[endLocation]
            board[endLocation] = 'wR'
            board[startLocation] = ' '
            if whiteKingCheck(board, globalWhiteKing):
                print("White King would be in check!")
                validEndCheck = False
            elif blackKingCheck(board, globalBlackKing):
                print(Fore.RED + "Black King is in check!" + Fore.RESET)
                blackKingInCheck = True
            board[startLocation] = 'wR'
            board[endLocation] = tempRemovedPiece

        elif current_turn == 'b':     # Could just use 'else' here instead, but might be less clear. 
            tempRemovedPiece = board[endLocation]
            board[endLocation] = 'bR'
            board[startLocation] = ' '
            if blackKingCheck(board, globalBlackKing):
                print("Black King would be in check!")
                validEndCheck = False
            elif whiteKingCheck(board, globalWhiteKing):
                print(Fore.CYAN + "White King is in check!" + Fore.RESET)
                whiteKingInCheck = True
            board[startLocation] = 'bR'
            board[endLocation] = tempRemovedPiece
    checkingForThreatened = False
    # Return True at the end of function if all requirements are met.
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
    elif board[startLocation].startswith('b'):
        turn = 'b'

    if turn == 'b':              #first check that the endLocation can be moved to
        if board[endLocation].startswith('w') or board[endLocation] == ' ': #if moving a black bishop, if the end location has a white piece or is empty, return true
            validEndCheck = True
        else:
            validEndCheck = False
            return validEndCheck
    elif turn == 'w':
        if board[endLocation].startswith('b') or board[endLocation] == ' ':
            validEndCheck = True
        else:
            validEndCheck = False
            return validEndCheck
    inBetweenSpaces = []

    # If the bishop is moving diagonally up and to the right:
    if startRowIndex < endRowIndex and startColumnIndex < endColumnIndex:
        while True:
            # Increment the STARTING row and column until either the ENDING row or column is reached.
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
    elif startRowIndex > endRowIndex and startColumnIndex < endColumnIndex:
        while True:
            if startRowIndex == endRowIndex:
                break
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex -= 1
            startColumnIndex += 1
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex])
    
    # If moving diagonally up and to the left:
    elif startRowIndex < endRowIndex and startColumnIndex > endColumnIndex: 
        while True:
            if startRowIndex == endRowIndex:
                break
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex += 1
            startColumnIndex -= 1
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex])
    
    # If moving diagonally down and to the left:
    elif startRowIndex > endRowIndex and startColumnIndex > endColumnIndex: 
        while True:
            if startRowIndex == endRowIndex:
                break
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex -= 1
            startColumnIndex -= 1
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex])

    # Check that the end location is valid.
    if endLocation not in inBetweenSpaces:
        validEndCheck = False
        return validEndCheck
    
    # inBetweenSpaces[-1] is the destination space and can now be deleted, 
    # in order to check that the in between spaces are empty.
    del inBetweenSpaces[-1] 
    for space in inBetweenSpaces:
        if board[space] != ' ':
            validEndCheck = False
            return validEndCheck

    # Finally, check whether any kings are placed in check. Temporarily move the piece in order to do this.
    global checkingForThreatened
    global whiteKingInCheck
    global blackKingInCheck
    if checkingForThreatened == False:
        if current_turn == 'w':
            tempRemovedPiece = board[endLocation]
            board[endLocation] = 'wB'
            board[startLocation] = ' '
            if whiteKingCheck(board, globalWhiteKing):
                print("White King would be in check!")
                validEndCheck = False
            elif blackKingCheck(board, globalBlackKing):
                print(Fore.RED + "Black King is in check!" + Fore.RESET)
                blackKingInCheck = True
            board[startLocation] = 'wB'
            board[endLocation] = tempRemovedPiece

        elif current_turn == 'b':     # Could just use 'else' here instead, but might be less clear. 
            tempRemovedPiece = board[endLocation]
            board[endLocation] = 'bB'
            board[startLocation] = ' '
            if blackKingCheck(board, globalBlackKing):
                print("Black King would be in check!")
                validEndCheck = False
            elif whiteKingCheck(board, globalWhiteKing):
                print(Fore.CYAN + "White King is in check!" + Fore.RESET)
                whiteKingInCheck = True
            board[startLocation] = 'bB'
            board[endLocation] = tempRemovedPiece
    checkingForThreatened = False

    return validEndCheck

def knightMovement(board, startLocation, endLocation):
    '''Rules for moving a knight.'''

    startRow = startLocation[0]
    startColumn = startLocation[1]
    startRowIndex = rowString.find(startRow)
    # row 8 is index 8, row 1 is index 1
    startColumnIndex = columnString.find(startColumn)
    # column a is index 1, h is 8

    if board[startLocation].startswith('w'):
        turn = 'w'
    elif board[startLocation].startswith('b'):
        turn = 'b'

    if turn == 'b':              # first check that the endLocation can be moved to
        if board[endLocation].startswith('w') or board[endLocation] == ' ':
            validEndCheck = True
        else:
            validEndCheck = False
            return validEndCheck
    elif turn == 'w':
        if board[endLocation].startswith('b') or board[endLocation] == ' ':
            validEndCheck = True
        else:
            validEndCheck = False
            return validEndCheck

    # Making a list of the eight possible spaces a knight can move to.
    validEndLocations = []
    try:
        validEndLocations.append(rowString[startRowIndex + 2] + columnString[startColumnIndex + 1])
    # IndexError will occur if the knight is too close to the edge of the board i.e. the knight can't move off the board
    # This will happen if index > 8
    except IndexError:
        pass
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

    # Already checked earlier to make sure the endLocation was empty or has a piece of the opposite color.
    # Now just have to check that endLocation is valid.
    if endLocation in validEndLocations:
        validEndCheck = True
    else:
        validEndCheck = False
        return validEndCheck

    # Finally, check whether any kings are placed in check. Temporarily move the piece in order to do this.
    global checkingForThreatened
    global whiteKingInCheck
    global blackKingInCheck
    if checkingForThreatened == False:
        if current_turn == 'w':
            tempRemovedPiece = board[endLocation]
            board[endLocation] = 'wN'
            board[startLocation] = ' '
            if whiteKingCheck(board, globalWhiteKing):
                print("White King would be in check!")
                validEndCheck = False
            elif blackKingCheck(board, globalBlackKing):
                print(Fore.RED + "Black King is in check!" + Fore.RESET)
                blackKingInCheck = True
            board[startLocation] = 'wN'
            board[endLocation] = tempRemovedPiece

        elif current_turn == 'b':     # Could just use 'else' here instead, but might be less clear. 
            tempRemovedPiece = board[endLocation]
            board[endLocation] = 'bN'
            board[startLocation] = ' '
            if blackKingCheck(board, globalBlackKing):
                print("Black King would be in check!")
                validEndCheck = False
            elif whiteKingCheck(board, globalWhiteKing):
                print(Fore.CYAN + "White King is in check!" + Fore.RESET)
                whiteKingInCheck = True
            board[startLocation] = 'bN'
            board[endLocation] = tempRemovedPiece
    checkingForThreatened = False
    
    return validEndCheck

def queenMovement(board, startLocation, endLocation):
    '''Rules for moving a queen.'''

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
    elif board[startLocation].startswith('b'):
        turn = 'b'

    if turn == 'b':
        if board[endLocation].startswith('w') or board[endLocation] == ' ':
            validEndCheck = True
        else:
            validEndCheck = False
            return validEndCheck
    elif turn == 'w':
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
        # Check that the end location is valid.
        if endLocation not in inBetweenSpaces:
            validEndCheck = False
            return validEndCheck
        del inBetweenSpaces[-1]

    # If moving diagonally down and to the right:
    elif startRowIndex > endRowIndex and startColumnIndex < endColumnIndex:
        while True:
            if startRowIndex == endRowIndex:
                break
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex -= 1
            startColumnIndex += 1
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex])
        if endLocation not in inBetweenSpaces:
            validEndCheck = False
            return validEndCheck
        del inBetweenSpaces[-1]

    # If moving diagonally up and to the left:
    elif startRowIndex < endRowIndex and startColumnIndex > endColumnIndex: 
        while True:
            if startRowIndex == endRowIndex:
                break
            if startColumnIndex == endColumnIndex:
                break
            startRowIndex += 1
            startColumnIndex -= 1
            inBetweenSpaces.append(rowString[startRowIndex] + columnString[startColumnIndex])
        if endLocation not in inBetweenSpaces:
            validEndCheck = False
            return validEndCheck
        del inBetweenSpaces[-1]

    # If moving diagonally down and to the left:
    elif startRowIndex > endRowIndex and startColumnIndex > endColumnIndex: 
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
        del inBetweenSpaces[-1]

    elif startColumn == endColumn:
        for i in range(min(startRowIndex, endRowIndex), max(startRowIndex, endRowIndex)):
            inBetweenSpaces.append(str(rowString[i]) + startColumn)
        # inBetweenSpaces[0] will either be startLocation or endLocation.
        # Either way, it should be deleted, since it is not "in between".
        # Since the for loop counts up to, but doesn't include, the last space,
            # the remaining spaces in inBetweenSpaces are indeed the in between spaces.
        del inBetweenSpaces[0]

    elif startRow == endRow:
        for i in range(min(startColumnIndex, endColumnIndex), max(startColumnIndex, endColumnIndex)):
            inBetweenSpaces.append(startRow + str(columnString[i]))
        del inBetweenSpaces[0]

    # Finally, check that the inbetween spaces are empty.
    for space in inBetweenSpaces:
        if board[space] != ' ':
            validEndCheck = False
            return validEndCheck

    # Finally, check whether any kings are placed in check. Temporarily move the piece in order to do this.
    global checkingForThreatened
    global whiteKingInCheck
    global blackKingInCheck
    if checkingForThreatened == False:
        if current_turn == 'w':
            tempRemovedPiece = board[endLocation]
            board[endLocation] = 'wQ'
            board[startLocation] = ' '
            if whiteKingCheck(board, globalWhiteKing):
                print("White King would be in check!")
                validEndCheck = False
            elif blackKingCheck(board, globalBlackKing):
                print(Fore.RED + "Black King is in check!" + Fore.RESET)
                blackKingInCheck = True
            board[startLocation] = 'wQ'
            board[endLocation] = tempRemovedPiece

        elif current_turn == 'b':     # Could just use 'else' here instead, but might be less clear. 
            tempRemovedPiece = board[endLocation]
            board[endLocation] = 'bQ'
            board[startLocation] = ' '
            if blackKingCheck(board, globalBlackKing):
                print("Black King would be in check!")
                validEndCheck = False
            elif whiteKingCheck(board, globalWhiteKing):
                print(Fore.CYAN + "White King is in check!" + Fore.RESET)
                whiteKingInCheck = True
            board[startLocation] = 'bQ'
            board[endLocation] = tempRemovedPiece

    checkingForThreatened = False
    # If the code reaches this point, validEndCheck returns True (unless king in check makes it false).
    return validEndCheck

def kingMovement(board, startLocation, endLocation):
    '''Rules for moving a king.'''
    startRow = startLocation[0]
    startColumn = startLocation[1]
    startRowIndex = rowString.find(startRow)
    # row 8 is index 8, row 1 is index 1
    startColumnIndex = columnString.find(startColumn)
    # column a is index 1, h is 8

    if board[startLocation].startswith('w'):
        turn = 'w'
    elif board[startLocation].startswith('b'):
        turn = 'b'

    if turn == 'b':
        if board[endLocation].startswith('w') or board[endLocation] == ' ':
            validEndCheck = True
        else:
            validEndCheck = False
            return validEndCheck
    elif turn == 'w':
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

    if endLocation not in validEndLocations:
        validEndCheck = False
        return validEndCheck
    
    threatenedSpaces = []
    # turn must equal current_turn in order to avoid an infinite loop of checking whether kings can threaten a space!
    global checkingForThreatened
    global whiteKingInCheck
    global blackKingInCheck
    global globalWhiteKing
    global globalBlackKing
    if checkingForThreatened == False:
        if current_turn == 'w' and current_turn == turn:
            threatenedSpaces = threatenedByBlack(board)
            if endLocation in threatenedSpaces:
                print('King cannot enter that space! Space is threatened!')
                validEndCheck = False
                return validEndCheck
        if current_turn == 'b' and current_turn == turn:
            threatenedSpaces = threatenedByWhite(board)
            if endLocation in threatenedSpaces:
                print('King cannot enter that space! Space is threatened!')
                validEndCheck = False
                return validEndCheck

    # Finally, check whether any kings are placed in check. Temporarily move the piece in order to do this.
    # Already checked earlier to see if king could move into space without being threatened.
    if checkingForThreatened == False:
        if current_turn == 'w':
            tempRemovedPiece = board[endLocation]
            globalWhiteKing = endLocation
            board[endLocation] = 'wK'
            board[startLocation] = ' '
            if blackKingCheck(board, globalBlackKing):
                print(Fore.RED + "Black King is in check!" + Fore.RESET)
                blackKingInCheck = True
            board[startLocation] = 'wK'
            globalWhiteKing = startLocation
            board[endLocation] = tempRemovedPiece

        elif current_turn == 'b':     # Could just use 'else' here instead, but might be less clear. 
            tempRemovedPiece = board[endLocation]
            board[endLocation] = 'bK'
            globalBlackKing = endLocation
            board[startLocation] = ' '
            if whiteKingCheck(board, globalWhiteKing):
                print(Fore.CYAN + "White King is in check!" + Fore.RESET)
                whiteKingInCheck = True
            board[startLocation] = 'bK'
            globalBlackKing = startLocation
            board[endLocation] = tempRemovedPiece

    checkingForThreatened = False
    return validEndCheck

def threatenedByBlack(board):
    '''A function that makes a list of all spaces threatened by black pieces. 
    Only checks empty spaces.'''
    threatenedSpaces = []
    # First loop through all the potential threatening pieces. Only black pieces for this function.
    for startLocation, threateningPiece in board.items():
        global checkingForThreatened
        checkingForThreatened = True
        # For each threatening piece, starting with the black rook here:
        if threateningPiece == 'bR':
            # First find all empty spaces.
            for endLocation in board.keys():
                if board[endLocation] == ' ':
                    validEndCheck = rookMovement(board, startLocation, endLocation)
                    # After each check, reset the checkingForThreatened variable to True.
                    checkingForThreatened = True
                    # If the empty space is a valid movement location, add to threatened spaces.
                    if validEndCheck:
                        threatenedSpaces.append(endLocation)
        if threateningPiece == 'bB':
            for endLocation in board.keys():
                if board[endLocation] == ' ':
                    validEndCheck = bishopMovement(board, startLocation, endLocation)
                    checkingForThreatened = True
                    if validEndCheck:
                        threatenedSpaces.append(endLocation)
        if threateningPiece == 'bN':
            for endLocation in board.keys():
                if board[endLocation] == ' ':
                    validEndCheck = knightMovement(board, startLocation, endLocation)
                    checkingForThreatened = True
                    if validEndCheck:
                        threatenedSpaces.append(endLocation)
        if threateningPiece == 'bQ':
            for endLocation in board.keys():
                if board[endLocation] == ' ':
                    validEndCheck = queenMovement(board, startLocation, endLocation)
                    checkingForThreatened = True
                    if validEndCheck:
                        threatenedSpaces.append(endLocation)
        if threateningPiece == 'bK':
            for endLocation in board.keys():
                if board[endLocation] == ' ':
                    validEndCheck = kingMovement(board, startLocation, endLocation)
                    checkingForThreatened = True
                    if validEndCheck:
                        threatenedSpaces.append(endLocation)
        # Need to make a special case for pawns, since pawns cannot capture pieces directly in front of them.
        # Also, pawns can move diagonally only if a piece is present in that space!
        if threateningPiece == 'bp':
            for endLocation in board.keys():
                if board[endLocation] == ' ':
                    # Create a temporary "ghost" to check if the pawn can move diagonally to capture it.
                    board[endLocation] = 'wQ'
                    startColumn = startLocation[1]
                    endColumn = endLocation[1]
                    validEndCheck = blackPawnMovement(board, startLocation, endLocation)
                    checkingForThreatened = True
                    if validEndCheck and startColumn != endColumn:
                        threatenedSpaces.append(endLocation)
                    board[endLocation] = ' '
    return threatenedSpaces

def threatenedByWhite(board):
    threatenedSpaces = []
    
    # First loop through all the potential threatening pieces. Only white pieces for this function.
    for startLocation, threateningPiece in board.items():
        global checkingForThreatened
        checkingForThreatened = True
        # For each threatening piece, starting with the white rook here:
        if threateningPiece == 'wR':
            # First find all empty spaces.
            for endLocation in board.keys():
                if board[endLocation] == ' ':
                    validEndCheck = rookMovement(board, startLocation, endLocation)
                    # Reset the checkingForThreatened variable to true after each validEndCheck
                    checkingForThreatened = True
                    # If the empty space is a valid movement location, add to threatened spaces.
                    if validEndCheck:
                        threatenedSpaces.append(endLocation)
        if threateningPiece == 'wB':
            for endLocation in board.keys():
                if board[endLocation] == ' ':
                    validEndCheck = bishopMovement(board, startLocation, endLocation)
                    checkingForThreatened = True
                    if validEndCheck:
                        threatenedSpaces.append(endLocation)
        if threateningPiece == 'wN':
            for endLocation in board.keys():
                if board[endLocation] == ' ':
                    validEndCheck = knightMovement(board, startLocation, endLocation)
                    checkingForThreatened = True
                    if validEndCheck:
                        threatenedSpaces.append(endLocation)
        if threateningPiece == 'wQ':
            for endLocation in board.keys():
                if board[endLocation] == ' ':
                    validEndCheck = queenMovement(board, startLocation, endLocation)
                    checkingForThreatened = True
                    if validEndCheck:
                        threatenedSpaces.append(endLocation)
        if threateningPiece == 'wK':
            for endLocation in board.keys():
                if board[endLocation] == ' ':
                    validEndCheck = kingMovement(board, startLocation, endLocation)
                    checkingForThreatened = True
                    if validEndCheck:
                        threatenedSpaces.append(endLocation)
        # Need to make a special case for pawns, since pawns cannot capture pieces directly in front of them.
        # Also, pawns can move diagonally only if a piece is present in that space!
        if threateningPiece == 'wp':
            for endLocation in board.keys():
                if board[endLocation] == ' ':
                    # Create a temporary "ghost" to check if the pawn can move diagonally to capture it.
                    board[endLocation] = 'bQ'
                    startColumn = startLocation[1]
                    endColumn = endLocation[1]
                    validEndCheck = whitePawnMovement(board, startLocation, endLocation)
                    checkingForThreatened = True
                    if validEndCheck and startColumn != endColumn:
                        threatenedSpaces.append(endLocation)
                    board[endLocation] = ' '
    return threatenedSpaces

def whiteKingCheck(board, whiteKingLocation):
    '''Returns True if king at whiteKingLocation is in check.'''
    # run check at the end of every turn to see if king is in check
    # First, if current turn movement places your own king in check, then move is invalid
    # Second, look to see if enemy king is in check
    # If king is in check on current turn, only valid movement is movement that removes check
    # If no movement possible, then checkmate

    # King is in check if threatenedBy function lists the king's space as threatened

    # Next, check to see if king is threatened.
    # Need to be careful about king loops!
    global checkingForThreatened
    for startLocation, threateningPiece in board.items():
        if threateningPiece == 'bR':
            checkingForThreatened = True
            validEndCheck = rookMovement(board, startLocation, whiteKingLocation)
            if validEndCheck:
                return True
        if threateningPiece == 'bB':
            checkingForThreatened = True
            validEndCheck = bishopMovement(board, startLocation, whiteKingLocation)
            if validEndCheck:
                return True
        if threateningPiece == 'bN':
            checkingForThreatened = True
            validEndCheck = knightMovement(board, startLocation, whiteKingLocation)
            if validEndCheck:
                return True
        if threateningPiece == 'bQ':
            checkingForThreatened = True
            validEndCheck = queenMovement(board, startLocation, whiteKingLocation)
            if validEndCheck:
                return True
        if threateningPiece == 'bK':
            checkingForThreatened = True
            validEndCheck = kingMovement(board, startLocation, whiteKingLocation)
            if validEndCheck:
                return True
        if threateningPiece == 'bp':
            checkingForThreatened = True
            validEndCheck = blackPawnMovement(board, startLocation, whiteKingLocation)
            if validEndCheck:
                return True
    return False

def blackKingCheck(board, blackKingLocation):
    '''Returns True if blackKingLocation would place the black king in check.'''
    global checkingForThreatened
    for startLocation, threateningPiece in board.items():
        if threateningPiece == 'wR':
            checkingForThreatened = True
            validEndCheck = rookMovement(board, startLocation, blackKingLocation)
            if validEndCheck:
                return True
        if threateningPiece == 'wB':
            checkingForThreatened = True
            validEndCheck = bishopMovement(board, startLocation, blackKingLocation)
            if validEndCheck:
                return True
        if threateningPiece == 'wN':
            checkingForThreatened = True
            validEndCheck = knightMovement(board, startLocation, blackKingLocation)
            if validEndCheck:
                return True
        if threateningPiece == 'wQ':
            checkingForThreatened = True
            validEndCheck = queenMovement(board, startLocation, blackKingLocation)
            if validEndCheck:
                return True
        if threateningPiece == 'wK':
            checkingForThreatened = True
            validEndCheck = kingMovement(board, startLocation, blackKingLocation)
            if validEndCheck:
                return True
        if threateningPiece == 'wp':
            checkingForThreatened = True
            validEndCheck = blackPawnMovement(board, startLocation, blackKingLocation)
            if validEndCheck:
                return True
    return False

def checkmate(board, kingLocation):
    '''If a King is in check, this function checks for checkmate.'''
    global globalWhiteKing
    global whiteKingInCheck
    global blackKingInCheck
    global globalBlackKing
    global checkingForThreatened
    
    checkmate = False
    if whiteKingInCheck:
        checkmate = True
    if blackKingInCheck:
        checkmate = True

    while checkmate:
        if whiteKingInCheck and current_turn == 'w':
            for startLocation, piece in board.items():
                if checkmate == False:
                    break
                if piece == 'wK':
                    for endLocation in board.keys():
                        checkingForThreatened = True
                        validEndCheck = kingMovement(board, startLocation, endLocation)
                        if validEndCheck:
                            tempStart = board[startLocation]
                            tempEnd = board[endLocation]
                            board[startLocation] = ' '
                            board[endLocation] = 'wK'
                            globalWhiteKing = endLocation
                            checkingForThreatened = True
                            if whiteKingCheck(board, globalWhiteKing):
                                board[startLocation] = tempStart
                                board[endLocation] = tempEnd
                                globalWhiteKing = startLocation
                            else:
                                checkmate = False
                                break
                if piece == 'wR':
                    for endLocation in board.keys():
                        checkingForThreatened = True
                        validEndCheck = rookMovement(board, startLocation, endLocation)
                        if validEndCheck:
                            tempStart = board[startLocation]
                            tempEnd = board[endLocation]
                            board[startLocation] = ' '
                            board[endLocation] = 'wR'
                            checkingForThreatened = True
                            if whiteKingCheck(board, globalWhiteKing):
                                board[startLocation] = tempStart
                                board[endLocation] = tempEnd
                            else:
                                checkmate = False
                                break
                if piece == 'wB':
                    for endLocation in board.keys():
                        checkingForThreatened = True
                        validEndCheck = bishopMovement(board, startLocation, endLocation)
                        if validEndCheck:
                            tempStart = board[startLocation]
                            tempEnd = board[endLocation]
                            board[startLocation] = ' '
                            board[endLocation] = 'wB'
                            checkingForThreatened = True
                            if whiteKingCheck(board, globalWhiteKing):
                                board[startLocation] = tempStart
                                board[endLocation] = tempEnd
                            else:
                                checkmate = False
                                break
                if piece == 'wN':
                    for endLocation in board.keys():
                        checkingForThreatened = True
                        validEndCheck = knightMovement(board, startLocation, endLocation)
                        if validEndCheck:
                            tempStart = board[startLocation]
                            tempEnd = board[endLocation]
                            board[startLocation] = ' '
                            board[endLocation] = 'wN'
                            checkingForThreatened = True
                            if whiteKingCheck(board, globalWhiteKing):
                                board[startLocation] = tempStart
                                board[endLocation] = tempEnd
                            else:
                                checkmate = False
                                break
                if piece == 'wQ':
                    for endLocation in board.keys():
                        checkingForThreatened = True
                        validEndCheck = queenMovement(board, startLocation, endLocation)
                        if validEndCheck:
                            tempStart = board[startLocation]
                            tempEnd = board[endLocation]
                            board[startLocation] = ' '
                            board[endLocation] = 'wQ'
                            checkingForThreatened = True
                            if whiteKingCheck(board, globalWhiteKing):
                                board[startLocation] = tempStart
                                board[endLocation] = tempEnd
                            else:
                                checkmate = False
                                break
                if piece == 'wp':
                    for endLocation in board.keys():
                        checkingForThreatened = True
                        validEndCheck = whitePawnMovement(board, startLocation, endLocation)
                        if validEndCheck:
                            tempStart = board[startLocation]
                            tempEnd = board[endLocation]
                            board[startLocation] = ' '
                            board[endLocation] = 'wp'
                            checkingForThreatened = True
                            if whiteKingCheck(board, globalWhiteKing):
                                board[startLocation] = tempStart
                                board[endLocation] = tempEnd
                            else:
                                checkmate = False
                                break

        if blackKingInCheck and current_turn == 'b':
            for startLocation, piece in board.items():
                if checkmate == False:
                    break
                if piece == 'bK':
                    for endLocation in board.keys():
                        checkingForThreatened = True
                        validEndCheck = kingMovement(board, startLocation, endLocation)
                        if validEndCheck:
                            tempStart = board[startLocation]
                            tempEnd = board[endLocation]
                            board[startLocation] = ' '
                            board[endLocation] = 'bK'
                            globalBlackKing = endLocation
                            checkingForThreatened = True
                            if blackKingCheck(board, globalBlackKing):
                                board[startLocation] = tempStart
                                board[endLocation] = tempEnd
                                globalBlackKing = startLocation
                            else:
                                checkmate = False
                                break
                if piece == 'bR':
                    for endLocation in board.keys():
                        checkingForThreatened = True
                        validEndCheck = rookMovement(board, startLocation, endLocation)
                        if validEndCheck:
                            tempStart = board[startLocation]
                            tempEnd = board[endLocation]
                            board[startLocation] = ' '
                            board[endLocation] = 'bR'
                            checkingForThreatened = True
                            if blackKingCheck(board, globalBlackKing):
                                board[startLocation] = tempStart
                                board[endLocation] = tempEnd
                            else:
                                checkmate = False
                                break
                if piece == 'bB':
                    for endLocation in board.keys():
                        checkingForThreatened = True
                        validEndCheck = bishopMovement(board, startLocation, endLocation)
                        if validEndCheck:
                            tempStart = board[startLocation]
                            tempEnd = board[endLocation]
                            board[startLocation] = ' '
                            board[endLocation] = 'bB'
                            checkingForThreatened = True
                            if blackKingCheck(board, globalBlackKing):
                                board[startLocation] = tempStart
                                board[endLocation] = tempEnd
                            else:
                                checkmate = False
                                break
                if piece == 'bN':
                    for endLocation in board.keys():
                        checkingForThreatened = True
                        validEndCheck = knightMovement(board, startLocation, endLocation)
                        if validEndCheck:
                            tempStart = board[startLocation]
                            tempEnd = board[endLocation]
                            board[startLocation] = ' '
                            board[endLocation] = 'bN'
                            checkingForThreatened = True
                            if blackKingCheck(board, globalBlackKing):
                                board[startLocation] = tempStart
                                board[endLocation] = tempEnd
                            else:
                                checkmate = False
                                break
                if piece == 'bQ':
                    for endLocation in board.keys():
                        checkingForThreatened = True
                        validEndCheck = queenMovement(board, startLocation, endLocation)
                        if validEndCheck:
                            tempStart = board[startLocation]
                            tempEnd = board[endLocation]
                            board[startLocation] = ' '
                            board[endLocation] = 'bQ'
                            checkingForThreatened = True
                            if blackKingCheck(board, globalBlackKing):
                                board[startLocation] = tempStart
                                board[endLocation] = tempEnd
                            else:
                                checkmate = False
                                break
                if piece == 'bp':
                    for endLocation in board.keys():
                        checkingForThreatened = True
                        validEndCheck = blackPawnMovement(board, startLocation, endLocation)
                        if validEndCheck:
                            tempStart = board[startLocation]
                            tempEnd = board[endLocation]
                            board[startLocation] = ' '
                            board[endLocation] = 'bp'
                            checkingForThreatened = True
                            if blackKingCheck(board, globalBlackKing):
                                board[startLocation] = tempStart
                                board[endLocation] = tempEnd
                            else:
                                checkmate = False
                                break

        if checkmate:
            if current_turn == 'w':
                print(Fore.CYAN + 'Checkmate! White Loses!' + Fore.RED + ' Congratulations Black!' + Fore.RESET)
                return checkmate
            if current_turn == 'b':
                print(Fore.RED + 'Checkmate! Black Loses!' + Fore.CYAN + ' Congratulations White!' + Fore.RESET)
                return checkmate
        else:
            return checkmate


def whiteMove(board):
    '''This function asks what white piece to move to where. The function provides rules for valid movement.'''
    current_turn = 'w'
    while True:
        global whiteKingInCheck
        visualBoard(board)
        if whiteKingInCheck:
            print('White King is in check!')
            if checkmate(board, globalWhiteKing):
                raise Exception('Game Over!')
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
            endLocation = input('To what location would you like to move this piece? (' + Fore.CYAN + board[startLocation] + Fore.RESET + ')\n')  #after picking a valid start location, pick an end location confined by the movement rules
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
                print(Fore.GREEN + 'Invalid move!' + Fore.RESET)
                continue
            else:
                movePiece(board, piece, startLocation, endLocation)
                break

def blackMove(board):
    '''This function asks what black piece to move to where. The function provides rules for valid movement.'''
    current_turn = 'b'
    while True:
        global blackKingInCheck
        visualBoard(board)
        if blackKingInCheck:
            print('Black King is in check!')
            if checkmate(board, globalBlackKing):
                raise Exception('Game Over!')
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
            endLocation = input('To what location would you like to move this piece? (' + Fore.RED + board[startLocation] + Fore.RESET + ')\n')  #after picking a valid start location, pick an end location confined by the movement rules
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
                print(Fore.GREEN + 'Invalid move!' + Fore.RESET)
                continue
            else:
                movePiece(board, piece, startLocation, endLocation)
                break

# A test chessboard that can be set up for testing purposes.
testBoard = {'8a': 'bR', '8b': 'bB', '8c': 'bN', '8d': 'bQ', '8e': 'bK', '8f': 'bN', '8g': 'bB', '8h': 'bR',
    '7a': 'bp', '7b': 'bp', '7c': 'bp', '7d': ' ', '7e': 'bp', '7f': 'wR', '7g': 'bp', '7h': 'bp',
    '6a': 'wp', '6b': ' ', '6c': ' ', '6d': ' ', '6e': ' ', '6f': ' ', '6g': ' ', '6h': ' ',
    '5a': ' ', '5b': 'wK', '5c': ' ', '5d': ' ', '5e': ' ', '5f': ' ', '5g': ' ', '5h': ' ',
    '4a': ' ', '4b': ' ', '4c': ' ', '4d': ' ', '4e': ' ', '4f': ' ', '4g': ' ', '4h': ' ',
    '3a': 'bp', '3b': 'wp', '3c': ' ', '3d': ' ', '3e': ' ', '3f': ' ', '3g': ' ', '3h': ' ',
    '2a': 'wp', '2b': 'wp', '2c': 'wp', '2d': 'wp', '2e': 'wp', '2f': 'wN', '2g': 'wp', '2h': ' ',
    '1a': 'wR', '1b': 'wB', '1c': 'wN', '1d': 'wQ', '1e': ' ', '1f': 'wN', '1g': 'wB', '1h': ' '}

# Welcome Screen.
print('\n\n' + Fore.GREEN + Back.BLACK + ('~' * 131) + Fore.RESET + Back.RESET)
print('Welcome to Kevin\'s chess game! Be sure your window is wide enough to avoid graphical errors with the board!')
print('Type "exit" at any time to quit.')  # Exiting is inelegant, but works when entering start or end locations.
print('White player moves first. Piece locations are denoted by row, then column. E.g. the white King, "wK", is initially located at 1e.')
print(Fore.GREEN + Back.BLACK + ('~' * 131) + Fore.RESET + Back.RESET)

# Initialize the chessboard. Note that 'testBoard' can instead be used for debugging.
# May want to implement saving, instead of initializing board always.
chessInit(chessboard)

# Store the locations of the kings in a global variable. This variable is important for check and checkmate.
# Can change chessboard to testBoard here, for testing purposes.
# This is not a function, because it should only be executed once at the beginning of the game.
# Then the global variables of KingLocation can be updated as needed by other functions.
# Of course, this variable assumes only one king of each color is on the board (be wary when testing).
for location in testBoard.keys():
    if testBoard[location] == 'wK':
        globalWhiteKing = location
    if testBoard[location] == 'bK':
        globalBlackKing = location




# Main program loop. blackMove can be commented out for testing purposes.
# testBoard can be used instead of chessboard for testing.
while True:
    whiteMove(testBoard)
    blackMove(testBoard)



# Updated: 5/28/2020 6:20 pm


#TODO:
''' Rules for castling, for when a pawn reaches the opposite end of the board, rules for switching a bishop with a pawn,
rules for turn structure and winning, quitting out of the game, starting a new game, possibly AI movement'''
# Undo function?

# BUG: move queen down one space. Move king down one space. Checkmate results!






# UNUSED OR BROKEN CODE
#______________________________________________________________________________________________________
'''visualBoard(testBoard)
#try:
blackMove(testBoard)
#except Exception as exitMessage:
#    print(exitMessage)  # The except clause will still result in the remaining code being executed.
#try:
whiteMove(testBoard)
#except Exception as exitMessage:
#   print(exitMessage) # The except clause will still result in the remaining code being executed.

visualBoard(testBoard)'''


'''# Store the previous movement in a global variable, for use by the undo function.
undo =
undoCheck = '''
# def undoMove(board, piece, startLocation, endLocation)


# The following function can be useful for setting variables at the beginning of other functions.
# But it can create a whole lot of linter errors with unused variables. So using it is questionable.
# Possible fix is to have all variables be global, and this function declare changes to the global variables.
    # global startRow, endRow, startColumn, endColumn, startRowIndex, endRowIndex, startColumnIndex, endColumnIndex
# Easier fix is to just not use this function, and set local variables as needed.
'''def setStartEndIndices(startLocation, endLocation):'''
'''Useful variables that give the start and end rows and columns, as well as a system for indexing the rows and columns.'''
'''startRow = startLocation[0]
    endRow = endLocation[0]
    startColumn = startLocation[1]
    endColumn = endLocation[1]
    startRowIndex = rowString.find(startRow)
    endRowIndex = rowString.find(endRow)                         #  row 8 is index 8, row 1 is index 1
    startColumnIndex = columnString.find(startColumn)
    endColumnIndex = columnString.find(endColumn)                    # column a is index 1, h is 8
    return startRow, endRow, startColumn, endColumn, startRowIndex, endRowIndex, startColumnIndex, endColumnIndex'''