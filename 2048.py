import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("2048")

grid_size = 4
board = [[0]*4 for _ in range(4)]
score = 0
high_score = 0

# Game UI
score_frame = tk.Frame(root)
score_frame.pack()

score_label = tk.Label(score_frame, text="Score: 0", font=('Arial', 12))
score_label.pack(side='left', padx=10)

high_score_label = tk.Label(score_frame, text="High Score: 0", font=('Arial', 12))
high_score_label.pack(side='left', padx=10)

canvas = tk.Canvas(root, width=300, height=300, bg='#bbada0')
canvas.pack()

def start_game():
    global board, score
    board = [[0]*4 for _ in range(4)]
    score = 0
    update_score()
    add_new_tile()
    add_new_tile()
    draw_board()

restart_button = tk.Button(root, text="Restart", command=start_game)
restart_button.pack(pady=10)

def draw_board():
    canvas.delete('all')
    for row in range(4):
        for col in range(4):
            x1 = col * 75 + 5
            y1 = row * 75 + 5
            x2 = x1 + 70
            y2 = y1 + 70
            
            value = board[row][col]
            color = '#5C4033' if value else '#cdc1b4'
            
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            if value:
                canvas.create_text((x1+x2)/2, (y1+y2)/2, 
                                text=str(value), 
                                font=('Arial', 20, 'bold'))

def update_score():
    global high_score
    score_label.config(text=f"Score: {score}")
    if score > high_score:
        high_score = score
        high_score_label.config(text=f"High Score: {high_score}")

def add_new_tile():
    empty = [(r,c) for r in range(4) for c in range(4) if board[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        board[r][c] = 2 if random.random() < 0.9 else 4

def move(direction):
    global score
    moved = False
    board_copy = [row[:] for row in board]
    
    if direction in ('left', 'right'):
        for row in range(4):
            non_zero = [n for n in board[row] if n != 0]
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
                    score += non_zero[i]*2
                    skip = True
                else:
                    merged.append(non_zero[i])
            
            merged += [0]*(4 - len(merged))
            if direction == 'right':
                merged = merged[::-1]
            
            if board[row] != merged:
                moved = True
                board[row] = merged
    
    elif direction in ('up', 'down'):
        for col in range(4):
            column = [board[row][col] for row in range(4)]
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
                    score += non_zero[i]*2
                    skip = True
                else:
                    merged.append(non_zero[i])
            
            merged += [0]*(4 - len(merged))
            if direction == 'down':
                merged = merged[::-1]
            
            if column != merged:
                moved = True
                for row in range(4):
                    board[row][col] = merged[row]
    
    if moved:
        update_score()
        add_new_tile()
        draw_board()
        
        if is_game_over():
            messagebox.showinfo("Game Over", f"Game Over! Score: {score}")

def is_game_over():
    # Check for empty spaces
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                return False
    
    # Check for possible merges
    for row in range(4):
        for col in range(3):
            if board[row][col] == board[row][col+1]:
                return False
    
    for col in range(4):
        for row in range(3):
            if board[row][col] == board[row+1][col]:
                return False
    
    return True

# Key bindings
root.bind('<Left>', lambda e: move('left'))
root.bind('<Right>', lambda e: move('right'))
root.bind('<Up>', lambda e: move('up'))
root.bind('<Down>', lambda e: move('down'))

start_game()
root.mainloop()
