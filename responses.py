import random
from data import (
    jokes,
    riddles,
    trivia_questions,
    movie_recommendations,
    would_you_rather
)
from games import (
    start_number_guessing_game,
    handle_number_guess,
    start_trivia_game,
    handle_trivia_answer,
    start_riddle_game,
    handle_riddle_answer
)
from utils import get_user_session

def get_response(user_input, session_id="default"):
    session = get_user_session(session_id)
    user_input = user_input.lower().strip()
    
    if any(word in user_input for word in ['yes', 'yeah', 'yep', 'sure', 'ok', 'okay', 'more', 'continue', 'next']):
        if session["conversation_context"] == "movie_recommendation" and session["last_genre"]:
            genre = session["last_genre"]
            start_idx = session["game_data"][f"{genre}_count"]
            movies_to_show = movie_recommendations[genre][start_idx:start_idx + 5]
            session["game_data"][f"{genre}_count"] += 5

            if session["game_data"][f"{genre}_count"] >= len(movie_recommendations[genre]):
                session["game_data"][f"{genre}_count"] = 0
                cycle_msg = "\n\n🔄 That's all! Starting from the beginning again."
            else:
                remaining = len(movie_recommendations[genre]) - session["game_data"][f"{genre}_count"]
                cycle_msg = f"\n\n📚 {remaining} more {genre} movies available!"

            response = f"🎬 More {genre.title()} Movies:\n• " + "\n• ".join(movies_to_show)
            response += cycle_msg
            response += f"\n\n🎯 Want even more? Just let me know!\n💫 Try a different genre too!"
            return response

        elif session["conversation_context"] == "game_suggestion":
            session["conversation_context"] = None
            return """🎮 Choose Your Game:

🎯 Number Guessing 
• Guess my number between 1-100
• 7 attempts to win
• +10 points for success

🧠 Trivia Quiz   
• 3 random questions
• Multiple choice format
• +5 points per correct answer

🤔 Brain Riddles
• Challenging puzzles
• Hint system available
• +10 points (or +5 with hint)

Which game sounds fun? 🚀"""

        elif session["conversation_context"] == "joke_request":
            session["conversation_context"] = "joke_request"
            return f"😂 {random.choice(jokes)}\n\n🎭 Enjoyed that? Want another one?"

        elif session["conversation_context"] == "would_you_rather":
            session["conversation_context"] = "would_you_rather"
            return f"🤔 Would You Rather:\n\n{random.choice(would_you_rather)}\n\nTell me your choice! Want another dilemma?"

    if session["current_game"] == "number_guess":
        return handle_number_guess(session, user_input)
    elif session["current_game"] == "trivia":
        return handle_trivia_answer(session, user_input)
    elif session["current_game"] == "riddle":
        return handle_riddle_answer(session, user_input)

    if any(word in user_input for word in ['number game', 'guess number', 'guessing game']):
        session["conversation_context"] = None
        return start_number_guessing_game(session)

    elif any(word in user_input for word in ['trivia', 'quiz', 'questions']):
        session["conversation_context"] = None
        return start_trivia_game(session)

    elif any(word in user_input for word in ['riddle', 'puzzle']):
        session["conversation_context"] = None
        return start_riddle_game(session)

    elif any(word in user_input for word in ['joke', 'funny', 'laugh']):
        session["conversation_context"] = "joke_request"
        return f"😂 {random.choice(jokes)}\n\n🎭 Enjoyed that? Want another one?"

    elif any(word in user_input for word in ['movie', 'film', 'watch']):
        session["conversation_context"] = "movie_recommendation"
        if any(genre in user_input for genre in movie_recommendations.keys()):
            for genre in movie_recommendations:
                if genre in user_input:
                    session["last_genre"] = genre
                    if f"{genre}_count" not in session["game_data"]:
                        session["game_data"][f"{genre}_count"] = 0

                    start_idx = session["game_data"][f"{genre}_count"]
                    movies_to_show = movie_recommendations[genre][start_idx:start_idx + 5]
                    session["game_data"][f"{genre}_count"] += 5

                    if session["game_data"][f"{genre}_count"] >= len(movie_recommendations[genre]):
                        session["game_data"][f"{genre}_count"] = 0
                        cycle_msg = "\n\n🔄 That's all! Starting from the beginning again."
                    else:
                        remaining = len(movie_recommendations[genre]) - session["game_data"][f"{genre}_count"]
                        cycle_msg = f"\n\n📚 {remaining} more {genre} movies available!"

                    response = f"🎬 {genre.title()} Movie Recommendations:\n• " + "\n• ".join(movies_to_show)
                    response += cycle_msg
                    response += f"\n\n💡 Need more suggestions? Just let me know!\n• Say yes for more {genre} movies\n• Try a different genre\n• Ask for random movie!"
                    return response

        return "🎬 Movie Time! What genre are you in the mood for?\n\n🎯 Available Genres:\n• Action • Comedy • Drama • Horror • Sci-Fi • Romance\n\nJust say: action movies, comedy films, or any genre you like!"

    elif any(phrase in user_input for phrase in ['random movie', 'surprise movie', 'any movie']):
        all_genres = list(movie_recommendations.keys())
        random_genre = random.choice(all_genres)
        random_movie = random.choice(movie_recommendations[random_genre])
        session["conversation_context"] = None
        return f"🎲 Random Movie Pick:\n\n🎬 {random_movie} ({random_genre.title()})\n\n🎯 Like {random_genre}? Ask for more or try random again!"

    elif any(phrase in user_input for phrase in ['different genre', 'other genre', 'change genre']):
        session["conversation_context"] = None
        session["last_genre"] = None
        return "🎬 Choose a Different Genre:\n\n🎯 Options:\n• Action 💥 • Comedy 😂 • Drama 🎭 • Horror 👻 • Sci-Fi 🚀 • Romance 💕\n\nSay: action movies or any genre!"

    elif any(phrase in user_input for phrase in ['would you rather', 'rather', 'choice']):
        session["conversation_context"] = "would_you_rather"
        return f"🤔 Would You Rather:\n\n{random.choice(would_you_rather)}\n\nTell me your choice!"

    elif any(word in user_input for word in ['score', 'points']):
        session["conversation_context"] = None
        return f"🏆 Your Score: {session['score']} points\n\nEarn points by:\n• Number Guessing (+10)\n• Trivia (+5 per correct)\n• Riddles (+10, or +5 with hint)"

    elif any(word in user_input for word in ['games', 'play', 'fun']):
        session["conversation_context"] = "game_suggestion"
        return """🎮 Available Games & Entertainment:

🎯 Games:
• Number Guessing → say number game
• Trivia Quiz → say trivia  
• Riddles → say riddle

🎭 Fun:
• Jokes → say joke
• Movies → say action movies or any genre
• Would You Rather → say would you rather

📊 Stats:
• Score → say score

Ready? Just type your choice! 🚀"""

    elif any(word in user_input for word in ['hello', 'hi', 'hey']):
        session["conversation_context"] = None
        return random.choice([
            "🎉 Hey there! Say games to see what we can play!",
            "👋 Hello! Want to play a game or hear a joke?",
            "🎊 Hi! Say joke for a laugh or games to play!"
        ])

    elif any(word in user_input for word in ['bye', 'goodbye']):
        session["conversation_context"] = None
        return f"👋 Goodbye! Thanks for playing! Final score: {session['score']} points."

    elif any(phrase in user_input for phrase in ['help', 'what can you do']):
        session["conversation_context"] = None
        return """🤖 I'm your Entertainment ChatBot!

🎮 I can:
• Play number guessing games
• Ask trivia questions  
• Give you riddles to solve
• Tell jokes
• Recommend movies
• Ask Would You Rather
• Track your score

Just say:
• Tell me a joke
• Let's play trivia
• I want action movies
• Would you rather
• Number game

Ready to begin? 🎉"""

    else:
        session["conversation_context"] = None
        return random.choice([
            "🎭 Interesting! Want to play a game or hear a joke?",
            "🎪 Cool! Try saying games or joke!",
            "🎨 Ready for fun? Try trivia or joke!",
            "🎵 Let's make this fun — try a game or ask for a movie!"
        ])
