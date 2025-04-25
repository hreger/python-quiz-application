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

        self.setup_main_menu()

    def setup_main_menu(self):
        self.clear_frame()
        self.apply_theme()

        tk.Label(self.root, text="Welcome to the Quiz App", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(self.root, text="Start Quiz", command=self.start_quiz, width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Manage Users", command=self.manage_users, width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Manage Questions", command=self.manage_questions, width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Leaderboard", command=self.show_leaderboard, width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Multiplayer Mode", command=self.start_multiplayer, width=20, height=2).pack(pady=10)

        # Developer Mode Toggle
        self.dev_mode_var = tk.BooleanVar(value=self.developer_mode)
        tk.Checkbutton(
            self.root, text="Developer Mode", variable=self.dev_mode_var, command=self.toggle_developer_mode
        ).pack(pady=10)

        # Dark/Light Mode Toggle
        self.dark_mode_var = tk.BooleanVar(value=self.dark_mode)
        tk.Checkbutton(
            self.root, text="Dark Mode", variable=self.dark_mode_var, command=self.toggle_dark_mode
        ).pack(pady=10)

        tk.Button(self.root, text="Exit", command=self.root.quit, width=20, height=2).pack(pady=10)

    def toggle_developer_mode(self):
        self.developer_mode = self.dev_mode_var.get()
        # Do not change dark_mode or dark_mode_var here to keep UI consistent
        self.apply_theme()
        # Removed call to setup_main_menu to keep UI consistent on toggle

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

        for widget in self.root.winfo_children():
            # Apply colors and indie game font
            try:
                widget.configure(bg=bg_color, fg=fg_color, font=("Courier New", 12, "bold"))
            except tk.TclError:
                # Some widgets may not support fg/bg/font config
                pass
            # For buttons, apply button colors and rounded style if possible
            if isinstance(widget, tk.Button):
                try:
                    widget.configure(bg=button_bg, fg=button_fg, activebackground=button_fg, activeforeground=button_bg, relief=tk.RAISED, borderwidth=3, font=("Courier New", 12, "bold"))
                except tk.TclError:
                    pass

    def start_quiz(self):
        self.clear_frame()
        self.apply_theme()
        self.current_user = simpledialog.askstring("User", "Enter your username:")
        if not self.current_user or self.current_user.strip() == "":
            messagebox.showwarning("Warning", "Username cannot be empty!")
            self.setup_main_menu()
            return

        if not any(user['username'] == self.current_user for user in self.users):
            self.users.append({"username": self.current_user, "score": 0, "current_game": ""})
            backend.save_users('users.toml', self.users)

        self.current_question_index = 0
        self.score = 0
        self.ask_question()

        # Bind arrow keys for navigation
        self.root.bind("<Left>", self.previous_question)
        self.root.bind("<Right>", self.next_question)

    def ask_question(self, index=None):
        self.clear_frame()
        self.apply_theme()
        if index is not None:
            self.current_question_index = index

        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]

            tk.Label(self.root, text=question['text'], font=("Arial", 14)).pack(pady=10)
            self.option_vars = []
            for i, option in enumerate(question['options'], 1):
                var = tk.IntVar()
                tk.Radiobutton(self.root, text=option, variable=var, value=i, font=("Arial", 12)).pack(anchor=tk.W)
                self.option_vars.append(var)

            tk.Button(self.root, text="Submit Answer", command=self.submit_answer, width=20, height=2).pack(pady=10)
            
            # Navigation Buttons
            if self.current_question_index > 0:
                tk.Button(self.root, text="Previous Question", command=self.previous_question, width=20, height=2).pack(side=tk.LEFT, padx=10, pady=10)
            if self.current_question_index < len(self.questions) - 1:
                tk.Button(self.root, text="Next Question", command=self.next_question, width=20, height=2).pack(side=tk.RIGHT, padx=10, pady=10)

    def submit_answer(self):
        choice = next((var.get() for var in self.option_vars if var.get() > 0), None)
        if choice is None:
            messagebox.showwarning("Warning", "Please select an option!")
            return

        if backend.ask_question(self.questions[self.current_question_index], choice):
            self.score += 1
            messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            messagebox.showinfo("Wrong!", f"The correct answer was: {self.questions[self.current_question_index]['answer']}")

        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.ask_question()
        else:
            self.end_quiz()

    def previous_question(self, event=None):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.ask_question()

    def next_question(self, event=None):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.ask_question()

    def end_quiz(self):
        self.clear_frame()
        self.apply_theme()
        self.users = backend.update_user_best_score(self.users, self.current_user, self.score)
        backend.save_users('users.toml', self.users)
        best_score = backend.get_user_best_score(self.users, self.current_user)

        tk.Label(self.root, text="Thank You for Playing!", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"Your Personal Best Score: {best_score}", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="View Leaderboard", command=self.show_leaderboard, width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu, width=20, height=2).pack(pady=10)

    def manage_users(self):
        self.clear_frame()
        self.apply_theme()
        tk.Label(self.root, text="Manage Users", font=("Arial", 18, "bold")).pack(pady=20)

        if not self.developer_mode:
            messagebox.showwarning("Warning", "Developer mode is required to manage users.")
            self.setup_main_menu()
            return

        tk.Label(self.root, text="Users:", font=("Arial", 14)).pack(pady=10)

        for user in self.users:
            user_frame = tk.Frame(self.root)
            user_frame.pack(pady=5)
            tk.Label(user_frame, text=f"User: {user['username']}, Score: {user['score']}", font=("Arial", 12)).pack(side=tk.LEFT)
            tk.Button(user_frame, text="Delete User", command=lambda u=user['username']: self.delete_user(u), width=15).pack(side=tk.RIGHT)

        tk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu, width=20, height=2).pack(pady=10)

    def delete_user(self, username):
        self.users = backend.delete_user(self.users, username)
        backend.save_users('users.toml', self.users)
        self.manage_users()

    def manage_questions(self):
        self.clear_frame()
        self.apply_theme()
        tk.Label(self.root, text="Manage Questions", font=("Arial", 18, "bold")).pack(pady=20)

        # Add Back button at the top
        tk.Button(self.root, text="Back", command=self.setup_main_menu, width=10).pack(pady=5)

        if not self.developer_mode:
            messagebox.showwarning("Warning", "Developer mode is required to manage questions.")
            self.setup_main_menu()
            return

        tk.Label(self.root, text="Current Questions:", font=("Arial", 14)).pack(pady=10)

        for idx, question in enumerate(self.questions):
            question_frame = tk.Frame(self.root)
            question_frame.pack(pady=5, fill=tk.X, padx=20)

            tk.Label(question_frame, text=f"{idx+1}. {question['text']}", font=("Arial", 12), anchor="w").pack(side=tk.LEFT, expand=True, fill=tk.X)
            tk.Button(question_frame, text="Edit", command=lambda i=idx: self.edit_question(i), width=10).pack(side=tk.RIGHT, padx=5)

        # Add New Question Section
        tk.Label(self.root, text="Add New Question:", font=("Arial", 14)).pack(pady=10)

        def add_field(label):
            tk.Label(self.root, text=label, font=("Arial", 12)).pack()
            entry = tk.Entry(self.root, font=("Arial", 12))
            entry.pack(pady=5)
            return entry

        category_entry = add_field("Category:")
        difficulty_entry = add_field("Difficulty:")
        question_entry = add_field("Question:")
        options_entry = add_field("Options (comma-separated):")
        answer_entry = add_field("Answer:")
        feedback_entry = add_field("Feedback:")

        def add_question():
            category = category_entry.get()
            difficulty = difficulty_entry.get()
            text = question_entry.get()
            options = [option.strip() for option in options_entry.get().split(',')]
            answer = answer_entry.get()
            feedback = feedback_entry.get()

            if category and difficulty and text and options and answer:
                self.questions = backend.add_question(self.questions, category, difficulty, text, options, answer, feedback)
                backend.save_questions('questions.toml', self.questions)
                messagebox.showinfo("Success", "Question added successfully!")
                self.manage_questions()
            else:
                messagebox.showwarning("Warning", "All fields must be filled!")

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
                self.manage_questions()
            else:
                messagebox.showwarning("Warning", "All fields must be filled!")

        # Remove the old "Submit" button and add "Submit New Question" button immediately after Feedback entry
        submit_button = tk.Button(self.root, text="Submit New Question", command=submit_new_question, width=20, height=2)
        submit_button.pack(pady=10)
        
        tk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu, width=20, height=2).pack(pady=10)

        pass

    def edit_question(self, index):
        self.clear_frame()
        self.apply_theme()

        question = self.questions[index]

        tk.Label(self.root, text="Edit Question", font=("Arial", 18, "bold")).pack(pady=20)

        # Editable fields with pre-filled data
        def add_field(label, value):
            tk.Label(self.root, text=label, font=("Arial", 12)).pack()
            entry = tk.Entry(self.root, font=("Arial", 12))
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
            self.manage_questions()

        tk.Button(self.root, text="Submit Changes", command=submit_edit, width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Back to Manage Questions", command=self.manage_questions, width=20, height=2).pack(pady=10)

        pass
    
    def delete_question(self, index):
        self.questions = backend.delete_question(self.questions, index)
        backend.save_questions('questions.toml', self.questions)
        messagebox.showinfo("Success", f"Question {index+1} deleted successfully!")
        self.manage_questions()

        pass

    def show_leaderboard(self):
        self.clear_frame()
        self.apply_theme()
        tk.Label(self.root, text="Leaderboard", font=("Arial", 18, "bold")).pack(pady=20)

        leaderboard = backend.get_leaderboard(self.users)
        for user in leaderboard:
            tk.Label(self.root, text=f"User: {user['username']}, Score: {user['score']}", font=("Arial", 12)).pack()

        tk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu, width=20, height=2).pack(pady=10)

        pass

    def start_multiplayer(self):
        self.clear_frame()
        self.apply_theme()
        tk.Label(self.root, text="Multiplayer Mode", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self.root, text="Player 1 Username:", font=("Arial", 12)).pack(pady=5)
        player1_entry = tk.Entry(self.root, font=("Arial", 12))
        player1_entry.pack(pady=5)

        tk.Label(self.root, text="Player 2 Username:", font=("Arial", 12)).pack(pady=5)
        player2_entry = tk.Entry(self.root, font=("Arial", 12))
        player2_entry.pack(pady=5)

        def start_game():
            player1 = player1_entry.get()
            player2 = player2_entry.get()

            if player1 and player2:
                self.users, game_id = backend.start_multiplayer_game(self.users, player1, player2)
                backend.save_users('users.toml', self.users)
                messagebox.showinfo("Game Started", f"Game started between {player1} and {player2} with ID: {game_id}")
                self.setup_main_menu()
            else:
                messagebox.showwarning("Warning", "Both usernames must be provided!")

        tk.Button(self.root, text="Start Game", command=start_game, width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu, width=20, height=2).pack(pady=10)
        pass

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
