class Cell:
    """Represents a cell in the Connect Four board. Each cell has a colour and scores for each direction.

    Attributes:
    colour (int): The colour of the cell. 0: empty, 1: red, 2: black
    scores (dict): A dictionary containing scores for each direction
    """
    def __init__(self):
        self.colour = 0  # 0: empty, 1: red, 2: black
        self.scores = {
            'vertical': [0, 0],
            'horizontal': [0, 0],
            'diagonal1': [0, 0],  # /
            'diagonal2': [0, 0]   # \
        }

    def reset(self):
        """Resets the cell to its initial state
        """
        self.colour = 0
        for direction in self.scores:
            self.scores[direction] = [0, 0]

class Board:
    """Represents the Connect Four board. The board is a 2D grid of cells.

    Attributes:
    rows (int): Number of rows in the board
    cols (int): Number of columns in the board
    cells (list[list[Cell]]): 2D grid of cells representing the board
    """
    def __init__(self, rows: int = 6, cols: int = 7):
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def reset(self):
        """Resets the board to its initial state
        """
        for row in self.cells:
            for cell in row:
                cell.reset()

    def is_valid_move(self, col: int) -> bool:
        """Checks if a move is valid in the given column

        Args:
            col (int): The column to check

        Returns:
            bool: True if the move is valid, False otherwise
        """
        return 0 <= col < self.cols and self.cells[0][col].colour == 0

    def drop_chip(self, col: int, colour: int) -> tuple[int, int]:
        """ Drops a chip of the given colour in the specified column

        Args:
            col (int): the column to drop the chip in
            colour (int): the colour of the chip (1: red, 2: black)

        Raises:
            ValueError: 
                If the column is invalid

        Returns:
            tuple[int, int]: 
                The row and column where the chip was dropped
        """
        if not self.is_valid_move(col):
            raise ValueError("Invalid move")

        for row in range(self.rows - 1, -1, -1):
            if self.cells[row][col].colour == 0:
                self.cells[row][col].colour = colour
                return row, col
            
    def update_vertical_score(self, row: int, col: int, colour: int) -> bool:
        """Updates the vertical score for the given cell

        Args:
            row (int): index of the row
            col (int): index of the column
            colour (int): colour of the cell

        Returns:
            bool: True if the score is 4 or more, False otherwise
        """
        count = 1
        # Check below the current cell
        for r in range(row + 1, min(row + 4, self.rows)):
            if self.cells[r][col].colour == colour:
                count += 1
            else:
                break
        return count >= 4

    def update_horizontal_score(self, row: int, col: int, colour: int) -> bool:
        """ Updates the horizontal score for the given cell

        Args:
            row (int): index of the row
            col (int): index of the column
            colour (int): colour of the cell

        Returns:
            bool: True if the score is 4 or more, False otherwise
        """
        count = 1
        # Check to the left
        for c in range(col - 1, max(col - 4, -1), -1):
            if self.cells[row][c].colour == colour:
                count += 1
            else:
                break
        # Check to the right
        for c in range(col + 1, min(col + 4, self.cols)):
            if self.cells[row][c].colour == colour:
                count += 1
            else:
                break
        return count >= 4

    def update_diagonal1_score(self, row: int, col: int, colour: int) -> bool:
        """ Updates the diagonal score for the given cell

        Args:
            row (int): index of the row
            col (int): index of the column
            colour (int): colour of the cell

        Returns:
            bool: True if the score is 4 or more, False otherwise 
        """
        count = 1
        # Check top-left to bottom-right
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0 and self.cells[r][c].colour == colour:
            count += 1
            r -= 1
            c -= 1
        r, c = row + 1, col + 1
        while r < self.rows and c < self.cols and self.cells[r][c].colour == colour:
            count += 1
            r += 1
            c += 1
        return count >= 4

    def update_diagonal2_score(self, row: int, col: int, colour: int) -> bool:
        """ Updates the diagonal score for the given cell

        Args:
            row (int): index of the row
            col (int): index of the column
            colour (int): colour of the cell

        Returns:
            bool: True if the score is 4 or more, False otherwise
        """
        count = 1
        # Check top-right to bottom-left
        r, c = row - 1, col + 1
        while r >= 0 and c < self.cols and self.cells[r][c].colour == colour:
            count += 1
            r -= 1
            c += 1
        r, c = row + 1, col - 1
        while r < self.rows and c >= 0 and self.cells[r][c].colour == colour:
            count += 1
            r += 1
            c -= 1
        return count >= 4

    def update_scores(self, row: int, col: int) -> bool:
        """ Updates the scores for the given cell

        Args:
            row (int): index of the row
            col (int): index of the column

        Returns:
            bool: True if the score is 4 or more, False otherwise
        """
        colour = self.cells[row][col].colour
        return (self.update_vertical_score(row, col, colour) or
                self.update_horizontal_score(row, col, colour) or
                self.update_diagonal1_score(row, col, colour) or
                self.update_diagonal2_score(row, col, colour))

class Game:
    """ Represents a Connect Four game between two players

    Attributes:
    board (Board): The Connect Four board
    players (list[str]): The names of the players
    moves (list[str]): The moves played
    """
    def __init__(self, players: list[str], moves: list[str]):
        self.board = Board()
        self.players = players
        self.moves = moves

    def play(self) -> tuple[int, int]:
        """ Plays the Connect Four game

        Returns:
            tuple[int, int]: the winner and the move number
        """
        for i, move in enumerate(self.moves):
            colour = 1 if i % 2 == 0 else 2
            col = int(move[1]) - 1
            
            row, col = self.board.drop_chip(col, colour)
            if self.board.update_scores(row, col):
                return colour, i + 1  # Return winner and move number
        
        return 0, len(self.moves)  # Draw


def parse_file(filename: str) -> list[Game]:
    """ Parses the input file and returns a list of Game objects

    Args:
        filename (str): the name of the input file

    Returns:
        list[Game]: a list of Game objects
    """
    games = []
    with open(filename, 'r') as file:
        game_data = []
        for line in file:
            line = line.strip()
            if line:
                game_data.append(line)
                if len(game_data) == 2:
                    players = game_data[0].split(', ')
                    moves = game_data[1].split(',')
                    games.append(Game(players, moves))
                    game_data = []
    return games

def process_games(games: list[Game]) -> list[str]:
    """ Processes the list of games and returns

    Args:
        games (list[Game]): a list of Game objects

    Returns:
        list[str]: a list of results
    """
    results = []
    
    for game in games:
        winner, winning_move = game.play()
        
        if winner == 0:
            result = f"Draw between {game.players[0]} and {game.players[1]}"
        else:
            winning_player = game.players[0] if winner == 1 else game.players[1]
            result = f"{winning_player} won in {winning_move} moves"
        
        results.append(result)
    return results

def solve_connect_four(filename: str):
    """ Solves the Connect Four game using the

    Args:
        filename (str): the name of the input file
    """
    games = parse_file(filename)
    results = process_games(games)
    
    return results