class Piece:
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return f"{self.color} {self.__class__.__name__.lower()}"

    def isValidMove(self, start, end, board):
        raise NotImplementedError("Must be implemented in subclass")


class Pawn(Piece):
    def isValidMove(self, start, end, board):
        startX, startY = start
        endX, endY = end
        dX = endX - startX
        dY = endY - startY

        if self.color == "white":
            forward = -1
        else:
            forward = 1

        # Check if the move is a one-step forward move
        if dX == 0 and dY == forward and board[endY][endX] is None:
            return True

        # Check if the move is a two-step forward move for pawns on their initial squares
        if (
            dX == 0
            and dY == 2 * forward
            and board[endY][endX] is None
            and board[endY - forward][endX] is None
            and (startY == 6 if self.color == "white" else startY == 1)
        ):
            return True

        # Check if the move is a capture (diagonal move)
        if (
            abs(dX) == 1
            and dY == forward
            and board[endY][endX] is not None
            and board[endY][endX].color != self.color
        ):
            return True

        # Check if the move is en passant capture
        if (
            abs(dX) == 1
            and dY == forward
            and board[endY][endX] is None
            and board[startY][endX] is not None
            and isinstance(board[startY][endX], Pawn)
            and board[startY][endX].color != self.color
            and (endX, startY) == board.enPassantTarget
        ):
            return True

        return False


class Knight(Piece):
    def isValidMove(self, start, end, board):
        startX, startY = start
        endX, endY = end
        dX = abs(endX - startX)
        dY = abs(endY - startY)

        # Check if the move is an L-shaped move (two squares in one direction and one square in the other direction)
        if (dX == 2 and dY == 1) or (dX == 1 and dY == 2):
            destinationPiece = board[endY][endX]

            # Check if the destination square is either empty or contains an opponent's piece
            if destinationPiece is None or destinationPiece.color != self.color:
                return True

        return False


class Bishop(Piece):
    def isValidMove(self, start, end, board):
        startX, startY = start
        endX, endY = end
        dX = abs(endX - startX)
        dY = abs(endY - startY)

        # Check if the move is a diagonal move
        if dX == dY:
            xStep = 1 if endX > startX else -1
            yStep = 1 if endY > startY else -1

            x, y = startX + xStep, startY + yStep
            while x != endX and y != endY:
                # Check if there are any pieces between the start and end squares
                if board[y][x] is not None:
                    return False
                x += xStep
                y += yStep

            destinationPiece = board[endY][endX]

            # Check if the destination square is either empty or contains an opponent's piece
            if destinationPiece is None or destinationPiece.color != self.color:
                return True

        return False

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hasMoved = False

    def isValidMove(self, start, end, board):
        startX, startY = start
        endX, endY = end
        dX = abs(endX - startX)
        dY = abs(endY - startY)

        # Check if the move is a horizontal or vertical move
        if dX == 0 or dY == 0:
            xStep = 1 if endX > startX else -1 if endX < startX else 0
            yStep = 1 if endY > startY else -1 if endY < startY else 0

            x, y = startX + xStep, startY + yStep
            while x != endX or y != endY:
                # Check if there are any pieces between the start and end squares
                if board[y][x] is not None:
                    return False
                x += xStep
                y += yStep

            destinationPiece = board[endY][endX]

            # Check if the destination square is either empty or contains an opponent's piece
            if destinationPiece is None or destinationPiece.color != self.color:
                return True

        return False

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.hasMoved = False

    def isValidMove(self, start, end, board):
        startX, startY = start
        endX, endY = end
        dX = abs(endX - startX)
        dY = abs(endY - startY)

        # Check if the move is a single square move in any direction
        if dX <= 1 and dY <= 1:
            destinationPiece = board[endY][endX]

            # Check if the destination square is either empty or contains an opponent's piece
            if destinationPiece is None or destinationPiece.color != self.color:
                return True

        # Implement castling rules
        if not self.hasMoved and dY == 0:
            rook = None
            if dX == 2:  # Kingside castling
                rook = board[startY][7]
                rookStart = (7, startY)
                rookEnd = (5, startY)
            elif dX == 3:  # Queenside castling
                rook = board[startY][0]
                rookStart = (0, startY)
                rookEnd = (3, startY)

            if rook and isinstance(rook, Rook) and not rook.hasMoved:
                # Check if there are no pieces between the king and the rook
                xRange = range(min(startX, endX) + 1, max(startX, endX))
                if all(board[startY][x] is None for x in xRange):
                    # Check if the squares the king moves through are not under attack
                    if not any(self.isSquareUnderAttack((x, startY), board) for x in xRange):
                        # Move the rook as part of the castling move
                        board[rookEnd[1]][rookEnd[0]] = rook
                        board[rookStart[1]][rookStart[0]] = None
                        return True

        return False

    def isSquareUnderAttack(self, square, board):
        x, y = square
        for i, row in enumerate(board):
            for j, piece in enumerate(row):
                if piece and piece.color != self.color and piece.isValidMove((j, i), square, board):
                    return True
        return False


class Queen(Piece):
    def isValidMove(self, start, end, board):
        startX, startY = start
        endX, endY = end
        dX = abs(endX - startX)
        dY = abs(endY - startY)

        # Check if the move is a diagonal, horizontal, or vertical move
        if dX == dY or dX == 0 or dY == 0:
            xStep = 1 if endX > startX else -1 if endX < startX else 0
            yStep = 1 if endY > startY else -1 if endY < startY else 0

            x, y = startX + xStep, startY + yStep
            while x != endX or y != endY:
                # Check if there are any pieces between the start and end squares
                if board[y][x] is not None:
                    return False
                x += xStep
                y += yStep

            destinationPiece = board[endY][endX]

            # Check if the destination square is either empty or contains an opponent's piece
            if destinationPiece is None or destinationPiece.color != self.color:
                return True

        return False
