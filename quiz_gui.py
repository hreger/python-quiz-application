import tkinter as tk
from tkinter import simpledialog, messagebox
import quiz_backend as backend

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")

        self.dark_mode = True  # Set dark mode as default for modern indie game UI
        self.developer_mode = False

        self.questions = backend.load_questions('questions.toml')
        self.users = backend.load_users('users.toml')
        self.current_user = None
        self.current_question_index = 0
        self.score = 0

        # Initialize theme variables
        self.dev_mode_var = tk.BooleanVar(value=self.developer_mode)
        self.dark_mode_var = tk.BooleanVar(value=self.dark_mode)

        # Main container frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create subframes for different content areas
        self.frames = {}
        self.create_frames()

        # Show main menu frame initially
        self.show_frame("main_menu")

    def create_frames(self):
        # Main Menu Frame
        main_menu = tk.Frame(self.main_frame)
        self.frames["main_menu"] = main_menu

        tk.Label(main_menu, text="Welcome to the Quiz App", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(main_menu, text="Start Quiz", command=lambda: self.show_frame("quiz"), width=20, height=2).pack(pady=10)
        tk.Button(main_menu, text="Manage Users", command=lambda: self.show_frame("manage_users"), width=20, height=2).pack(pady=10)
        tk.Button(main_menu, text="Manage Questions", command=lambda: self.show_frame("manage_questions"), width=20, height=2).pack(pady=10)
        tk.Button(main_menu, text="Leaderboard", command=lambda: self.show_frame("leaderboard"), width=20, height=2).pack(pady=10)
        tk.Button(main_menu, text="Multiplayer Mode", command=lambda: self.show_frame("multiplayer"), width=20, height=2).pack(pady=10)

        tk.Checkbutton(main_menu, text="Developer Mode", variable=self.dev_mode_var, command=self.toggle_developer_mode).pack(pady=10)
        tk.Checkbutton(main_menu, text="Dark Mode", variable=self.dark_mode_var, command=self.toggle_dark_mode).pack(pady=10)

        tk.Button(main_menu, text="Exit", command=self.root.quit, width=20, height=2).pack(pady=10)

        # Quiz Frame
        quiz_frame = tk.Frame(self.main_frame)
        self.frames["quiz"] = quiz_frame

        # Manage Users Frame
        manage_users = tk.Frame(self.main_frame)
        self.frames["manage_users"] = manage_users

        # Manage Questions Frame
        manage_questions = tk.Frame(self.main_frame)
        self.frames["manage_questions"] = manage_questions

        # Leaderboard Frame
        leaderboard = tk.Frame(self.main_frame)
        self.frames["leaderboard"] = leaderboard

        # Multiplayer Frame
        multiplayer = tk.Frame(self.main_frame)
        self.frames["multiplayer"] = multiplayer

    def show_frame(self, frame_name):
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()
        # Show the requested frame
        frame = self.frames[frame_name]
        frame.pack(fill=tk.BOTH, expand=True)
        self.apply_theme()

        # Call frame-specific setup if needed
        if frame_name == "main_menu":
            self.setup_main_menu_frame()
        elif frame_name == "quiz":
            self.setup_quiz_frame()
        elif frame_name == "manage_users":
            self.setup_manage_users_frame()
        elif frame_name == "manage_questions":
            self.setup_manage_questions_frame()
        elif frame_name == "leaderboard":
            self.setup_leaderboard_frame()
        elif frame_name == "multiplayer":
            self.setup_multiplayer_frame()

    def setup_main_menu_frame(self):
        # Update checkbutton variables
        self.dev_mode_var.set(self.developer_mode)
        self.dark_mode_var.set(self.dark_mode)

    def setup_quiz_frame(self):
        frame = self.frames["quiz"]
        for widget in frame.winfo_children():
            widget.destroy()

        self.current_user = simpledialog.askstring("User", "Enter your username:")
        if not self.current_user or self.current_user.strip() == "":
            messagebox.showwarning("Warning", "Username cannot be empty!")
            self.show_frame("main_menu")
            return

        if not any(user['username'] == self.current_user for user in self.users):
            self.users.append({"username": self.current_user, "score": 0, "current_game": ""})
            backend.save_users('users.toml', self.users)

        self.current_question_index = 0
        self.score = 0

        self.show_question()

    def show_question(self):
        frame = self.frames["quiz"]
        for widget in frame.winfo_children():
            widget.destroy()

        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]

            tk.Label(frame, text=question['text'], font=("Arial", 14)).pack(pady=10)
            self.option_vars = []
            self.selected_option = tk.IntVar()

            for i, option in enumerate(question['options'], 1):
                tk.Radiobutton(frame, text=option, variable=self.selected_option, value=i, font=("Arial", 12)).pack(anchor=tk.W)

            tk.Button(frame, text="Submit Answer", command=self.submit_answer, width=20, height=2).pack(pady=10)

            nav_frame = tk.Frame(frame)
            nav_frame.pack(pady=10, fill=tk.X)

            if self.current_question_index > 0:
                tk.Button(nav_frame, text="Previous Question", command=self.previous_question, width=20, height=2).pack(side=tk.LEFT, padx=10)
            if self.current_question_index < len(self.questions) - 1:
                tk.Button(nav_frame, text="Next Question", command=self.next_question, width=20, height=2).pack(side=tk.RIGHT, padx=10)
        else:
            self.end_quiz()

    def submit_answer(self):
        choice = self.selected_option.get()
        if choice == 0:
            messagebox.showwarning("Warning", "Please select an option!")
            return

        if backend.ask_question(self.questions[self.current_question_index], choice):
            self.score += 1
            messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            messagebox.showinfo("Wrong!", f"The correct answer was: {self.questions[self.current_question_index]['answer']}")

        self.current_question_index += 1
        self.show_question()

    def previous_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question()

    def next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.show_question()

    def end_quiz(self):
        frame = self.frames["quiz"]
        for widget in frame.winfo_children():
            widget.destroy()

        self.users = backend.update_user_best_score(self.users, self.current_user, self.score)
        backend.save_users('users.toml', self.users)
        best_score = backend.get_user_best_score(self.users, self.current_user)

        tk.Label(frame, text="Thank You for Playing!", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(frame, text=f"Your Personal Best Score: {best_score}", font=("Arial", 14)).pack(pady=10)
        tk.Button(frame, text="View Leaderboard", command=lambda: self.show_frame("leaderboard"), width=20, height=2).pack(pady=10)
        tk.Button(frame, text="Back to Main Menu", command=lambda: self.show_frame("main_menu"), width=20, height=2).pack(pady=10)

    def setup_manage_users_frame(self):
        frame = self.frames["manage_users"]
        for widget in frame.winfo_children():
            widget.destroy()

        if not self.developer_mode:
            messagebox.showwarning("Warning", "Developer mode is required to manage users.")
            self.show_frame("main_menu")
            return

        tk.Label(frame, text="Manage Users", font=("Arial", 18, "bold")).pack(pady=20)

        for user in self.users:
            user_frame = tk.Frame(frame)
            user_frame.pack(pady=5)
            tk.Label(user_frame, text=f"User: {user['username']}, Score: {user['score']}", font=("Arial", 12)).pack(side=tk.LEFT)
            tk.Button(user_frame, text="Delete User", command=lambda u=user['username']: self.delete_user(u), width=15).pack(side=tk.RIGHT)

        tk.Button(frame, text="Back to Main Menu", command=lambda: self.show_frame("main_menu"), width=20, height=2).pack(pady=10)

    def delete_user(self, username):
        self.users = backend.delete_user(self.users, username)
        backend.save_users('users.toml', self.users)
        self.setup_manage_users_frame()

    def manage_users(self):
        self.show_frame("manage_users")

    def setup_manage_questions_frame(self):
        frame = self.frames["manage_questions"]
        for widget in frame.winfo_children():
            widget.destroy()

        if not self.developer_mode:
            messagebox.showwarning("Warning", "Developer mode is required to manage questions.")
            self.show_frame("main_menu")
            return

        tk.Label(frame, text="Manage Questions", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(frame, text="Back", command=lambda: self.show_frame("main_menu"), width=10).pack(pady=5)

        for idx, question in enumerate(self.questions):
            question_frame = tk.Frame(frame)
            question_frame.pack(pady=5, fill=tk.X, padx=20)

            tk.Label(question_frame, text=f"{idx+1}. {question['text']}", font=("Arial", 12), anchor="w").pack(side=tk.LEFT, expand=True, fill=tk.X)
            tk.Button(question_frame, text="Edit", command=lambda i=idx: self.edit_question(i), width=10).pack(side=tk.RIGHT, padx=5)

        tk.Label(frame, text="Add New Question:", font=("Arial", 14)).pack(pady=10)

        def add_field(label):
            tk.Label(frame, text=label, font=("Arial", 12)).pack()
            entry = tk.Entry(frame, font=("Arial", 12))
            entry.pack(pady=5)
            return entry

        category_entry = add_field("Category:")
        difficulty_entry = add_field("Difficulty:")
        question_entry = add_field("Question:")
        options_entry = add_field("Options (comma-separated):")
        answer_entry = add_field("Answer:")
        feedback_entry = add_field("Feedback:")

        def submit_new_question():
            category = category_entry.get()
            difficulty = difficulty_entry.get()
            text = question_entry.get()
            options = [option.strip() for option in options_entry.get().split(',')]
            answer = answer_entry.get()
            feedback = feedback_entry.get()

            if category and difficulty and text and options and answer:
                self.questions = backend.add_question(self.questions, category, difficulty, text, options, answer, feedback)
                backend.save_questions('questions.toml', self.questions)
                messagebox.showinfo("Success", "New question submitted successfully!")
                self.setup_manage_questions_frame()
            else:
                messagebox.showwarning("Warning", "All fields must be filled!")

        submit_button = tk.Button(frame, text="Submit New Question", command=submit_new_question, width=20, height=2)
        submit_button.pack(pady=10)

        tk.Button(frame, text="Back to Main Menu", command=lambda: self.show_frame("main_menu"), width=20, height=2).pack(pady=10)

    def manage_questions(self):
        self.show_frame("manage_questions")

    def edit_question(self, index):
        frame = self.frames["manage_questions"]
        for widget in frame.winfo_children():
            widget.destroy()

        question = self.questions[index]

        tk.Label(frame, text="Edit Question", font=("Arial", 18, "bold")).pack(pady=20)

        def add_field(label, value):
            tk.Label(frame, text=label, font=("Arial", 12)).pack()
            entry = tk.Entry(frame, font=("Arial", 12))
            entry.insert(0, value)
            entry.pack(pady=5)
            return entry

        category_entry = add_field("Category:", question['category'])
        difficulty_entry = add_field("Difficulty:", question['difficulty'])
        text_entry = add_field("Question:", question['text'])
        options_entry = add_field("Options (comma-separated):", ",".join(question['options']))
        answer_entry = add_field("Answer:", question['answer'])
        feedback_entry = add_field("Feedback:", question['feedback'])

        def submit_edit():
            self.questions[index] = {
                'category': category_entry.get(),
                'difficulty': difficulty_entry.get(),
                'text': text_entry.get(),
                'options': [o.strip() for o in options_entry.get().split(',')],
                'answer': answer_entry.get(),
                'feedback': feedback_entry.get()
            }
            backend.save_questions('questions.toml', self.questions)
            messagebox.showinfo("Success", "Question updated successfully!")
            self.setup_manage_questions_frame()

        tk.Button(frame, text="Submit Changes", command=submit_edit, width=20, height=2).pack(pady=10)
        tk.Button(frame, text="Back to Manage Questions", command=self.setup_manage_questions_frame, width=20, height=2).pack(pady=10)

    def show_leaderboard_frame(self):
        frame = self.frames["leaderboard"]
        for widget in frame.winfo_children():
            widget.destroy()

        tk.Label(frame, text="Leaderboard", font=("Arial", 18, "bold")).pack(pady=20)

        leaderboard = backend.get_leaderboard(self.users)
        for user in leaderboard:
            tk.Label(frame, text=f"User: {user['username']}, Score: {user['score']}", font=("Arial", 12)).pack()

        tk.Button(frame, text="Back to Main Menu", command=lambda: self.show_frame("main_menu"), width=20, height=2).pack(pady=10)

    def show_leaderboard(self):
        self.show_frame("leaderboard")
        self.show_leaderboard_frame()

    def setup_multiplayer_frame(self):
        frame = self.frames["multiplayer"]
        for widget in frame.winfo_children():
            widget.destroy()

        tk.Label(frame, text="Multiplayer Mode", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(frame, text="Player 1 Username:", font=("Arial", 12)).pack(pady=5)
        player1_entry = tk.Entry(frame, font=("Arial", 12))
        player1_entry.pack(pady=5)

        tk.Label(frame, text="Player 2 Username:", font=("Arial", 12)).pack(pady=5)
        player2_entry = tk.Entry(frame, font=("Arial", 12))
        player2_entry.pack(pady=5)

        def start_game():
            player1 = player1_entry.get()
            player2 = player2_entry.get()

            if player1 and player2:
                self.users, game_id = backend.start_multiplayer_game(self.users, player1, player2)
                backend.save_users('users.toml', self.users)
                messagebox.showinfo("Game Started", f"Game started between {player1} and {player2} with ID: {game_id}")
                self.show_frame("main_menu")
            else:
                messagebox.showwarning("Warning", "Both usernames must be provided!")

        tk.Button(frame, text="Start Game", command=start_game, width=20, height=2).pack(pady=10)
        tk.Button(frame, text="Back to Main Menu", command=lambda: self.show_frame("main_menu"), width=20, height=2).pack(pady=10)

    def start_multiplayer(self):
        self.show_frame("multiplayer")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def toggle_developer_mode(self):
        self.developer_mode = self.dev_mode_var.get()
        # Do not change dark_mode or dark_mode_var here to keep UI consistent
        self.apply_theme()

    def toggle_dark_mode(self):
        self.dark_mode = self.dark_mode_var.get()
        self.apply_theme()

    def apply_theme(self):
        # Indie game-like style palette
        if not self.dark_mode:
            bg_color = "#1e1e2f"  # dark navy
            fg_color = "#f0f0f0"  # off-white
            button_bg = "#6c5ce7"  # vibrant purple
            button_fg = "#f0f0f0"  # off-white
        else:
            bg_color = "#121212"  # almost black
            fg_color = "#dfe6e9"  # light gray
            button_bg = "#00cec9"  # bright teal
            button_fg = "#dfe6e9"  # light gray

        self.root.configure(bg=bg_color)

        # Apply theme to main frame and all subframes and their widgets
        def apply_to_widgets(widget):
            try:
                widget.configure(bg=bg_color, fg=fg_color, font=("Courier New", 12, "bold"))
            except tk.TclError:
                pass
            if isinstance(widget, tk.Button):
                try:
                    widget.configure(bg=button_bg, fg=button_fg, activebackground=button_fg, activeforeground=button_bg, relief=tk.RAISED, borderwidth=3, font=("Courier New", 12, "bold"))
                except tk.TclError:
                    pass
            for child in widget.winfo_children():
                apply_to_widgets(child)

        apply_to_widgets(self.main_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
