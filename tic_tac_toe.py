import tkinter as tk
from tkinter import messagebox
import random

# --- Game Logic ---

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != "":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None

def is_full(board):
    return all(cell != "" for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif is_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -float("inf")
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# --- GUI Part ---

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe 🎮")
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.vs_computer = False
        self.current_player = "X"
        self.create_menu()
        self.create_board()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        mode_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Mode", menu=mode_menu)
        mode_menu.add_command(label="2 Player", command=self.start_2_player)
        mode_menu.add_command(label="Vs Computer", command=self.start_vs_computer)
        mode_menu.add_separator()
        mode_menu.add_command(label="Exit", command=self.root.quit)

    def create_board(self):
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(
                    self.root,
                    text="",
                    font=("Arial", 24, "bold"),
                    width=5,
                    height=2,
                    bg="#222831",
                    fg="#EEEEEE",
                    activebackground="#393E46",
                    command=lambda r=i, c=j: self.make_move(r, c)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

    def reset_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for row in self.buttons:
            for btn in row:
                btn.config(text="", state="normal", bg="#222831")
        self.current_player = "X"

    def start_2_player(self):
        self.vs_computer = False
        self.reset_board()
        messagebox.showinfo("Mode Selected", "2 Player Mode Activated!")

    def start_vs_computer(self):
        self.vs_computer = True
        self.reset_board()
        messagebox.showinfo("Mode Selected", "Playing vs Computer!")

    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)

            winner = check_winner(self.board)
            if winner:
                messagebox.showinfo("Game Over", f"🏆 Player {winner} wins!")
                self.reset_board()
                return
            elif is_full(self.board):
                messagebox.showinfo("Game Over", "🤝 It's a tie!")
                self.reset_board()
                return

            if self.vs_computer:
                self.current_player = "O"
                move = best_move(self.board)
                if move:
                    i, j = move
                    self.board[i][j] = "O"
                    self.buttons[i][j].config(text="O")
                    winner = check_winner(self.board)
                    if winner:
                        messagebox.showinfo("Game Over", f"🏆 Player {winner} wins!")
                        self.reset_board()
                        return
                    elif is_full(self.board):
                        messagebox.showinfo("Game Over", "🤝 It's a tie!")
                        self.reset_board()
                        return
                self.current_player = "X"
            else:
                self.current_player = "O" if self.current_player == "X" else "X"


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
