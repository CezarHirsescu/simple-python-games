import pygame as py
from random import randint


class GameWindow:
    """ Game window is a class that will contain the entire tic tac toe
    game. It will play the game for one round. Created to be implemented
    in the main class.

    Constants:
        BLACK (tup): RGB for the colour black
        WHITE (tup): RGB for the colour white
        WORD_SPACE (int): The pixel height of the words that will go above
            the tic tac toe grid. (Might be switched to a field)

    Fields:
        self.height (int): The height of the screen, defined by the
         program as int() + WORD_SPACE, int being the size of the play
         grid. Implemented as a field for window resizability options.
        self.width (int): The width of the screen. Is the size of the play
            grid. Implemented as a field for window resizability options.
        self.window (py.display): The window where the game will be displayed
        self.game_array (list): A 2d list which is a copy of the gameboard.
            Used by the program to keep track of the game and determine
            if a user has won. Modified then restored in the hard_ai()
            method.

    Methods:
        run(self, ai=None): Uses all the private methods and class
            attributes to run one round of the tic tac toe game. If ai
            is not specified, the mode will be two players. The ai arg
            is a function that returns a tuple to be used as a location
            for draw_x_or_o() method.
        easy_ai(self): Picks a random position on the board and returns
            that position if it is currently empty.
        hard_ai(self): Uses the mini-max algorithm to determine the
            optimal location.
    """

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    WORD_SPACE = 50

    def __init__(self):
        py.init()
        self.height = 540 + self.WORD_SPACE
        self.width = 590
        self.window = py.display.set_mode((self.width, self.height))
        self.window.fill(self.WHITE)
        py.display.update()
        self.game_array = [['_', '_', '_'],
                           ['_', '_', '_'],
                           ['_', '_', '_']]

    def _check_winner(self):
        """ Checks to see if x or o has won. Returns none if the game is
        still in play, 1 if 'X' has won, -1 if 'O' has won and 0 if it's
         a tie.
        """

        x_win = ['X', 'X', 'X']  # return 1
        o_win = ['O', 'O', 'O']  # return -1
        total_pieces = []  # if filled, return 0 for tie
        dig1 = []
        dig2 = []

        # check rows
        for i in range(3):
            row = []
            col = []

            for j in range(3):
                row.append(self.game_array[i][j])
                col.append(self.game_array[j][i])
                total_pieces.append(self.game_array[i][j])

            dig1.append(self.game_array[i][i])
            dig2.append(self.game_array[i][2 - i])

            if row == x_win or col == x_win or dig1 == x_win or dig2 == x_win:
                return 1
            elif row == o_win or col == o_win or dig1 == o_win or dig2 == o_win:
                return -1

        if '_' not in total_pieces:
            return 0

        return None

    def _draw_grid(self):
        """ draws the tic tac toe grid on the py window. Scales to the
        width and height of the screen
        """

        for i in range(1, 3):
            line1_x = self.width // 3 * i
            line2_y = ((self.height * i) + self.WORD_SPACE) // 3

            py.draw.line(self.window, self.BLACK, (line1_x, self.WORD_SPACE),
                         (line1_x, self.height), 3)
            py.draw.line(self.window, self.BLACK, (0, line2_y),
                         (self.width, line2_y), 3)

    def _draw_x_or_o(self, position, player):
        """ If player is x then it calls the draw_x to draw an x in the
        position specified. Else if player is o then it calls the draw_o
        to draw an o in the position specified. This method also draws
        the x or o in the self.game_array field.

        args:
            position (tuple): a tuple of two ints that represent the row
                and column
            player (str): a string with the value of either 'X' or 'O'

        methods:
            draw_x(grid_pos_x, grid_pos_y): draws an x in the specified
            grid position
            draw_o(grid_pos_x, grid_pos_y): draws an o in the specified
            grid position
        """

        width_pos = self.width // 3
        height_pos = (self.height - self.WORD_SPACE) // 3

        def draw_x(grid_pos_x, grid_pos_y):
            """ draws an 'x' in the specified grid position. It scales
            py.window coordinates with the grid positions so it can draw
            an x with any width and length of the py.window. """

            x1 = int(width_pos / 4.2) + (width_pos * grid_pos_x)
            x2 = x1 + int(width_pos * 0.55)
            y1 = height_pos // 3 + (height_pos * grid_pos_y)
            y2 = y1 + int(height_pos * 0.77)

            py.draw.line(self.window, self.BLACK, (x1, y1), (x2, y2), 5)
            py.draw.line(self.window, self.BLACK, (x1, y2), (x2, y1), 5)
            py.display.update()

        def draw_o(grid_pos_x, grid_pos_y):
            """ same as draw x, but it draws an 'o' instead. """

            x = (width_pos * grid_pos_x) + width_pos // 2
            y = ((height_pos * grid_pos_y) + self.WORD_SPACE) + height_pos // 2

            if width_pos <= height_pos:
                radius = int(width_pos * 0.36)
            else:
                radius = int(height_pos * 0.36)

            py.draw.circle(self.window, self.BLACK, (x, y), radius, 4)
            py.display.update()

        pos_x, pos_y = position
        if player == 'X':
            draw_x(pos_x, pos_y)
            self.game_array[pos_x][pos_y] = 'X'
        else:   # player == 'O'
            draw_o(pos_x, pos_y)
            self.game_array[pos_x][pos_y] = 'O'

    def _get_grid_pos(self, mouse_x, mouse_y):
        """ gets the screen position from the mouse and returns a grid
        position tuple.
        """

        for x in range(1, 4):
            for y in range(1, 4):
                if (mouse_x < x * self.width // 3) and (mouse_y < y * self.height // 3):
                    return (x - 1), (y - 1)

    def _has_space(self, position):
        """ checks the game board to see if there is a space to play an
        x or an o and returns true if there is space and false if not.
        """

        pos_x, pos_y = position
        if self.game_array[pos_x][pos_y] == '_':
            return True
        return False

    def _draw_sentence(self, text):
        """ draws the 'text' string in the WORD_SPACE gap """

        font = py.font.SysFont('comicsansms', 28)
        text = font.render(text, True, self.BLACK, self.WHITE)
        text_rect = text.get_rect()
        text_rect.center = (self.width // 2, self.WORD_SPACE // 2)
        self.window.blit(text, text_rect)

    def _draw_turn_text(self, is_player_x_turn):
        """ uses the _draw_sentence method to display who's turn it is.
        this method is to be used before every turn (except the first
        turn) in the run method.
        """

        if is_player_x_turn:
            self._draw_sentence("     It's Player X's turn     ")
        else:
            self._draw_sentence("     It's Player O's turn     ")

    def _draw_first_player_text(self, is_player_x_turn):
        """ uses the _draw_sentence method to determine who will go first.
        this method is to be used at the beginning of the game in the
        run method.
        """

        if is_player_x_turn:
            self._draw_sentence("  Player 'X' will go first  ")
        else:
            self._draw_sentence("  Player 'O' will go first  ")

    def _draw_winner_text(self, winner):
        """ uses the _draw_sentence method to display a win-condition
        text.
        """

        if winner == 1:
            self._draw_sentence("     Player 'X' wins!!!!     ")
        elif winner == -1:
            self._draw_sentence("     Player 'O' wins!!!!     ")
        else:
            self._draw_sentence("        It's a tie!!!        ")

    def easy_ai(self):
        """ This method generates random positions and returns one if it
        is valid. This ai is purposefully terrible. Returns position as
        tuple.

        """

        while True:
            x = randint(0, 2)
            y = randint(0, 2)
            if self.game_array[x][y] == '_':
                return x, y

    def hard_ai(self):
        """ This ai uses the mini-max algorithm to determine the best
        position for it to play. The regular mini-max algorithm returns
        a score of type int, however the hard_ai() method knows to
        associate a score with a certain position, and it will return
        the position with the highest score (unlike the mini-max
        function which just returns a score). The ai plays the 'o' symbol
        for the computer and returns a tuple for the best optimal
        position. When the computer is maximizing, the best score is
        actually -1 since the _check_winner method returns -1 when o
        wins. When the ai has the first move, location (0, 0) is hard-
        coded for the optimal move because at that stage in the game
        every position is granted equal and it takes too much time to
        let the computer carry out the mini-max algorithm in that
        scenario.

        Methods:
            gameboard_is_empty(): Returns True if self.game_array is
                empty, else returns False. Is used to determine if the
                ai has the first turn.
            mini_max(is_maximizing): This method implements the mini-max
                algorithm. This algorithm is recursive. The
                'is_maximizing' arg is used to iterate between the
                minimizing and maximizing player (hence the name of the
                algorithm). For info on the general mini-max algorithm
                theory, go to: https://en.wikipedia.org/wiki/Minimax.
                In this specific use of mini-max, the function starts
                with the worst possible score for a position (which
                depends on who's maximizing). It then iterates through
                all nine positions and determines a score for each
                position using the mini-max algorithm (it's recursive).
                Once you reach the end of the tree, which in this case
                means the game is over, the algorithm returns 1, -1, or 0.
                Once that happens, those scores are returned by each
                recursion of mini-max, and it eventually gets back to the
                first call of the algorithm where the function finally
                returns a score. This happens 9 times (one time for every
                position on the board) and it returns the best score out
                of those 9 moves. Usually the algorithm takes a depth
                argument as well, however since this is such a simple
                game the depth is irrelevant.
        """

        def gameboard_is_empty():
            if self.game_array == [['_', '_', '_'],
                                   ['_', '_', '_'],
                                   ['_', '_', '_']]:
                return True
            return False

        def mini_max(is_maximizing):

            if self._check_winner() is not None:
                return self._check_winner()

            if is_maximizing:
                best_score = 1
                for i in range(3):
                    for j in range(3):
                        if self.game_array[i][j] == '_':
                            self.game_array[i][j] = 'O'
                            score = mini_max(False)
                            if score < best_score:
                                best_score = score
                            self.game_array[i][j] = '_'
            else:
                best_score = -1
                for i in range(3):
                    for j in range(3):
                        if self.game_array [i][j] == '_':
                            self.game_array[i][j] = 'X'
                            score = mini_max(True)
                            if score > best_score:
                                best_score = score
                            self.game_array[i][j] = '_'
            return best_score

        best_score = 1
        best_position = (0, 0)
        if gameboard_is_empty():
            return 0, 0
        for i in range(3):
            for j in range(3):
                if self.game_array[i][j] == '_':
                    self.game_array[i][j] = 'O'
                    temp_score = mini_max(False)
                    if temp_score < best_score:
                        best_score = temp_score
                        best_position = (i, j)
                    self.game_array[i][j] = '_'
        x, y = best_position
        return x, y

    def run(self, ai=None):
        """ The run() method is used to play one round of tic tac toe.
        It combines every other private method in this class. It starts
        by randomly picking which player will go first. Then it starts
        the loop to play the game. The loop keeps playing until an end
        condition is reached, and then the game ends. This method is
        meant to be implemented another program controls playing again
        or switching to single-player or multi-player or quiting.

        Args:
             ai (method returning tuple)=None: if ai is not specified,
                the program is played both sides by the user. This is
                the same-device multi-player mode. If ai is specified,
                the program becomes a single-player game, where player
                'O' is controlled by the computer.

                ** If ai is specified, it nust be a method that returns
                a tuple. The two ai's that come with this class are
                easy_ai and hard_ai. For implementation purposes, the
                user does not only have to use these two ai's. The user
                can use any custom method as long as it returns a tuple
                of x, y (grid locations).
                **

        Methods:
              play_turn

        """

        def play_turn(pos_tuple):
            """ plays a position in the given grid location """
            nonlocal is_x_turn
            if self._has_space(pos_tuple):
                if is_x_turn:
                    self._draw_x_or_o(pos_tuple, player_x)
                    is_x_turn = False
                else:
                    self._draw_x_or_o(pos_tuple, player_o)
                    is_x_turn = True
                self._draw_turn_text(is_x_turn)

        running = True
        player_x = 'X'
        player_o = 'O'
        game_over = False

        if randint(1, 2) == 1:
            is_x_turn = True
        else:
            is_x_turn = False
        self._draw_first_player_text(is_x_turn)

        while running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
            if game_over:
                while True:
                    event = py.event.wait()
                    if event.type == py.QUIT:
                        py.quit()
                        return 1

            self._draw_grid()

            if ai is not None and is_x_turn is False:
                position = ai()
                play_turn(position)
            else:
                button1, _, _ = py.mouse.get_pressed()
                if button1 == 1:
                    py.time.delay(100)
                    x_pos, y_pos = py.mouse.get_pos()
                    position = self._get_grid_pos(x_pos, y_pos)
                    play_turn(position)

            if self._check_winner() is not None:
                self._draw_winner_text(self._check_winner())
                game_over = True

            py.time.delay(100)
            py.display.update()


if __name__ == '__main__':
    game = GameWindow()
    game.run(game.hard_ai)
