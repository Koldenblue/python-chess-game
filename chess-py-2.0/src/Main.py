from Rook_class import Rook
from Piece_class import Piece
from Position_class import Position
from Board_class import Board



chessboard = Board()
bR1, bR2, wR1, wR2 = chessboard.board_init()
print("\n")
print(chessboard.space_list)
print("\n", chessboard.space_dict, "\n")
print(chessboard.space_dict['a2'])
print("\n")
print(chessboard.piece_dict)
print("\n")
print(chessboard.space_array)
print("\n")


chessboard.space_points_ref()

chessboard.visual_board()
