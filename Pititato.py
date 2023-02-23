import tkinter as tk
import os
import tkinter.simpledialog as simpledialog


class Pititato:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Pi Tic Tac Toe")
        self.window.geometry("800x480")
        self.window.attributes('-fullscreen', True)
        self.turn = "X"
        self.board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        self.scoreboard = {}
        self.load_scoreboard()
        self.create_scoreboard()
        self.create_board()
        tk.mainloop()

    def load_scoreboard(self):
        if os.path.exists("scoreboard.txt"):
            with open("scoreboard.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    name = parts[0]
                    score = int(parts[1])
                    self.scoreboard[name] = score

    def save_scoreboard(self):
        with open("scoreboard.txt", "w") as file:
            for name, score in sorted(self.scoreboard.items(), key=lambda item: item[1], reverse=True):
                file.write(name + "," + str(score) + "\n")

    def create_scoreboard(self):
        self.score_frame = tk.Frame(self.window, width=320, height=480)
        self.score_frame.place(x=520, y=40)
        self.score_label = tk.Label(self.score_frame, text="Top Players", font=("Arial", 15))
        self.score_label.pack(pady=10)
        self.score_list = tk.Listbox(self.score_frame, font=("Arial", 14))
        self.score_list.pack(padx=10, pady=10, fill="both", expand=True)
        for name, score in sorted(self.scoreboard.items(), key=lambda item: item[1], reverse=True):
            self.score_list.insert("end", name + " (" + str(score) + " wins)")
        self.new_game_button = tk.Button(self.score_frame, text="New Game", font=("Arial", 14), command=self.reset_board)
        self.new_game_button.pack(pady=10)
        self.exit_button = tk.Button(self.score_frame, text="Exit Game", font=("Arial", 14), command=self.window.destroy)
        self.exit_button.pack(pady=10)

    def create_board(self):
        self.board_frame = tk.Frame(self.window, width=480, height=480)
        self.board_frame.place(x=40, y=80)
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.board_frame, text=" ", font=("Arial", 50), bg="#ffffff", width=3, height=1, command=lambda i=i, j=j: self.play_turn(i, j))
                button.grid(row=i, column=j)
        self.turn_label = tk.Label(self.board_frame, text="You can place your " + self.turn, font=("Arial", 15))
        self.turn_label.grid(row=3, columnspan=3, pady=10)

    def play_turn(self, row, col):
        index = row * 3 + col
        if self.board[index] == " ":
            self.board[index] = self.turn
            self.update_button(index)
            if self.check_winner():
                self.handle_winner()
            elif self.check_tie():
                self.handle_tie()
            else:
                self.switch_turn()

    def switch_turn(self):
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"
        self.turn_label.config(text="Turn: " + self.turn)

    def update_button(self, index):
        row = index // 3
        col = index % 3
        button = self.board_frame.grid_slaves(row=row, column=col)[0]
        button.config(text=self.board[index], state="disabled")

    def check_winner(self):
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != " ":
                return True
            if self.board[i*3] == self.board[i*3+1] == self.board[i*3+2] != " ":
                return True
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return True
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return True
        return False

    def handle_winner(self):
        winner_name = simpledialog.askstring("Congratulations!", "Enter your name:")
        if winner_name:
            self.scoreboard[winner_name] = self.scoreboard.get(winner_name, 0) + 1
            self.save_scoreboard()
            self.score_list.delete(0, "end")
            for name, score in sorted(self.scoreboard.items(), key=lambda item: item[1], reverse=True):
                self.score_list.insert("end", name + " (" + str(score) + " wins)")
            if tk.messagebox.askyesno("Rematch?", "Do you want to play again?"):
                self.reset_board()
            else:
                self.window.destroy()

    def check_tie(self):
        return " " not in self.board

    def handle_tie(self):
        if tk.messagebox.askyesno("It's a tie!", "Do you want to play again?"):
            self.reset_board()
        else:
            self.window.destroy()

    def reset_board(self):
        self.turn = "X"
        self.board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        for i in range(3):
            for j in range(3):
                button = self.board_frame.grid_slaves(row=i, column=j)[0]
                button.config(text=" ", state="normal")
        self.turn_label.config(text="Turn: " + self.turn)
        self.score_list.delete(0, "end")
        for name, score in sorted(self.scoreboard.items(), key=lambda item: item[1], reverse=True):
            self.score_list.insert("end", name + " (" + str(score) + " wins)")

if __name__ == "__main__":
    Pititato()
