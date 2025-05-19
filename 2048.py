import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

root = tk.Tk()
root.title("2048")

grid_size = 4
board = [[0]*4 for _ in range(4)]
score = 0
high_score = 0
move_history = []
auto_playing = False

# Game UI
score_frame = tk.Frame(root)
score_frame.pack()

score_label = tk.Label(score_frame, text="Score: 0", font=('Arial', 12))
score_label.pack(side='left', padx=10)

high_score_label = tk.Label(score_frame, text="High Score: 0", font=('Arial', 12))
high_score_label.pack(side='left', padx=10)

canvas = tk.Canvas(root, width=300, height=300, bg='#bbada0')
canvas.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

def start_game():
    global board, score, move_history
    board = [[0]*4 for _ in range(4)]
    score = 0
    move_history = []
    update_score()
    add_new_tile()
    add_new_tile()
    draw_board()

def undo_move():
    global board, score, move_history
    if move_history:
        board, score = move_history.pop()
        update_score()
        draw_board()

restart_button = tk.Button(button_frame, text="Restart", command=start_game)
restart_button.pack(side='left', padx=5)

undo_button = tk.Button(button_frame, text="Undo", command=undo_move)
undo_button.pack(side='left', padx=5)

auto_play_button = tk.Button(button_frame, text="Auto Play", command=lambda: auto_play(True))
auto_play_button.pack(side='left', padx=5)

stop_button = tk.Button(button_frame, text="Stop", command=lambda: auto_play(False), state=tk.DISABLED)
stop_button.pack(side='left', padx=5)

def draw_board():
    canvas.delete('all')
    for row in range(4):
        for col in range(4):
            x1 = col * 75 + 5
            y1 = row * 75 + 5
            x2 = x1 + 70
            y2 = y1 + 70
            
            value = board[row][col]
            color = get_tile_color(value)
            
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            if value:
                text_color = '#776e65' if value < 8 else '#f9f6f2'
                canvas.create_text((x1+x2)/2, (y1+y2)/2, 
                                text=str(value), 
                                font=('Arial', 20, 'bold'),
                                fill=text_color)

def get_tile_color(value):
    colors = {
        0: '#cdc1b4',
        2: '#eee4da',
        4: '#ede0c8',
        8: '#f2b179',
        16: '#f59563',
        32: '#f67c5f',
        64: '#f65e3b',
        128: '#edcf72',
        256: '#edcc61',
        512: '#edc850',
        1024: '#edc53f',
        2048: '#edc22e'
    }
    return colors.get(value, '#3c3a32')

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

def move(direction, record_move=True):
    global score, move_history, auto_playing
    
    if auto_playing and not record_move:
        pass  # Allow computer moves without recording
    elif auto_playing:
        return False  # Don't allow manual moves during auto play
    
    if record_move:
        move_history.append(([row[:] for row in board], score))
    
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
            return False
        return True
    return False

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

def auto_play(start):
    global auto_playing
    
    if start:
        auto_playing = True
        auto_play_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        computer_move()
    else:
        auto_playing = False
        auto_play_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

def computer_move():
    global board, score
    
    if not auto_playing or is_game_over():
        auto_play(False)
        if is_game_over():
            messagebox.showinfo("Game Over", f"Game Over! Score: {score}")
        return
    
    directions = ['left', 'up', 'right', 'down']
    moved = False
    
    for direction in directions:
        if move(direction, record_move=False):
            moved = True
            break
    
    if not moved:
        for direction in directions:
            board_backup = [row[:] for row in board]
            score_backup = score
            if move(direction, record_move=False):
                moved = True
                break
            board = [row[:] for row in board_backup]
            score = score_backup
    
    if moved:
        root.after(100, computer_move)
    else:
        auto_play(False)
        messagebox.showinfo("Game Over", f"Game Over! Score: {score}")

# Key bindings
root.bind('<Left>', lambda e: move('left'))
root.bind('<Right>', lambda e: move('right'))
root.bind('<Up>', lambda e: move('up'))
root.bind('<Down>', lambda e: move('down'))

start_game()
root.mainloop()
