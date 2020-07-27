""" The ChessEngine class is responsible for storing game info. It will also
store and apply the moves that pieces can make. Lastly, it will store a
move log (the backend).
"""

class GameState(object):
    """ The Gamestate class saves the state of the game (duh!). Is used
    to keep track of when the game will end and which pieces can move
    where.
    """

    def __init__(self):
        # gameboard is a 2d list
        # pieces are named by color (lowercase) and type (uppercase)
        # empty pieces are named '--'
        self.generatorFunctions = {
            'P': self._generate_pawn_moves, 'R': self._generate_rook_moves,
            'N': self._generate_knight_moves, 'B': self._generate_bishop_moves,
            'K': self._generate_king_moves, 'Q': self._generate_queen_moves}
        self.gameboard = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP' for i in range(8)],
            ['--' for i in range(8)],
            ['--' for i in range(8)],
            ['--' for i in range(8)],
            ['--' for i in range(8)],
            ['wP' for i in range(8)],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.whiteTurn = True
        self.moveLog = []  # a list of Move() objects
        self.piecesCaptured = []  # a list of str of all captured pieces
        self.wKLocation = (7, 4)    # white king pos stored as (row, col)
        self.bKLocation = (0, 4)    # black king pos stored as (row, col)
        self.enpassantSquare = ()   # the square where a en passant capture is possible
        # keep track of castle rights
        self.currentCastleRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(True, True, True, True)]

    def reset_gamestate(self):
        self.gameboard = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP' for i in range(8)],
            ['--' for i in range(8)],
            ['--' for i in range(8)],
            ['--' for i in range(8)],
            ['--' for i in range(8)],
            ['wP' for i in range(8)],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.whiteTurn = True
        self.moveLog = []
        self.piecesCaptured = []
        self.wKLocation = (7, 4)
        self.bKLocation = (0, 4)
        self.enpassantSquare = ()
        self.currentCastleRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(True, True, True, True)]

    def update_kings_position(self):
        for row in range(len(self.gameboard)):
            for col in range(len(self.gameboard[row])):
                if self.gameboard[row][col][1] == 'K':
                    if self.gameboard[row][col][0] == 'w':
                        self.wKLocation = (row, col)
                    else:
                        self.bKLocation = (row, col)

    def move_piece(self, move):
        """ Takes a move as a parameter and executes it. It takes the special cases from
        pawn promotion, castling and en passant. """
        self.gameboard[move.start_row][move.start_col] = '--'  # set the starting position empty
        if move.pieceCaptured not in self.piecesCaptured:
            self.piecesCaptured.append(move.pieceCaptured)  # add captured piece to piecesCaptured
        self.gameboard[move.end_row][move.end_col] = move.pieceMoved  # set the ending position to the moved piece
        self.moveLog.append(move)  # add move to move log

        # action for pawn promotion
        if move.isPawnPromotion:
            self.gameboard[move.end_row][move.end_col] = move.pieceMoved[0] + move.promotion_piece

        # action for en passant
        if move.enPassantMove:
            # setting the captured piece to the pawn is handled by the Move class
            # delete the piece after capturing it in en passant
            self.gameboard[move.start_row][move.end_col] = '--'

        # action for castle move
        if move.isCastle:
            color = 'w' if self.whiteTurn else 'b'
            if move.end_col == move.start_col + 2:  # the castle is kingside
                # move the rook to the new position
                self.gameboard[move.end_row][move.end_col - 1] = color + 'R'
                # replace the old rook position as empty
                self.gameboard[move.end_row][move.end_col + 1] = '--'
            else:   # the castle is queenside
                # move the rook to the new position
                self.gameboard[move.end_row][move.end_col + 1] = color + 'R'
                # replace the old rook position as empty
                self.gameboard[move.end_row][move.end_col - 2] = '--'

        # update castling rights whenever a king or a rook is moved
        self.update_castle_rights(move)

        self.update_kings_position()    # update king pos
        self.whiteTurn = not self.whiteTurn  # switch the turn


    def undo_move(self):
        """ This will undo the last move made"""
        if len(self.moveLog) > 0:
            move = self.moveLog.pop()  # remove move from log
            self.gameboard[move.start_row][move.start_col] = move.pieceMoved  # replace moved piece
            self.gameboard[move.end_row][move.end_col] = move.pieceCaptured  # replaced captured piece

            if move.enPassantMove:  # undo en passant move
                # replace the piece that was captured
                if self.whiteTurn:
                    self.gameboard[move.end_row - 1][move.end_col] = 'wP'
                else:
                    self.gameboard[move.end_row + 1][move.end_col] = 'bP'
                # reset the enpassant square to what it was before
                self.enpassantSquare = (move.end_row, move.end_col)

            if move.isCastle:   # undo castle move
                color = 'w' if not self.whiteTurn else 'b'
                if move.end_col == move.start_col + 2:  # the castle is kingside
                    # set the previous rook location empty
                    self.gameboard[move.end_row][move.end_col - 1] = '--'
                    # replace the old rook position with the rook
                    self.gameboard[move.end_row][move.end_col + 1] = color + 'R'
                else:  # the castle is queenside
                    # set the previous rook location empty
                    self.gameboard[move.end_row][move.end_col + 1] = '--'
                    # replace the old rook position with the rook
                    self.gameboard[move.end_row][move.end_col - 2] = color + 'R'

            # undo castle rights
            log = self.castleRightsLog.pop()  # get rid of the most recent castle right
            # set the current castle right to the one before
            self.currentCastleRights = CastleRights(log.wks, log.bks, log.wqs, log.bqs)

            self.update_kings_position()    # update kings position
            self.whiteTurn = not self.whiteTurn  # switch the turn


    def update_castle_rights(self, move):
        """ method updates if a king or rook has moved and given up its
        castling right. Does not track if king is in check or empty spaces
        """
        if move.pieceMoved == 'wK':
            self.currentCastleRights.wks = False
            self.currentCastleRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastleRights.bks = False
            self.currentCastleRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.start_row == 7:
                if move.start_col == 7:     # right rook
                    self.currentCastleRights.wks = False
                elif move.start_col == 0:   # left rook
                    self.currentCastleRights.wqs = False
        elif move.pieceMoved == 'bR':
            if move.start_row == 0:
                if move.start_col == 7:     # right rook
                    self.currentCastleRights.bks = False
                elif move.start_col == 0:  # left rook
                    self.currentCastleRights.bqs = False
        self.castleRightsLog.append(CastleRights(self.currentCastleRights.wks, self.currentCastleRights.bks,
                                                 self.currentCastleRights.wqs, self.currentCastleRights.bqs))


    def get_valid_moves(self):
        """ returns every move the user can play, considering checks
        Algorithm steps:
            generate all possible moves
            for each possible move:
                - simulate the move
                - generate all possible moves the opponent can make
                - if the king is still in check after generating all our possible moves:
                    remove move from the list of possible moves
        """
        moves = self.get_possible_moves()  # generate all possible moves

        # add castle moves here
        # ! adding castle moves in get_possible_moves causes recursion error !
        # store a copy of the current castle rights, as they may change as we check valid moves
        temp_castle_rights = CastleRights(self.currentCastleRights.wks, self.currentCastleRights.bks,
                                          self.currentCastleRights.wqs, self.currentCastleRights.bqs)
        if self.whiteTurn:
            self.get_castle_moves(self.wKLocation, moves)
        else:
            self.get_castle_moves(self.bKLocation, moves)

        # iterate through each move backwards to avoid bugs when removing items
        for i in range(len(moves) - 1, -1, -1):     # for each possible move
            self.move_piece(moves[i])   # simulate the move
            # we need to swap the turn back because the move_piece method switched the turns
            self.whiteTurn = not self.whiteTurn
            if self.in_check():     # checks if the king is still in check
                moves.remove(moves[i])  # remove move from moves
            # after this we need to undo the actions we took to simulate a move
            self.whiteTurn = not self.whiteTurn
            self.undo_move()

        # set the castle rights to what they were before
        self.currentCastleRights = temp_castle_rights
        return moves

    def in_check(self):
        """ determines if the current player is in check"""
        if self.whiteTurn:
            return self.square_under_attack(self.wKLocation[0], self.wKLocation[1])
        else:
            return self.square_under_attack(self.bKLocation[0], self.bKLocation[1])

    def square_under_attack(self, r, c):
        """ determines if the specified square is under attack """
        # simulate the opponents moves and see if they can attack our piece
        self.whiteTurn = not self.whiteTurn     # switch the turn
        opp_moves = self.get_possible_moves()  # to generate opponents moves
        self.whiteTurn = not self.whiteTurn     # turn must be switched back
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False

    def get_possible_moves(self):
        """ returns a list of every the user can play, NOT considering checks,
        the moves are stored as Move objects
        Algorithm steps:
            for every square on the board:
                if the piece is not empty and it's that color's turn:
                    generate moves for that specific piece
                    add them to moves
        """
        moves = []
        for r in range(len(self.gameboard)):
            for c in range(len(self.gameboard[r])):
                color = self.gameboard[r][c][0]
                piece = self.gameboard[r][c][1]
                if (color == 'w' and self.whiteTurn) or (
                        color == 'b' and not self.whiteTurn):
                    # the generate functions take the r and c parameters reversed
                    # this is because the methods think of r, c as x, y
                    # in co-ordinate systems x is always before y
                    # therefore: c = x, r = y, and (x, y) = (c, r)
                    piece_moves = self.generatorFunctions[piece](c, r)
                    for move in piece_moves:
                        moves.append(move)
        return moves

    def _generate_pawn_moves(self, c, r):
        """ Usually, the pawn can only move forward one tile. It has some
        extra conditions though: if you haven't moved the pawn yet it can
        travel two spaces, and if the pawn is capturing it can move diagonally.
        The pawn can also preform a move known as "en passant", and it
        can be promoted if it reaches the closest rank to the opponent.
        For the most part, we just have to check if the pawn can move in
        each location manually and if it can then add the move.
        """

        step_up = -1 if self.whiteTurn else 1
        moves = []

        # every move features an increase in the row by at least one,
        # so no list of locations is needed
        if 0 <= r + step_up <= 7:   # if the move is not out of bounds
            # standard pawn move: if the space ahead is free, add the move
            if self.gameboard[r + step_up][c] == '--':
                moves.append(Move((c, r), (c, r + step_up), self.gameboard))

                # 2 step move: can only preform this move if standard move is possible
                # if the pawn has not moved yet (the pawn can only move forward)
                if (self.whiteTurn and r == 6) or (not self.whiteTurn and r == 1):
                    # if the space two steps ahead is empty, add the move
                    if self.gameboard[r + step_up * 2][c] == '--':
                        moves.append(Move((c, r), (c, r + step_up * 2), self.gameboard))

            # checking diagonal captures
            color = 'b' if self.whiteTurn else 'w'
            if c + 1 <= 7 and self.gameboard[r + step_up][c + 1][0] == color:   # regular capture
                moves.append(Move((c, r), (c + 1, r + step_up), self.gameboard))
            elif c + 1 <= 7 and (r + step_up, c + 1) == self.enpassantSquare:   # enpassant move
                moves.append(Move((c, r), (c + 1, r + step_up), self.gameboard))
            if 0 <= c - 1 and self.gameboard[r + step_up][c - 1][0] == color:
                moves.append(Move((c, r), (c - 1, r + step_up), self.gameboard))
            elif 0 <= c - 1 and (r + step_up, c - 1) == self.enpassantSquare:   # enpassant move
                moves.append(Move((c, r), (c - 1, r + step_up), self.gameboard))

        return moves

    def _generate_rook_moves(self, c, r):
        """ The rook can move up and down and left to right. The rook has
        to stop moving in that direction until it hits the bounds, a
        friendly piece or an enemy piece (which it captures). To generate
        the moves, we will keep generating moves in every direction using
        a while loop until the piece has to stop.
        """
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        color = 'w' if self.whiteTurn else 'b'
        opp_color = 'b' if self.whiteTurn else 'w'

        # while True:
        # step increase/decrease
        # check if move is in bounds, if not exit
        # check if move will capture it's own color, if so exit
        # add the piece
        # check if the piece has captured another color, if so exit

        for direction in directions:
            row_inc, col_inc = r, c
            while True:
                row_inc += direction[0]
                col_inc += direction[1]
                if row_inc > 7 or col_inc > 7 or row_inc < 0 or col_inc < 0:
                    break
                if self.gameboard[row_inc][col_inc][0] == color:
                    break
                moves.append(Move((c, r), (col_inc, row_inc), self.gameboard))
                if self.gameboard[row_inc][col_inc][0] == opp_color:
                    break

        return moves

    def _generate_knight_moves(self, c, r):
        """ The knight moves in an L shape in every direction. The knight
        can also jump over other pieces. This piece is similar to the
        king; we just have to check if each location is movable, if so
        then add the move
        """
        moves = []
        locations = [   # create all the possible moves
            (c + 2, r + 1),
            (c + 2, r - 1),
            (c - 2, r + 1),
            (c - 2, r - 1),
            (c + 1, r + 2),
            (c + 1, r - 2),
            (c - 1, r + 2),
            (c - 1, r - 2),
        ]

        color = 'w' if self.whiteTurn else 'b'
        for loc in locations:
            # if the location is in bounds
            if 0 <= loc[0] <= 7 and 0 <= loc[1] <= 7:
                # if knight is not taking his own color
                if self.gameboard[loc[1]][loc[0]][0] != color:
                    # add move
                    moves.append(Move((c, r), loc, self.gameboard))
        return moves

    def _generate_bishop_moves(self, c, r):
        """ The bishop can move in every diagonal direction. The piece
        has to stop once it reaches the bounds, a friendly piece, or
        captures an enemy piece. The move generation is very similar to
        the rook, except we must increment both axes to generate the
        moves.
        """
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        color = 'w' if self.whiteTurn else 'b'
        opp_color = 'b' if self.whiteTurn else 'w'

        # while True:
        # (row, col) increase/decrease
        # check if move is in bounds, if not exit
        # check if move will capture it's own color, if so exit
        # add the piece
        # check if the piece has captured another color, if so exit

        for direction in directions:
            row_inc, col_inc = r, c
            while True:
                row_inc += direction[0]
                col_inc += direction[1]
                if row_inc > 7 or col_inc > 7 or row_inc < 0 or col_inc < 0:
                    break
                if self.gameboard[row_inc][col_inc][0] == color:
                    break
                moves.append(Move((c, r), (col_inc, row_inc), self.gameboard))
                if self.gameboard[row_inc][col_inc][0] == opp_color:
                    break

        return moves

    def _generate_king_moves(self, c, r):
        """ The king can move a distance of one tile in any square.
        The move generation is simple for this piece, we just have to look
        one square in every direction and check if that location is
        movable. If so, move the piece there. The king can also castle,
        which is a more complex move that requires a different strategy
        to generate. To generate a castle, we just have to check that the
        king and the rook have not moved and the space in between them
        is empty.
        """
        moves = []
        locations = [   # creating all possible moves
            (c + 1, r),
            (c - 1, r),
            (c, r + 1),
            (c, r - 1),
            (c + 1, r + 1),
            (c + 1, r - 1),
            (c - 1, r + 1),
            (c - 1, r - 1)]

        color = 'w' if self.whiteTurn else 'b'
        for loc in locations:
            # if the location is in bounds
            if 0 <= loc[0] <= 7 and 0 <= loc[1] <= 7:
                # if king is not taking his own color
                if self.gameboard[loc[1]][loc[0]][0] != color:
                    # add move
                    moves.append(Move((c, r), loc, self.gameboard))

        return moves

    def get_castle_moves(self, pos, moves):
        """ for castling there are 4 conditions:
            (1) cannot castle if the king is in check
            (2) The king or rook of respective side cannot have already moved
            (3) the space in between the castles must be open
            (4) the king does not end up in check
        """
        r, c = pos  # pos will be the king position as (row, col)
        if self.square_under_attack(r, c):     # step (1)
            return
        # kingside castle
        if ((self.currentCastleRights.wks and self.whiteTurn) or
            (self.currentCastleRights.bks and not self.whiteTurn)):     # step (2)
            # step (3)
            if self.gameboard[r][c + 1] == '--' and self.gameboard[r][c + 2] == '--':
                # step (4)
                if not self.square_under_attack(r, c + 2):
                    moves.append(Move((c, r), (c + 2, r), self.gameboard))  # add move
        # queenside castle
        if ((self.currentCastleRights.wqs and self.whiteTurn)
            or (self.currentCastleRights.bqs and not self.whiteTurn)):     # step (2)
            if (self.gameboard[r][c - 1] == '--' and self.gameboard[r][c - 2] == '--'
                    and self.gameboard[r][c - 3] == '--'):  # step (3)
                # step (4)
                if not self.square_under_attack(r, c - 2):
                    moves.append(Move((c, r), (c - 2, r), self.gameboard))    # add move


    def _generate_queen_moves(self, c, r):
        """ The queen can move in any direction, diagonal or straight for
        any amount of blocks until she reaches the bounds, hits a friendly
        piece, or captures an enemy piece. The queen is essentially a rook
        and a bishop, so all that is needed to generate the queen moves
        is to generate rook moves and then generate bishop moves."""
        moves = []
        for move in self._generate_rook_moves(c, r):
            moves.append(move)
        for move in self._generate_bishop_moves(c, r):
            moves.append(move)
        return moves


