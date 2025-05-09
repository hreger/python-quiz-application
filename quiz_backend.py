import toml
import random

def load_questions(filename):
    with open(filename, 'r') as file:
        data = toml.load(file)
    return data['question']

def save_questions(filename, questions):
    with open(filename, 'w') as file:
        toml.dump({'question': questions}, file)

def load_users(filename):
    with open(filename, 'r') as file:
        data = toml.load(file)
    return data['user']

def save_users(filename, users):
    with open(filename, 'w') as file:
        toml.dump({'user': users}, file)

def filter_questions(questions, category=None, difficulty=None):
    filtered = []
    for question in questions:
        if (category is None or question['category'] == category) and \
           (difficulty is None or question['difficulty'] == difficulty):
            filtered.append(question)
    return filtered

def ask_question(question, choice):
    return question['options'][choice - 1] == question['answer']

def add_question(questions, category, difficulty, text, options, answer, feedback):
    questions.append({
        'category': category,
        'difficulty': difficulty,
        'text': text,
        'options': options,
        'answer': answer,
        'feedback': feedback
    })
    return questions


def delete_question(questions, index):
    if 0 <= index < len(questions):
        questions.pop(index)
    return questions

def get_leaderboard(users):
    return sorted(users, key=lambda x: x['score'], reverse=True)

def find_user(users, username):
    for user in users:
        if user['username'] == username:
            return user
    return None

def delete_user(users, username):
    users = [user for user in users if user['username'] != username]
    return users

def update_user_best_score(users, username, score):
    user = find_user(users, username)
    if user:
        if score > user['score']:
            user['score'] = score
    return users

def get_user_best_score(users, username):
    user = find_user(users, username)
    return user['score'] if user else 0

def start_multiplayer_game(users, user1, user2):
    game_id = f"{user1}_{user2}_{random.randint(1000, 9999)}"
    for user in users:
        if user['username'] in [user1, user2]:
            user['current_game'] = game_id
    return users, game_id

def get_current_game(users, username):
    user = find_user(users, username)
    return user['current_game'] if user else None
