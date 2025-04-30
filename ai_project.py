import customtkinter as ctk
from tkinter import messagebox
import random
import pygame

pygame.mixer.init()
click_sound = pygame.mixer.Sound("click.wav")
win_sound = pygame.mixer.Sound("win.wav")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Tic-Tac-Toe Game")
app.geometry("400x550")

current_player = "X"
player_names = {"X": "Player 1", "O": "Player 2"}
scores = {"X": 0, "O": 0}
buttons = []
game_mode = "PvP"
difficulty = "Easy"
move_history = []

widgets_stack = []

def clear_widgets():
    while widgets_stack:
        widgets_stack.pop().destroy()

def switch_player():
    global current_player
    current_player = "O" if current_player == "X" else "X"
    turn_label.configure(text=f"Turn: {player_names[current_player]} ({current_player})")

def check_winner():
    for i in range(3):
        if buttons[i][0].cget("text") == buttons[i][1].cget("text") == buttons[i][2].cget("text") != "":
            return buttons[i][0].cget("text")
        if buttons[0][i].cget("text") == buttons[1][i].cget("text") == buttons[2][i].cget("text") != "":
            return buttons[0][i].cget("text")
    if buttons[0][0].cget("text") == buttons[1][1].cget("text") == buttons[2][2].cget("text") != "":
        return buttons[0][0].cget("text")
    if buttons[0][2].cget("text") == buttons[1][1].cget("text") == buttons[2][0].cget("text") != "":
        return buttons[0][2].cget("text")
    return None

def is_draw():
    return all(buttons[i][j].cget("text") != "" for i in range(3) for j in range(3))

def on_click(row, col):
    if buttons[row][col].cget("text") == "":
        click_sound.play()
        buttons[row][col].configure(
            text=current_player,
            text_color="red" if current_player == "X" else "yellow"
        )
        move_history.append((row, col, current_player))
        winner = check_winner()
        if winner:
            scores[winner] += 1
            update_score()
            win_sound.play()
            app.after(800, lambda: show_end_dialog(winner))
        elif is_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_board()
        else:
            switch_player()
            if game_mode == "PvC" and current_player == "O":
                app.after(500, ai_play)

def show_end_dialog(winner):
    response = messagebox.askquestion("Round Over", f"{player_names[winner]} won!\nWould you like to play again?")
    if response == 'yes':
        reset_board()
    else:
        app.destroy()

def reset_board():
    global current_player
    current_player = "X"
    turn_label.configure(text=f"Turn: {player_names[current_player]} ({current_player})")
    for i in range(3):
        for j in range(3):
            buttons[i][j].configure(text="")
    move_history.clear()

def reset_scores():
    global scores
    scores = {"X": 0, "O": 0}
    update_score()

def update_score():
    score_label.configure(
        text=f"{player_names['X']} (X): {scores['X']}   |   {player_names['O']} (O): {scores['O']}"
    )

def show_mode_selection():
    clear_widgets()
    title = ctk.CTkLabel(app, text="Select Game Mode", font=("Arial", 24, "bold"))
    title.pack(pady=20)
    widgets_stack.append(title)

    btn1 = ctk.CTkButton(app, text="Player vs Player", command=lambda: choose_mode("PvP"), font=("Arial", 16))
    btn1.pack(pady=10)
    widgets_stack.append(btn1)

    btn2 = ctk.CTkButton(app, text="Player vs Computer", command=lambda: choose_mode("PvC"), font=("Arial", 16))
    btn2.pack(pady=10)
    widgets_stack.append(btn2)

def choose_mode(mode):
    global game_mode
    game_mode = mode
    ask_difficulty()

def ask_difficulty():
    clear_widgets()

    difficulty_label = ctk.CTkLabel(app, text="Select Difficulty", font=("Arial", 24, "bold"))
    difficulty_label.pack(pady=20)
    widgets_stack.append(difficulty_label)

    easy_btn = ctk.CTkButton(app, text="Easy", command=lambda: choose_difficulty("Easy"), font=("Arial", 16))
    easy_btn.pack(pady=10)
    widgets_stack.append(easy_btn)

    medium_btn = ctk.CTkButton(app, text="Medium", command=lambda: choose_difficulty("Medium"), font=("Arial", 16))
    medium_btn.pack(pady=10)
    widgets_stack.append(medium_btn)

    hard_btn = ctk.CTkButton(app, text="Hard", command=lambda: choose_difficulty("Hard"), font=("Arial", 16))
    hard_btn.pack(pady=10)
    widgets_stack.append(hard_btn)

    back_btn = ctk.CTkButton(app, text="Back", command=show_mode_selection, font=("Arial", 16))
    back_btn.pack(pady=10)
    widgets_stack.append(back_btn)

