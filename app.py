from flask import Flask, render_template, request, jsonify
from responses import get_response
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")  # Make sure index.html is in templates/

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Parse the JSON sent by frontend
        data = request.get_json()
        print("Received:", data)  # Debug log

        user_message = data.get("message", "")
        session_id = data.get("session_id", "default")

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Generate bot response using modular logic
        bot_response = get_response(user_message, session_id)
        print("Bot response:", bot_response)  # Debug log

        return jsonify({
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    except Exception as e:
        print("ERROR:", e)  # Critical for debugging
        return jsonify({'error': 'Server error'}), 500

if __name__ == "__main__":
    print("🎮 Entertainment ChatBot is starting...")
    print("🎯 Games: Number Guessing, Trivia, Riddles")
    print("🎭 Fun: Jokes, Movies, Would You Rather")
    print("📱 Open: http://localhost:5000")
    print("🛑 Stop: Ctrl+C")
    app.run(debug=True, host="0.0.0.0", port=5000)