class Move(object):
    """ The Move class stores the information about a move that player
    may make. Is used in the GameState class. Contains functionality to
    translate "x, y" positions to "file, rank" positions (ex. A1 to A3).
    """
    y_to_rank = {i: chr(97 + i) for i in range(8)}
    x_to_file = {i: f'{8 - i}' for i in range(8)}

    def __init__(self, start_pos, end_pos, gameboard, promotion_piece='P', enpassant_move=False, is_castle=False):
        # x represents columns, y represents rows
        # position (x, y) becomes [y][x] or [row][col]
        # positions
        self.start_col, self.start_row = start_pos
        self.end_col, self.end_row = end_pos
        # pieces
        self.pieceMoved = gameboard[self.start_row][self.start_col]
        self.pieceCaptured = gameboard[self.end_row][self.end_col]
        # pawn promotion
        self.isPawnPromotion = ((self.pieceMoved == 'wP' and self.end_row == 0) or
                                (self.pieceMoved == 'bP' and self.end_row == 7))
        self.promotion_piece = promotion_piece
        # en passant
        self.enPassantMove = enpassant_move
        if self.enPassantMove:  # we need to set the captured pawn as the captured piece
            step = 1 if self.pieceMoved[0] == 'b' else -1
            self.pieceCaptured = gameboard[self.end_row + step][self.end_col]
        # castling
        self.isCastle = is_castle

    def get_chess_pos(self):
        first_pos = self.get_rank_file(self.start_row, self.start_col)
        second_pos = self.get_rank_file(self.end_row, self.end_col)
        return first_pos + ' to ' + second_pos

    def get_rank_file(self, x, y):
        return self.y_to_rank[y] + self.x_to_file[x]


class CastleRights(object):

    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
