#!/usr/bin/python3

from Rook_class import Rook
from Piece_class import Piece
from Position_class import Position
from Board_class import Board
from King_class import King

import sys

def main():
    chessboard = Board()
    chessboard.board_init()
    black_turn = False
    king_checked = False

    # Game loop:
    while True:
        if not black_turn:
            turn = "white"
        else:
            turn = "black"
        chessboard.visual_board()

        # If friendly king is in check, movement is restricted...
        if king_checked:
            print("{0} king is in check.".format(turn.title()))

        # First, get player movement input.
        start_posn, end_posn = move_input(chessboard)
        start_column, start_row = chessboard.get_indices(start_posn)
        end_column, end_row = chessboard.get_indices(end_posn)

        # Validate that the correct color piece is moved.
        if chessboard.space_array[start_column][start_row].black != black_turn:
            print(f"Invalid move! You must choose a {turn} piece to move!")
            continue

        # Validate the movement of the piece.
        if not chessboard.validate_move(start_column, start_row, end_column, end_row):
            print("Invalid movement!")
            continue

        # Find if any kings are placed in check.
        wK, bK = chessboard.eval_check(start_column, start_row, end_column, end_row)
        if black_turn and bK.in_check:
            print(f"Invalid move! Friendly {turn} king would be placed in check.")
            continue
        if not black_turn and wK.in_check:
            print(f"Invalid move! Friendly {turn} king would be placed in check.")
            continue

        # Move the piece.
        chessboard.move(start_column, start_row, end_column, end_row)

        # If an enemy king is placed in check, note the gamestate, and find if checkmate has occurred.
        if black_turn and wK.in_check:
            king_checked = True
        elif not black_turn and bK.in_check:
            king_checked = True
        else:
            king_checked = False

        # Finally, switch turns.
        if black_turn == False:
            black_turn = True
        else:
            black_turn = False

def move_input(chessboard):
    '''Gets start and end locations from the player.'''
    while True:
        start_posn = input("Start location? Type \"board\" at any time to view the board and restart movement input.\n")
        start_posn = start_posn.lower().strip()
        if start_posn == "board":
            chessboard.visual_board()
            continue
        elif start_posn in chessboard.space_list:
            pass
        else:
            print("Invalid location!")
            continue

        end_posn = input("End location?\n")
        end_posn = end_posn.lower().strip()
        if end_posn == "board":
            chessboard.visual_board()
            continue
        elif end_posn in chessboard.space_list:
            pass
        else:
            print("Invalid location!")
            continue
        return start_posn, end_posn

main()


# TEST CODE:
# chessboard.move('a1', 'a2')
#print(chessboard.space_array)
#chessboard.space_points_ref()
# END TEST CODE

# TEST CODE:
for column, piece_list in enumerate(chessboard.space_array):
    for row in range(len(piece_list)):
        print(chessboard.space_array[column][row].black)
for column, row in enumerate(chessboard.space_array):
    print("index = " + str(column))
    print("value = " + str(row))

print("\n\n")
for column in chessboard.space_array:
    for piece in column:
        print(piece)
chessboard = Board()
chessboard.board_init()
chessboard.visual_board()
# print("\n")
# print(chessboard.space_list)
# print("\n", chessboard.space_dict, "\n")
print(chessboard.space_dict['a2'])
# print("\n")
# print(chessboard.piece_dict)
# print("\n")
# print("\n")
# END TEST CODE


