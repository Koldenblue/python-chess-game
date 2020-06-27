#!/usr/bin/python3

from Rook_class import Rook
from Piece_class import Piece
from Position_class import Position
from Board_class import Board

import sys

def main():
    chessboard = Board()
    chessboard.board_init()
    chessboard.visual_board()
    black_turn = False

    # TEST CODE:
    # chessboard.move('a1', 'a2')
    print(chessboard.space_array)
    chessboard.eval_check()
    chessboard.space_points_ref()


    # END TEST CODE


    # Game loop:
    while True:
        # Get input for movement:
        #TODO: add black or white turns
        start_posn = input("start location?")
        if start_posn.lower() in chessboard.space_list:
            pass
        else:
            print("Invalid location!")
            continue

        end_posn = input("end location?")
        if end_posn.lower() in chessboard.space_list:
            pass
        else:
            print("Invalid location!")
            continue

        # Check to see if move is valid. If so, move the piece and switch turns.
        successful_move = chessboard.move(start_posn, end_posn)
        if successful_move:
            if black_turn == False:
                black_turn = True
            else:
                black_turn = False
        else:
            print("Invalid movement!")

main()





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


