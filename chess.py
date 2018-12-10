"""IS590PR2 Friday section, Spring 2018
In-class example development of OO class to represent Chess games.
"""


class ChessPiece:

    # This is a PROTECTED class variable, because we don't want
    # any code outside the class (or its pollinator_types to be able to
    # directly see or modify it:
    __all_pieces = []

    def __init__(self, color, location=None):
        self.color = color
        self.location = location
        ChessPiece.__all_pieces.append(self)

    @staticmethod
    def clear_board():
        ChessPiece.__all_pieces = []

    @staticmethod
    def setup_pieces():
        Rook('black', 'a1')
        Rook('black', 'h1')
        Knight('black', 'b1')
        Knight('black', 'g1')
        Bishop('black', 'c1')
        Bishop('black', 'f1')
        King('black', 'd1')
        Queen('black', 'e1')

        Pawn('black', 'a2')
        Pawn('black', 'b2')
        Pawn('black', 'c2')
        Pawn('black', 'd2')
        Pawn('black', 'e2')
        Pawn('black', 'f2')
        Pawn('black', 'g2')
        Pawn('black', 'h2')

    @staticmethod
    def list_pieces():
        for p in ChessPiece.__all_pieces:
            print(p)

    def __str__(self) -> str:
        return '{} {} {}'.format(
                self.color, self.__class__.__name__, self.location)

    def __repr__(self):
        return "ChessPiece('{}', '{}', '{}')".format(
                self.color, self.__class__.__name__, self.location)

    @staticmethod
    def get_piece_at(location: str) -> 'ChessPiece':
        """Get the ChessPiece at a specific location, or None if empty.
        :param location: a board position string. e.g. 'a1' or 'f6'
        :return: ChessPiece | None
        """
        for p in ChessPiece.__all_pieces:
            if p.location == location:
                return p
        return None

    def move(self, destination: str):
        # TODO: is there already a piece there?
        p = ChessPiece.get_piece_at(destination)
        if p is not None:
            if p.color == self.color:
                raise ValueError('Can\'t move onto our own piece!')
                return
            else:
                # We can capture that piece!
                p.remove()
        # Now update the moved piece's location:
        self.location = destination

    def remove(self):
        print(self, 'was captured. Removing it from game.')
        ChessPiece.__all_pieces.remove(self)


class King(ChessPiece):

    def move(self, destination: str):
        # TODO: check here if this new destination is valid.

        print('moving the king...')

        # Call the superclass implementation of move()
        #   for the details that are always the same:
        super().move(destination)

    def castle(self, which_rook):
        """The castle method only is available to the King
        (and affects a Rook), so this method shouldn't exist in ChessPiece.
        :param which_rook:
        :return:
        """
        pass


class Queen(ChessPiece):
    pass


class Bishop(ChessPiece):
    pass


class Knight(ChessPiece):
    pass


class Rook(ChessPiece):
    pass


class Pawn(ChessPiece):
    pass


if __name__ == '__main__':

    ChessPiece.setup_pieces()

    black_king = ChessPiece.get_piece_at('d1')
    print(black_king)
    try:
        black_king.move('d2')  # this should produce an exception.
    except ValueError:
        print('oops, we can\'t move there.  Let\'s try moving the pawn instead.')
        pawn_d = ChessPiece.get_piece_at('d2')
        pawn_d.move('d4')  # advance pawn 2 ranks instead.

    ChessPiece.list_pieces()  # show all the pieces.  (I didn't implement the white ones yet.)






