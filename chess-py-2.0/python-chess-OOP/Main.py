from Rook_class import Rook
from Piece_class import Piece
from Position_class import Position


bR1 = Rook(Piece(True, 'rook', Position(0,0)))
bR2 = Rook(Piece(True, 'rook', Position(7,0)))
wR1 = Rook(Piece(False, 'rook', Position(0,7)))
wR2 = Rook(Piece(False, 'rook', Position(7,7)))

print(bR1.rook_move(Position(1,0)))
print(bR1.piece.position.column)