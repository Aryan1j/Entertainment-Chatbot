from flask import Flask, render_template, request, jsonify
from responses import get_response
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")  

@app.route('/chat', methods=['POST'])
def chat():
    try:
        
        data = request.get_json()
        print("Received:", data)  

        user_message = data.get("message", "")
        session_id = data.get("session_id", "default")

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

       
        bot_response = get_response(user_message, session_id)
        print("Bot response:", bot_response) 

        return jsonify({
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    except Exception as e:
        print("ERROR:", e) 
        return jsonify({'error': 'Server error'}), 500

if __name__ == "__main__":
    print("📱 Open: http://localhost:5000")
    print("Stop: Ctrl+C")
    app.run(debug=True, host="0.0.0.0", port=5000)
