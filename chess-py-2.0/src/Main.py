from Rook_class import Rook
from Piece_class import Piece
from Position_class import Position
from Board_class import Board



chessboard = Board()
chessboard.space_points_ref()

bR1, bR2, wR1, wR2 = chessboard.board_init()

print(wR1.rook_move(Position(1,2)))
print(bR1.rook_move(Position(1,0)))
print(bR1.piece.position.column)

chessboard.visual_board()