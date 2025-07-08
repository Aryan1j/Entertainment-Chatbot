import random
from data import trivia_questions, riddles

def start_number_guessing_game(session):
    session["current_game"] = "number_guess"
    session["game_data"] = {
        "number": random.randint(1, 100),
        "attempts": 0,
        "max_attempts": 7
    }
    return "🎯 Number Guessing Game Started!\nI'm thinking of a number between 1 and 100.\nYou have 7 attempts to guess it!\nWhat's your first guess?"

def handle_number_guess(session, guess):
    try:
        guess = int(guess)
        game_data = session.get("game_data", {})
        target = game_data.get("number")
        game_data["attempts"] = game_data.get("attempts", 0) + 1
        attempts_left = game_data.get("max_attempts", 7) - game_data["attempts"]

        if target is None:
            return "⚠️ No number to guess. Say 'number game' to start over."

        if guess == target:
            session["current_game"] = None
            session["score"] += 10
            return f"🎉 CORRECT! The number was {target}!\nYou got it in {game_data['attempts']} attempts!\n+10 points! Your score: {session['score']}"
        elif game_data["attempts"] >= game_data.get("max_attempts", 7):
            session["current_game"] = None
            return f"💥 Game Over! The number was {target}.\nBetter luck next time!"
        elif guess < target:
            return f"📈 Too low! You have {attempts_left} attempts left.\nTry a higher number!"
        else:
            return f"📉 Too high! You have {attempts_left} attempts left.\nTry a lower number!"
    except ValueError:
        return "❌ Please enter a valid number!"

def start_trivia_game(session):
    question = random.choice(trivia_questions)
    session["current_game"] = "trivia"
    session["game_data"] = {
        "current_question": question,
        "questions_answered": 0,
        "correct_answers": 0
    }
    return f"🧠 Trivia Time!\n\nQuestion: {question['question']}\n" + "\n".join(question['options']) + "\n\nType A, B, C, or D!"

def handle_trivia_answer(session, answer):
    game_data = session.get("game_data", {})
    question = game_data.get("current_question")

    if not question:
        session["current_game"] = None
        return "⚠️ Trivia game not active. Type 'trivia' to start again."

    answer = answer.upper().strip()
    if answer not in ['A', 'B', 'C', 'D']:
        return "❌ Please answer with A, B, C, or D!"

    game_data["questions_answered"] += 1

    if answer == question["answer"]:
        game_data["correct_answers"] += 1
        session["score"] += 5
        response = f"✅ Correct! {question['explanation']}\n+5 points!"
    else:
        response = f"❌ Wrong! The correct answer was {question['answer']}.\n{question['explanation']}"

    if game_data["questions_answered"] < 3:
        next_question = random.choice(trivia_questions)
        game_data["current_question"] = next_question
        response += f"\n\nNext Question ({game_data['questions_answered'] + 1}/3):\n{next_question['question']}\n" + "\n".join(next_question['options'])
    else:
        session["current_game"] = None
        score_msg = f"\n\n🏆 Trivia Complete!\nYou got {game_data['correct_answers']}/3 correct!\nTotal Score: {session['score']}"
        response += score_msg

    return response

def start_riddle_game(session):
    riddle = random.choice(riddles)
    session["current_game"] = "riddle"
    session["game_data"] = {
        "current_riddle": riddle,
        "attempts": 0,
        "hint_used": False
    }
    return f"🤔 Riddle Time!\n\n{riddle['question']}\n\nWhat am I? (Type 'hint' if you need help)"

def handle_riddle_answer(session, answer):
    game_data = session.get("game_data", {})
    riddle = game_data.get("current_riddle")

    if not riddle:
        session["current_game"] = None
        return "⚠️ Riddle game not active. Type 'riddle' to start again."

    if answer.lower() == "hint":
        if not game_data.get("hint_used", False):
            game_data["hint_used"] = True
            return f"💡 Hint: {riddle['hint']}\n\nNow, what am I?"
        else:
            return "⚠️ You already used your hint! Try to guess the answer."

    game_data["attempts"] = game_data.get("attempts", 0) + 1

    if answer.lower() == riddle["answer"].lower():
        session["current_game"] = None
        points = 10 if not game_data.get("hint_used", False) else 5
        session["score"] += points
        return f"🎉 Correct! The answer is {riddle['answer']}!\n+{points} points! Your score: {session['score']}"
    elif game_data["attempts"] >= 3:
        session["current_game"] = None
        return f"💭 The answer was: {riddle['answer']}\nBetter luck next time!"
    else:
        attempts_left = 3 - game_data["attempts"]
        return f"❌ Not quite right! You have {attempts_left} attempts left.\nTry again or type 'hint' for help!"
