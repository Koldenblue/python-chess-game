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
    game_over = False

    # Game loop:
    while True:
        if not black_turn:
            turn = "white"
            enemy = "black"
        else:
            turn = "black"
            enemy = "white"
        print(chessboard)

        if king_checked:
            print("{0} king is in check.".format(turn.title()))
            game_over = chessboard.checkmates_king(black_turn)
        if game_over:
            print(f"GAME OVER! CHECKMATE! {enemy.upper()} WINS!")
            break

        # First, get player movement input.
        start_posn = move_input(chessboard, "Start")
        start_column, start_row = chessboard.get_indices(start_posn)
        # Validate that the correct color piece is moved.
        if chessboard.space_array[start_column][start_row].black != black_turn:
            print(f"Invalid move! You must choose a {turn} piece to move!")
            continue
        end_posn = move_input(chessboard, "End")
        end_column, end_row = chessboard.get_indices(end_posn)

        # Validate the movement of the piece.
        if not chessboard.validate_move(start_column, start_row, end_column, end_row):
            print("Invalid movement!")
            continue

        # Find if any kings are placed in check.
        bK, wK = chessboard.checks_kings(start_column, start_row, end_column, end_row)
        if not king_checked:
            if black_turn and bK.in_check:
                print(f"Invalid move! Friendly {turn} king would be placed in check.")
                continue
            if not black_turn and wK.in_check:
                print(f"Invalid move! Friendly {turn} king would be placed in check.")
                continue
        else:
            if black_turn and bK.in_check:
                print(f"Invalid move! Friendly {turn} king is still in check.")
                continue
            if not black_turn and wK.in_check:
                print(f"Invalid move! Friendly {turn} king is still in check.")
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


def move_input(chessboard, start_end):
    '''Gets start or end locations from the player. Chessboard is a Board object.
    start_end is a string equal to "Start" or "End".'''
    while True:
        posn = input(f"{start_end} location? Type \"board\" at any time to view the board.\n")
        posn = posn.lower().strip()
        if posn == "board":
            chessboard.visual_board()
            continue
        elif posn in chessboard.space_list:
            pass
        else:
            print("Invalid location!")
            continue
        
        #TODO: return "undo" to restart movement
        return posn


def test():
    '''Prints out board lists and calls board functions for testing.'''
    chessboard = Board()
    chessboard.test_init()
    black_turn = False
    king_checked = False
    
    print(chessboard, '\n\n')
    print("SPACE ARRAY")
    print(chessboard.space_array, '\n\n')
    print("SPACE LIST")
    print(chessboard.space_list, '\n\n')
    print("SPACE DICT")
    print(chessboard.space_dict, "\n\n")
    print("LOCATION ARRAY")
    print(chessboard.location_array)
    chessboard.space_points_ref()


    # Game loop:
    while True:
        if not black_turn:
            turn = "white"
            enemy = "black"
        else:
            turn = "black"
            enemy = "white"
        print(chessboard)
        game_over = False
        print(f"GAME OVER! CHECKMATE! {enemy.upper()} WINS!")
        if king_checked:
            print("{0} king is in check.".format(turn.title()))
            game_over = chessboard.checkmates_king(black_turn)
        if game_over:
            print(f"GAME OVER! CHECKMATE! {enemy.upper()} WINS!")
            break

        # First, get player movement input.
        start_posn = move_input(chessboard, "Start")
        start_column, start_row = chessboard.get_indices(start_posn)
        # Validate that the correct color piece is moved.
        if chessboard.space_array[start_column][start_row].black != black_turn:
            print(f"Invalid move! You must choose a {turn} piece to move!")
            continue
        end_posn = move_input(chessboard, "End")
        end_column, end_row = chessboard.get_indices(end_posn)

        # Validate the movement of the piece.
        if not chessboard.validate_move(start_column, start_row, end_column, end_row):
            print("Invalid movement!")
            continue

        # Find if any kings are placed in check.
        bK, wK = chessboard.checks_kings(start_column, start_row, end_column, end_row)
        if not king_checked:
            if black_turn and bK.in_check:
                print(f"Invalid move! Friendly {turn} king would be placed in check.")
                continue
            if not black_turn and wK.in_check:
                print(f"Invalid move! Friendly {turn} king would be placed in check.")
                continue
        else:
            if black_turn and bK.in_check:
                print(f"Invalid move! Friendly {turn} king is still in check.")
                continue
            if not black_turn and wK.in_check:
                print(f"Invalid move! Friendly {turn} king is still in check.")
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


test()
#main()




'''
BUGS:
Making chessboard = Board() and then running boardinit(), then running main() seems to not work?
May be a problem for game restart.
'''

'''
WORKING:
pawn capture pieces
pawn and rook movement
'''

'''
POSSIBLE FEATURES:
movement hints to get out of check
'''

'''
TODO:
convert chessboard.visual_board() to print(chessboard)
'''
