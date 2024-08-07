import tkinter as tk
from tkinter import simpledialog, messagebox
import quiz_backend as backend
import random

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application") 

        self.questions = backend.load_questions('questions.toml')
        self.users = backend.load_users('users.toml')
        self.current_user = None
        self.current_question = None
        self.score = 0

        self.setup_main_menu()

    def setup_main_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="Welcome to the Quiz App", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.root, text="Start Quiz", command=self.start_quiz).pack(pady=10)
        tk.Button(self.root, text="Manage Users", command=self.manage_users).pack(pady=10)
        tk.Button(self.root, text="Manage Questions", command=self.manage_questions).pack(pady=10)
        tk.Button(self.root, text="Leaderboard", command=self.show_leaderboard).pack(pady=10)
        tk.Button(self.root, text="Multiplayer Mode", command=self.start_multiplayer).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def start_quiz(self):
        self.clear_frame()
        self.current_user = simpledialog.askstring("User", "Enter your username:")
        if self.current_user is None or self.current_user.strip() == "":
            messagebox.showwarning("Warning", "Username cannot be empty!")
            self.setup_main_menu()
            return

        if not any(user['username'] == self.current_user for user in self.users):
            self.users.append({"username": self.current_user, "score": 0, "current_game": ""})
            backend.save_users('users.toml', self.users)

        self.ask_next_question()

    def ask_next_question(self):
        self.clear_frame()
        question = random.choice(self.questions)
        self.current_question = question

        tk.Label(self.root, text=question['text'], font=("Arial", 14)).pack(pady=10)
        self.option_vars = []
        for i, option in enumerate(question['options'], 1):
            var = tk.IntVar()
            tk.Radiobutton(self.root, text=option, variable=var, value=i).pack(anchor=tk.W)
            self.option_vars.append(var)

        tk.Button(self.root, text="Submit Answer", command=self.submit_answer).pack(pady=10)

    def submit_answer(self):
        choice = next((var.get() for var in self.option_vars if var.get() > 0), None)
        if choice is None:
            messagebox.showwarning("Warning", "Please select an option!")
            return

        if backend.ask_question(self.current_question, choice):
            self.score += 1
            messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            messagebox.showinfo("Wrong!", f"The correct answer was: {self.current_question['answer']}")

        self.ask_next_question()

    def manage_users(self):
        self.clear_frame()
        tk.Label(self.root, text="Manage Users", font=("Arial", 16)).pack(pady=20)

        for user in self.users:
            tk.Label(self.root, text=f"User: {user['username']}, Score: {user['score']}").pack()

        tk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu).pack(pady=10)

    def manage_questions(self):
        self.clear_frame()
        tk.Label(self.root, text="Manage Questions", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.root, text="Category:").pack(pady=5)
        category_entry = tk.Entry(self.root)
        category_entry.pack(pady=5)

        tk.Label(self.root, text="Difficulty:").pack(pady=5)
        difficulty_entry = tk.Entry(self.root)
        difficulty_entry.pack(pady=5)

        tk.Label(self.root, text="Question:").pack(pady=5)
        question_entry = tk.Entry(self.root)
        question_entry.pack(pady=5)

        tk.Label(self.root, text="Options (comma-separated):").pack(pady=5)
        options_entry = tk.Entry(self.root)
        options_entry.pack(pady=5)

        tk.Label(self.root, text="Answer:").pack(pady=5)
        answer_entry = tk.Entry(self.root)
        answer_entry.pack(pady=5)

        tk.Label(self.root, text="Feedback:").pack(pady=5)
        feedback_entry = tk.Entry(self.root)
        feedback_entry.pack(pady=5)

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
                self.setup_main_menu()
            else:
                messagebox.showwarning("Warning", "All fields must be filled!")

        tk.Button(self.root, text="Add Question", command=add_question).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu).pack(pady=10)

    def show_leaderboard(self):
        self.clear_frame()
        tk.Label(self.root, text="Leaderboard", font=("Arial", 16)).pack(pady=20)

        leaderboard = backend.get_leaderboard(self.users)
        for user in leaderboard:
            tk.Label(self.root, text=f"User: {user['username']}, Score: {user['score']}").pack()

        tk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu).pack(pady=10)

    def start_multiplayer(self):
        self.clear_frame()
        tk.Label(self.root, text="Multiplayer Mode", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.root, text="Player 1 Username:").pack(pady=5)
        player1_entry = tk.Entry(self.root)
        player1_entry.pack(pady=5)

        tk.Label(self.root, text="Player 2 Username:").pack(pady=5)
        player2_entry = tk.Entry(self.root)
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

        tk.Button(self.root, text="Start Game", command=start_game).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu).pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
