from Rook_class import Rook
from Piece_class import Piece
from Position_class import Position
from Board_class import Board



chessboard = Board()
chessboard.board_init()
print(chessboard.space_list)
print("\n", chessboard.space_dict, "\n")
print(chessboard.space_dict['a2'])

chessboard.space_points_ref()

print(chessboard.space_array)


bR1, bR2, wR1, wR2 = chessboard.board_init()


print(bR1.rook_move(Position(1, 0)))
print(bR1.black)

#chessboard.visual_board()
