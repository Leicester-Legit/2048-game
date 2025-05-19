import tkinter as tk
from tkinter import messagebox
import random

class Simple2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        
        self.grid_size = 4
        self.board = [[0]*4 for _ in range(4)]
        self.score = 0
        self.high_score = 0
        
        # Game UI
        self.score_frame = tk.Frame(root)
        self.score_frame.pack()
        
        self.score_label = tk.Label(self.score_frame, text="Score: 0", font=('Arial', 12))
        self.score_label.pack(side='left', padx=10)
        
        self.high_score_label = tk.Label(self.score_frame, text="High Score: 0", font=('Arial', 12))
        self.high_score_label.pack(side='left', padx=10)
        
        self.canvas = tk.Canvas(root, width=300, height=300, bg='#bbada0')
        self.canvas.pack()
        
        self.restart_button = tk.Button(root, text="Restart", command=self.start_game)
        self.restart_button.pack(pady=10)
        
        # Key bindings
        self.root.bind('<Left>', lambda e: self.move('left'))
        self.root.bind('<Right>', lambda e: self.move('right'))
        self.root.bind('<Up>', lambda e: self.move('up'))
        self.root.bind('<Down>', lambda e: self.move('down'))
        
        self.start_game()
    
    def start_game(self):
        self.board = [[0]*4 for _ in range(4)]
        self.score = 0
        self.update_score()
        self.add_new_tile()
        self.add_new_tile()
        self.draw_board()
    
    def draw_board(self):
        self.canvas.delete('all')
        for row in range(4):
            for col in range(4):
                x1 = col * 75 + 5
                y1 = row * 75 + 5
                x2 = x1 + 70
                y2 = y1 + 70
                
                value = self.board[row][col]
                color = '#5C4033' if value else '#cdc1b4'
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                if value:
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, 
                                          text=str(value), 
                                          font=('Arial', 20, 'bold'))
    
    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"High Score: {self.high_score}")
    
    def add_new_tile(self):
        empty = [(r,c) for r in range(4) for c in range(4) if self.board[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.board[r][c] = 2 if random.random() < 0.9 else 4
    
    def move(self, direction):
        moved = False
        board_copy = [row[:] for row in self.board]
        
        if direction in ('left', 'right'):
            for row in range(4):
                non_zero = [n for n in self.board[row] if n != 0]
                if direction == 'right':
                    non_zero = non_zero[::-1]
                
                merged = []
                skip = False
                for i in range(len(non_zero)):
                    if skip:
                        skip = False
                        continue
                    if i < len(non_zero)-1 and non_zero[i] == non_zero[i+1]:
                        merged.append(non_zero[i]*2)
                        self.score += non_zero[i]*2
                        skip = True
                    else:
                        merged.append(non_zero[i])
                
                merged += [0]*(4 - len(merged))
                if direction == 'right':
                    merged = merged[::-1]
                
                if self.board[row] != merged:
                    moved = True
                    self.board[row] = merged
        
        elif direction in ('up', 'down'):
            for col in range(4):
                column = [self.board[row][col] for row in range(4)]
                non_zero = [n for n in column if n != 0]
                if direction == 'down':
                    non_zero = non_zero[::-1]
                
                merged = []
                skip = False
                for i in range(len(non_zero)):
                    if skip:
                        skip = False
                        continue
                    if i < len(non_zero)-1 and non_zero[i] == non_zero[i+1]:
                        merged.append(non_zero[i]*2)
                        self.score += non_zero[i]*2
                        skip = True
                    else:
                        merged.append(non_zero[i])
                
                merged += [0]*(4 - len(merged))
                if direction == 'down':
                    merged = merged[::-1]
                
                if column != merged:
                    moved = True
                    for row in range(4):
                        self.board[row][col] = merged[row]
        
        if moved:
            self.update_score()
            self.add_new_tile()
            self.draw_board()
            
            if self.is_game_over():
                messagebox.showinfo("Game Over", f"Game Over! Score: {self.score}")
    
    def is_game_over(self):
        # Check for empty spaces
        for row in range(4):
            for col in range(4):
                if self.board[row][col] == 0:
                    return False
        
        # Check for possible merges
        for row in range(4):
            for col in range(3):
                if self.board[row][col] == self.board[row][col+1]:
                    return False
        
        for col in range(4):
            for row in range(3):
                if self.board[row][col] == self.board[row+1][col]:
                    return False
        
        return True

if __name__ == "__main__":
    root = tk.Tk()
    game = Simple2048(root)
    root.mainloop()