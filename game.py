import random
import os


class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        if not self.name:
            name = input("What is your name? ")
            while not name.isalpha():
                print("You can't use special characters or numbers in your name.")
                name = input("What is your name? ")
            self.name = name

    def choose_symbol(self):
        if not self.symbol:
            symbol = input("Enter Your Desired Symbol: ")
            while len(symbol) != 1 or not symbol.isalpha():
                print(
                    "You can't use special characters or numbers in your symbol and it must be one letter."
                )
                symbol = input("Enter Your Desired Symbol: ")
            self.symbol = symbol.upper()


class Menu:
    def display_main_menu(self):
        main_menu = """
            -------------Main Menu-------------
        1. Start Game
        2. Quit Game
        """
        print(main_menu)
        choice = int(input("Enter your choice(1-2): "))
        while choice not in [1, 2]:
            print("Invalid choice.")
            choice = int(input("Enter your choice(1-2): "))
        return choice

    def display_endgame_menu(self):
        endgame_menu = """
            -------------Game Over-------------
        1. Play Again
        2. Quit Game
        """
        print(endgame_menu)
        choice = int(input("Enter your choice(1-2): "))
        while choice not in [1, 2]:
            print("Invalid choice.")
            choice = int(input("Enter your choice(1-2): "))
        return choice


class Board:
    def __init__(self):
        self.board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

    def display_board(self):
        for row in self.board:
            print(" | ".join(row))
            print("-" * 9)

    def update_board(self, position, symbol):
        row = (position - 1) // 3
        col = (position - 1) % 3
        self.board[row][col] = symbol
        os.system("cls")

    def is_position_available(self, position):
        row = (position - 1) // 3
        col = (position - 1) % 3
        return self.board[row][col] not in ["X", "O"]

    def reset_board(self):
        self.board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]


class Game:
    def __init__(self):
        self.board = Board()
        self.player = Player()
        self.menu = Menu()
        self.computer_symbol = ""
        self.current_player = ""
        self.winning_combinations = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],  # Rows
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],  # Columns
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],  # Diagonals
        ]
        self.player_wins = 0
        self.computer_wins = 0
        self.draws = 0

    def start_game(self):
        if self.menu.display_main_menu() == 1:
            self.player.choose_name()
            self.player.choose_symbol()
            self.current_player = self.player.name
            self.computer_symbol = "X" if self.player.symbol == "O" else "O"
            self.play_game()

    def play_game(self):
        while True:
            while True:
                self.board.display_board()
                if self.current_player == self.player.name:
                    self.human_move()
                else:
                    self.computer_move()
                if self.check_win(self.player.symbol):
                    print(f"Congratulations {self.player.name}, you won!")
                    self.player_wins += 1
                    break
                if self.check_win(self.computer_symbol):
                    print("Computer wins!")
                    self.computer_wins += 1
                    break
                if self.check_draw():
                    print("It's a draw!")
                    self.draws += 1
                    break
                self.switch_player()
            choice = self.menu.display_endgame_menu()
            if choice == 1:
                self.board.reset_board()
            else:
                self.display_scores()
                break

    def human_move(self):
        position = int(input("Enter your move (1-9): "))
        while (
            position < 1
            or position > 9
            or not self.board.is_position_available(position)
        ):
            print("Invalid move. Please try again.")
            position = int(input("Enter your move (1-9): "))
        self.board.update_board(position, self.player.symbol)

    def computer_move(self):
        available_positions = [
            i for i in range(1, 10) if self.board.is_position_available(i)
        ]
        position = random.choice(available_positions)
        self.board.update_board(position, self.computer_symbol)
        print(f"Computer placed '{self.computer_symbol}' at position {position}.")

    def switch_player(self):
        self.current_player = (
            self.player.name
            if self.current_player == self.computer_symbol
            else self.computer_symbol
        )

    def check_win(self, symbol):
        for combination in self.winning_combinations:
            if all(self.board.board[row][col] == symbol for row, col in combination):
                return True
        return False

    def check_draw(self):
        for row in self.board.board:
            for cell in row:
                if cell not in ["X", "O"]:
                    return False
        return True

    def display_scores(self):
        print(f"Player Wins: {self.player_wins}")
        print(f"Computer Wins: {self.computer_wins}")
        print(f"Draws: {self.draws}")


game = Game()
game.start_game()