def choose_difficulty(diff):
    global difficulty
    difficulty = diff
    ask_names()

def ask_names():
    clear_widgets()
    global entry1, entry2, start_btn

    entry1 = ctk.CTkEntry(app, placeholder_text="Your Name (X)")
    entry1.pack(pady=10)
    widgets_stack.append(entry1)

    if game_mode == "PvP":
        entry2 = ctk.CTkEntry(app, placeholder_text="Second Player's Name (O)")
        entry2.pack(pady=10)
        widgets_stack.append(entry2)
    else:
        entry2 = None

    start_btn = ctk.CTkButton(app, text="Start Game", command=start_game, font=("Arial", 16))
    start_btn.pack(pady=10)
    widgets_stack.append(start_btn)

    back_btn = ctk.CTkButton(app, text="Back", command=ask_difficulty, font=("Arial", 16))
    back_btn.pack(pady=10)
    widgets_stack.append(back_btn)

def start_game():
    player_names["X"] = entry1.get() or "Player 1"
    if game_mode == "PvP":
        player_names["O"] = entry2.get() or "Player 2"
    else:
        player_names["O"] = "AI"
    setup_game()

def setup_game():
    clear_widgets()
    global turn_label, score_label, buttons
    buttons.clear()

    turn_label = ctk.CTkLabel(app, text=f"Turn: {player_names[current_player]} (X)", font=("Arial", 18))
    turn_label.pack(pady=10)
    widgets_stack.append(turn_label)

    score_label = ctk.CTkLabel(app, text="", font=("Arial", 16))
    score_label.pack()
    widgets_stack.append(score_label)
    update_score()

    frame = ctk.CTkFrame(app)
    frame.pack(pady=20)
    widgets_stack.append(frame)

    for i in range(3):
        row = []
        for j in range(3):
            btn = ctk.CTkButton(frame, text="", width=80, height=80, font=("Arial", 32),
                                command=lambda r=i, c=j: on_click(r, c))
            btn.grid(row=i, column=j, padx=5, pady=5)
            row.append(btn)
        buttons.append(row)

    reset_btn = ctk.CTkButton(app, text="Restart Game", command=reset_board)
    reset_btn.pack(pady=10)
    widgets_stack.append(reset_btn)

    reset_scores_btn = ctk.CTkButton(app, text="Reset Scores", command=reset_scores)
    reset_scores_btn.pack(pady=10)
    widgets_stack.append(reset_scores_btn)

    back_to_menu_btn = ctk.CTkButton(app, text="Back to Menu", command=show_mode_selection)
    back_to_menu_btn.pack(pady=10)
    widgets_stack.append(back_to_menu_btn)

def ai_play():
    if difficulty == "Easy":
        easy_ai_move()
    elif difficulty == "Medium":
        medium_ai_move()
    else:
        hard_ai_move()

def easy_ai_move():
    empty_cells = [(i, j) for i in range(3) for j in range(3) if buttons[i][j].cget("text") == ""]
    if empty_cells:
        row, col = random.choice(empty_cells)
        on_click(row, col)

def medium_ai_move():
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if buttons[i][j].cget("text") == "":
                buttons[i][j].configure(text="O")
                score = minimax(False, 2)
                buttons[i][j].configure(text="")
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        on_click(best_move[0], best_move[1])

def hard_ai_move():
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if buttons[i][j].cget("text") == "":
                buttons[i][j].configure(text="O")
                score = minimax(False, 5)
                buttons[i][j].configure(text="")
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        on_click(best_move[0], best_move[1])

def minimax(is_maximizing, depth):
    winner = check_winner()
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif is_draw():
        return 0
    if depth == 0:
        return 0
    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if buttons[i][j].cget("text") == "":
                    buttons[i][j].configure(text="O")
                    score = minimax(False, depth - 1)
                    buttons[i][j].configure(text="")
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if buttons[i][j].cget("text") == "":
                    buttons[i][j].configure(text="X")
                    score = minimax(True, depth - 1)
                    buttons[i][j].configure(text="")
                    best_score = min(score, best_score)
        return best_score

show_mode_selection()
app.mainloop()