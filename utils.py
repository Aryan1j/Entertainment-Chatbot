user_sessions = {}

def get_user_session(session_id="default"):
    if session_id not in user_sessions:
        user_sessions[session_id] = {
            "current_game": None,
            "last_action": None,
            "last_genre": None,
            "conversation_context": None,
            "game_data": {
                "action_count": 0,
                "comedy_count": 0,
                "drama_count": 0,
                "horror_count": 0,
                "sci-fi_count": 0,
                "romance_count": 0
            },
            "score": 0,
            "name": None
        }
    return user_sessions[session_id]