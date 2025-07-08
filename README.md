# 🎉 Entertainment ChatBot 🎮

An interactive chatbot built using **Python + Flask** that delivers quick fun, games, and recommendations through a sleek, web-based interface.

---

## 💡 Features

- 😂 Tells random jokes  
- 🤔 Asks brainy riddles with hints  
- 🧠 Runs trivia quizzes (3 questions per game)  
- 🎬 Recommends movies by genre (action, comedy, etc.)  
- 🎯 Plays number guessing game  
- 🏆 Tracks score per session  
- 🌐 Web interface with chat-like user experience

---

## 🖥️ Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **Session Storage:** Python dictionary (per user/session)  
- **Deployment-ready:** Works on localhost and can be hosted

---

## 📂 Folder Structure

```
entertainment-chatbot/
├── app.py               # Flask server and endpoints
├── responses.py         # Core logic for responding to user input
├── games.py             # Riddle, trivia, and number guessing logic
├── data.py              # Static content: jokes, riddles, trivia, movies
├── utils.py             # Session management
└── templates/
    └── index.html       # Frontend chat UI
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Aryan1j/entertainment-chatbot.git
cd entertainment-chatbot
```

### 2. Install dependencies
```bash
pip install flask
```

### 3. Run the Flask server
```bash
python app.py
```

### 4. Open the app in your browser
```
http://localhost:5000
```

You’ll see a chat interface where you can type:
- `joke`
- `trivia`
- `riddle`
- `action movies`
- `number game`

---

## 🔧 Example Commands

| Command            | What It Does                          |
|--------------------|----------------------------------------|
| `joke`             | Sends you a random joke 😂             |
| `trivia`           | Starts a 3-question quiz 🧠            |
| `riddle`           | Sends a riddle (with hint option) 🤔  |
| `number game`      | Start guessing a number (1–100) 🎯     |
| `romance movies`   | Shows movie suggestions by genre 🎬   |
| `score`            | Displays your total points 🏆          |

---

## 🔮 Future Ideas

- Dark/light mode toggle  
- User login with score history  
- Leaderboard  
- AI-generated jokes and trivia  
- Voice commands integration  

---
