# Quiz Application

This project is a Python-based quiz application that allows users to participate in trivia competitions. It supports single-player and multiplayer modes, lets users manage questions and scores, and provides a leaderboard. The project uses a TOML file for configuration and question data.

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Setup and Installation](#setup-and-installation)
5. [Configuration Files](#configuration-files)
6. [Running the Application](#running-the-application)
7. [Usage](#usage)
8. [Optional Features](#optional-features)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)
11. [License](#license)

## Features

- **Single-Player Mode**: Users can attempt questions and receive feedback.
- **Multiplayer Mode**: Users can challenge each other in a trivia competition.
- **Question Management**: Admins can add and manage quiz questions.
- **Leaderboard**: Displays the top users based on their scores.
- **User Management**: Track user scores and progress.

## Project Structure

```
quiz_application/
├── venv/                  # Virtual environment directory
├── questions.toml         # Configuration file for quiz questions
├── users.toml             # Configuration file for user data (optional)
├── quiz_backend.py        # Backend logic script
├── quiz_gui.py            # GUI script
└── README.md              # Project documentation
```

## Prerequisites

- **Python 3.x**: Make sure Python 3 is installed on your system.
- **pip**: Python's package installer should be available.

## Setup and Installation

Follow these steps to set up and run the quiz application:

### 1. Clone the Repository

If you haven't already cloned the repository, do so using:

```sh
git clone https://github.com/yourusername/quiz_application.git
cd quiz_application
```

### 2. Set Up a Virtual Environment

A virtual environment isolates project dependencies. Create and activate a virtual environment:

- **Windows**:

  ```sh
  python -m venv venv
  venv\Scripts\activate
  ```

- **macOS/Linux**:

  ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the required Python packages:

```sh
pip install toml tkinter
```

### 4. Create Configuration Files

#### `questions.toml`

Create a `questions.toml` file in the `quiz_application` directory with the following sample content:

```toml
[[question]]
category = "Geography"
difficulty = "easy"
text = "What is the capital of France?"
options = ["Paris", "Berlin", "Madrid", "Rome"]
answer = "Paris"
feedback = "Paris is the capital and largest city of France."

[[question]]
category = "Mathematics"
difficulty = "medium"
text = "What is 2 + 2?"
options = ["3", "4", "5", "6"]
answer = "4"
feedback = "2 + 2 equals 4."

[[question]]
category = "Literature"
difficulty = "hard"
text = "Who wrote 'To Kill a Mockingbird'?"
options = ["Harper Lee", "Mark Twain", "J.K. Rowling", "Ernest Hemingway"]
answer = "Harper Lee"
feedback = "'To Kill a Mockingbird' was written by Harper Lee."
```

#### `users.toml` (Optional)

If you have user management features, create a `users.toml` file with initial user data:

```toml
[[user]]
username = "player1"
score = 0

[[user]]
username = "player2"
score = 0
```

## Running the Application

1. **Activate the Virtual Environment**:

   - **Windows**:

     ```sh
     venv\Scripts\activate
     ```

   - **macOS/Linux**:

     ```sh
     source venv/bin/activate
     ```

2. **Run the GUI Application**:

   Execute the following command to start the application:

   ```sh
   python quiz_gui.py
   ```

   This will open the Tkinter-based GUI for the quiz application.

## Usage

1. **Start the Application**: Launch the application using the command mentioned above.
2. **Navigate Through the GUI**:
   - **Start Quiz**: Begin a quiz in single-player mode.
   - **Manage Questions**: Add or edit quiz questions (admin feature).
   - **View Leaderboard**: Check the top users based on scores.
   - **Start Multiplayer**: Challenge another player to a trivia match.

## Optional Features

- **Add New Features**: You can extend the application to include additional features like question categories, timed quizzes, or enhanced user statistics.
- **Customization**: Modify the GUI and backend logic to tailor the quiz experience to your needs.

## Troubleshooting

- **PowerShell Execution Policy Issues**: If you encounter issues with PowerShell execution policies, consider using Command Prompt or Git Bash to activate the virtual environment. For further details, refer to the section on changing PowerShell execution policies.
- **Missing Dependencies**: Ensure all required packages are installed. Run `pip install toml tkinter` to install necessary libraries.
- **File Not Found Errors**: Verify that `questions.toml` and `users.toml` are correctly placed in the project directory.

## Contributing

Feel free to contribute to this project by:
- Reporting issues.
- Submitting pull requests with improvements or bug fixes.
- Suggesting new features.

Please follow standard GitHub contribution guidelines.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

