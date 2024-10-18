import random
from tkinter import *
from tkinter import messagebox


class Player:
    def __init__(self):
        self.name = "Player"
        self.symbol = "X"


class Board:
    def __init__(self, root, game):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = []
        self.root = root
        self.game = game
        self.create_board()

    def create_board(self):
        for row in range(3):
            row_buttons = []
            for col in range(3):
                button = Button(
                    self.root,
                    text="",
                    font=('Arial', 24),
                    width=5,
                    height=2,
                    fg="green",  # Set the symbol color to green
                    command=lambda r=row, c=col: self.game.player_move(r, c)
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def update_board(self, row, col, symbol):
        self.board[row][col] = symbol
        self.buttons[row][col].config(text=symbol, state="disabled")

    def is_position_available(self, row, col):
        return self.board[row][col] == ""

    def reset_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", state="normal")


class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("345x450")
        self.player = Player()
        self.board = Board(self.root, self)
        self.current_player = self.player
        self.computer_symbol = "O"
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
        self.info_label = Label(root, text="Player's Turn (X)", font=("Arial", 16))
        self.info_label.grid(row=3, column=0, columnspan=3, pady=10)
        self.restart_button = Button(
            root, text="Restart Game", command=self.restart_game, font=("Arial", 12)
        )
        self.restart_button.grid(row=4, column=0, columnspan=3, pady=10)

    def player_move(self, row, col):
        if self.board.is_position_available(row, col):
            self.board.update_board(row, col, self.player.symbol)
            if self.check_win(self.player.symbol):
                self.info_label.config(text="Player Wins!")
                self.end_game("Player wins!")
            elif self.check_draw():
                self.info_label.config(text="It's a Draw!")
                self.end_game("It's a draw!")
            else:
                self.info_label.config(text="Computer's Turn (O)")
                self.disable_player_buttons()  # Disable player buttons
                self.root.after(1000, self.computer_move)

    def computer_move(self):
        available_positions = [
            (r, c)
            for r in range(3)
            for c in range(3)
            if self.board.is_position_available(r, c)
        ]
        if available_positions:
            row, col = random.choice(available_positions)
            self.board.update_board(row, col, self.computer_symbol)
            if self.check_win(self.computer_symbol):
                self.info_label.config(text="Computer Wins!")
                self.end_game("Computer wins!")
            elif self.check_draw():
                self.info_label.config(text="It's a Draw!")
                self.end_game("It's a draw!")
            else:
                self.info_label.config(text="Player's Turn (X)")
                self.enable_player_buttons()  # Re-enable player buttons

    def check_win(self, symbol):
        for combination in self.winning_combinations:
            if all(self.board.board[row][col] == symbol for row, col in combination):
                return True
        return False

    def check_draw(self):
        return all(cell != "" for row in self.board.board for cell in row)

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        for row in self.board.buttons:
            for button in row:
                button.config(state="disabled")

    def restart_game(self):
        self.board.reset_board()
        self.info_label.config(text="Player's Turn (X)")
        self.enable_player_buttons()  # Re-enable buttons when restarting

    def disable_player_buttons(self):
        for row in self.board.buttons:
            for button in row:
                button.config(state="disabled")

    def enable_player_buttons(self):
        for row in self.board.buttons:
            for button in row:
                if button.cget("text") == "":
                    button.config(state="normal")


root = Tk()
root.resizable(False , False)
supermario_icon = PhotoImage(file= "pngegg.png")
root.iconphoto(True , supermario_icon)
root.config(background="#000")



game = Game(root)
root.mainloop()
