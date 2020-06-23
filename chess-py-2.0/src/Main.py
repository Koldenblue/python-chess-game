#!/usr/bin/python3

from Rook_class import Rook
from Piece_class import Piece
from Position_class import Position
from Board_class import Board

import sys

def main():
    chessboard = Board()
    bR1, bR2, wR1, wR2 = chessboard.board_init()
    chessboard.visual_board()
    black_turn = False

    # FOR TESTING:
    chessboard.move('a1', 'a2')


    # Game loop:
    while True:
        # Get input for movement:
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


# FOR TESTING:
chessboard = Board()
bR1, bR2, wR1, wR2 = chessboard.board_init()
chessboard.visual_board()
# print("\n")
# print(chessboard.space_list)
# print("\n", chessboard.space_dict, "\n")
print(chessboard.space_dict['a2'])
# print("\n")
# print(chessboard.piece_dict)
# print("\n")
print(chessboard.space_array)
# print("\n")
chessboard.space_points_ref()


