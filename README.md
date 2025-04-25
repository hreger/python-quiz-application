# Python Quiz Application 🎯

[![Python](https://img.shields.io/badge/python-v3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

> A modern, interactive quiz application built with Python that supports both single-player and multiplayer modes, featuring a clean GUI interface and extensive customization options.

![Quiz App Demo](docs/demo.gif)

## ✨ Features

- 🎮 **Single-Player Mode** - Test your knowledge at your own pace
- 👥 **Multiplayer Mode** - Challenge friends in real-time trivia battles
- 📝 **Question Management** - Easy-to-use interface for adding and editing questions
- 🏆 **Leaderboard System** - Track top performers and compete for high scores
- 👤 **User Profiles** - Personal progress tracking and statistics
- 🎨 **Modern GUI** - Clean and intuitive Tkinter-based interface
- 🔧 **Customizable** - Easy configuration using TOML files

## 🚀 Quick Start

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/hreger/python-quiz-application
cd python-quiz-application
```

2. Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
quiz_application/
├── venv/                  # Virtual environment
├── questions.toml         # Quiz questions configuration
├── users.toml            # User data storage
├── quiz_backend.py       # Core logic and functionality
├── quiz_gui.py          # GUI implementation
└── README.md            # Documentation
```

## 🎮 Usage

1. Start the application:
```bash
python quiz_gui.py
```

2. Choose your game mode:
   - 🎯 Single Player: Practice mode with instant feedback
   - 🤝 Multiplayer: Challenge other players
   - ⚙️ Question Management: Add or edit questions (admin only)
   - 📊 Leaderboard: View top scores

## ⚙️ Configuration

### Questions Configuration (questions.toml)

```toml
[[question]]
category = "Geography"
difficulty = "easy"
text = "What is the capital of France?"
options = ["Paris", "Berlin", "Madrid", "Rome"]
answer = "Paris"
feedback = "Paris is the capital and largest city of France."
```

### User Data (users.toml)

```toml
[[user]]
username = "player1"
score = 0
```

## 📸 App Screenshots

### Home View
<img src="Screenshots/py_app_lightmode.png" width="500"/>
<img src="Screenshots/py_app_darkmode.png" width="500"/>

---


## 🛠️ Development

Want to contribute? Great! Please check our [contribution guidelines](CONTRIBUTING.md).

### Setting Up Development Environment

1. Fork the repository
2. Create a feature branch
3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

- **PowerShell Execution Policy**: If you encounter execution policy issues on Windows:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- **Missing Dependencies**: Ensure all requirements are installed:
  ```bash
  pip install -r requirements.txt
  ```
- **File Not Found Errors**: Verify configuration files exist in the correct locations

## 📫 Contact

LinkedIn Link - [P Sanjeev Pradeep](https://www.linkedin.com/in/p-sanjeev-pradeep)

Project Link: [https://github.com/hreger/python-quiz-application](https://github.com/hreger/python-quiz-application)

## 🙏 Acknowledgments

- [Python](https://www.python.org/) - Programming language
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI library
- [TOML](https://toml.io/) - Configuration file format

---

<p align="center">Made with ❤️ by [P Sanjeev Pradeep]</p>

