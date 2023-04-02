from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.board = self.createInitialBoard()
        self.enPassantTarget = None

    def __repr__(self):
        return "\n".join([" ".join([str(piece) if piece else "." for piece in row]) for row in self.board])

    def createInitialBoard(self):
        # Create an 8x8 chess board with the initial piece configuration
        board = [[None] * 8 for _ in range(8)]

        # Place pawns
        for i in range(8):
            board[1][i] = Pawn("black")
            board[6][i] = Pawn("white")

        # Place rooks
        board[0][0] = Rook("black")
        board[0][7] = Rook("black")
        board[7][0] = Rook("white")
        board[7][7] = Rook("white")

        # Place knights
        board[0][1] = Knight("black")
        board[0][6] = Knight("black")
        board[7][1] = Knight("white")
        board[7][6] = Knight("white")

        # Place bishops
        board[0][2] = Bishop("black")
        board[0][5] = Bishop("black")
        board[7][2] = Bishop("white")
        board[7][5] = Bishop("white")

        # Place queens
        board[0][3] = Queen("black")
        board[7][3] = Queen("white")

        # Place kings
        board[0][4] = King("black")
        board[7][4] = King("white")

        return board

    def movePiece(self, start, end):
        startX, startY = start
        endX, endY = end
        piece = self.board[startY][startX]

        if piece and piece.isValidMove(start, end, self.board):
            # En passant capture
            if isinstance(piece, Pawn) and (endX, startY) == self.enPassantTarget:
                self.board[startY][endX] = None

            # Move the piece to the destination square
            self.board[endY][endX] = piece
            self.board[startY][startX] = None

            # Update the piece's hasMoved status
            piece.hasMoved = True

            # Update the enPassantTarget if a pawn makes a two-step move
            forward = -1 if piece.color == "white" else 1
            if isinstance(piece, Pawn) and abs(startY - endY) == 2:
                self.enPassantTarget = (endX, endY - forward)
            else:
                self.enPassantTarget = None

            return True
        else:
            return False
    
    def isCheck(self, color):
        kingPos = None
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if isinstance(piece, King) and piece.color == color:
                    kingPos = (x, y)
                    break
            if kingPos:
                break

        if not kingPos:
            raise ValueError("No king found for the given color")

        return kingPos and any(
            piece
            and piece.color != color
            and piece.isValidMove((x, y), kingPos, self.board)
            for y, row in enumerate(self.board)
            for x, piece in enumerate(row)
        )
    
    def isCheckmate(self, color):
        if not self.isCheck(color):
            return False

        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece and piece.color == color:
                    for endY, endRow in enumerate(self.board):
                        for endX, _ in enumerate(endRow):
                            if self.move_piece((x, y), (endX, endY)):
                                self.move_piece((endX, endY), (x, y))
                                if not self.isCheck(color):
                                    return False
        return True

    def isInCheck(self, color):
        king_position = None

        # Find the king's position
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece and piece.color == color and isinstance(piece, King):
                    king_position = (x, y)
                    break
            if king_position:
                break

        # Check if any opponent's piece can move to the king's position
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece and piece.color != color and piece.isValidMove((x, y), king_position, self.board):
                    return True

        return False

    def isStalemate(self, color):
        if not self.isInCheck(color):
            for y in range(8):
                for x in range(8):
                    piece = self.board[y][x]
                    if piece and piece.color == color:
                        for end_y in range(8):
                            for end_x in range(8):
                                if piece.isValidMove((x, y), (end_x, end_y), self.board):
                                    # Make a temporary move to see if the player is still in check after the move
                                    original_end_piece = self.board[end_y][end_x]
                                    self.board[end_y][end_x] = piece
                                    self.board[y][x] = None

                                    if not self.isInCheck(color):
                                        # Undo the temporary move
                                        self.board[y][x] = piece
                                        self.board[end_y][end_x] = original_end_piece
                                        return False

                                    # Undo the temporary move
                                    self.board[y][x] = piece
                                    self.board[end_y][end_x] = original_end_piece

        return True


chess_board = Board()
