from flask import Flask, render_template, request, jsonify
import random
import json
from datetime import datetime

app = Flask(__name__)

# Entertainment data
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
    "Why don't eggs tell jokes? They'd crack each other up!",
    "What do you call a fake noodle? An impasta!",
    "Why did the math book look so sad? Because it had too many problems!",
    "What do you call a bear with no teeth? A gummy bear!",
    "Why don't skeletons fight each other? They don't have the guts!",
    "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
    "Why did the coffee file a police report? It got mugged!",
    "What do you call a sleeping bull? A bulldozer!"
]

riddles = [
    {
        "question": "I have keys but no locks. I have space but no room. You can enter, but you can't go outside. What am I?",
        "answer": "keyboard",
        "hint": "You're probably using one right now to type!"
    },
    {
        "question": "The more you take, the more you leave behind. What am I?",
        "answer": "footsteps",
        "hint": "Think about walking..."
    },
    {
        "question": "I'm tall when I'm young, and short when I'm old. What am I?",
        "answer": "candle",
        "hint": "I provide light and melt away..."
    },
    {
        "question": "What has hands but can't clap?",
        "answer": "clock",
        "hint": "It tells you something important every second..."
    },
    {
        "question": "What gets wet while drying?",
        "answer": "towel",
        "hint": "You use it after a shower..."
    }
]

trivia_questions = [
    {
        "question": "What is the largest planet in our solar system?",
        "options": ["A) Earth", "B) Jupiter", "C) Saturn", "D) Mars"],
        "answer": "B",
        "explanation": "Jupiter is the largest planet, more than twice as massive as all other planets combined!"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["A) Van Gogh", "B) Picasso", "C) Leonardo da Vinci", "D) Michelangelo"],
        "answer": "C",
        "explanation": "Leonardo da Vinci painted the Mona Lisa between 1503-1519!"
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["A) Go", "B) Au", "C) Ag", "D) Gd"],
        "answer": "B",
        "explanation": "Au comes from the Latin word 'aurum' meaning gold!"
    },
    {
        "question": "Which country has the most time zones?",
        "options": ["A) Russia", "B) USA", "C) China", "D) France"],
        "answer": "D",
        "explanation": "France has 12 time zones due to its overseas territories!"
    }
]

movie_recommendations = {
    "action": [
        "John Wick", "Mad Max: Fury Road", "The Dark Knight", "Avengers: Endgame", "Mission Impossible",
        "Die Hard", "Terminator 2", "The Matrix", "Gladiator", "Heat", "Casino Royale", "Speed",
        "Face/Off", "The Rock", "Con Air", "Lethal Weapon", "Rush Hour", "Bad Boys", "Top Gun",
        "Raiders of the Lost Ark", "Aliens", "Predator", "Rambo", "Rocky", "The Bourne Identity",
        "Fast & Furious", "300", "Kill Bill", "Sin City", "Taken", "The Expendables", "Commando",
        "Point Break", "True Lies", "Demolition Man", "Total Recall", "RoboCop", "First Blood",
        "Bloodsport", "Enter the Dragon", "Police Story", "Hard Boiled", "The Raid", "Dredd",
        "Mad Max", "Road House", "Under Siege", "Cliffhanger", "Eraser", "The Long Kiss Goodnight"
    ],
    "comedy": [
        "The Grand Budapest Hotel", "Superbad", "Anchorman", "The Hangover", "Borat",
        "Dumb and Dumber", "There's Something About Mary", "Meet the Parents", "Zoolander", "Dodgeball",
        "Wedding Crashers", "Old School", "Step Brothers", "Talladega Nights", "The Other Guys",
        "Tropic Thunder", "Pineapple Express", "This Is the End", "Knocked Up", "The 40-Year-Old Virgin",
        "Ghostbusters", "Coming to America", "Beverly Hills Cop", "Trading Places", "The Mask",
        "Ace Ventura", "Liar Liar", "Bruce Almighty", "Yes Man", "The Cable Guy", "Dumb and Dumber To",
        "Napoleon Dynamite", "Office Space", "Super Troopers", "Anchorman 2", "Scary Movie",
        "American Pie", "Road Trip", "EuroTrip", "Van Wilder", "Jackass", "Borat 2", "The Interview",
        "Pineapple Express", "Neighbors", "22 Jump Street", "Game Night", "Tag", "Blockers"
    ],
    "drama": [
        "The Shawshank Redemption", "Forrest Gump", "The Godfather", "Schindler's List", "12 Years a Slave",
        "One Flew Over the Cuckoo's Nest", "To Kill a Mockingbird", "The Green Mile", "Good Will Hunting",
        "Dead Poets Society", "A Beautiful Mind", "Rain Man", "Philadelphia", "The Pursuit of Happyness",
        "Million Dollar Baby", "Mystic River", "There Will Be Blood", "No Country for Old Men",
        "The Departed", "Goodfellas", "Casino", "Scarface", "The Pianist", "Life is Beautiful",
        "Amadeus", "Gandhi", "Braveheart", "Titanic", "The English Patient", "Saving Private Ryan",
        "Platoon", "Born on the Fourth of July", "JFK", "Nixon", "All the President's Men",
        "The Social Network", "Moneyball", "The Big Short", "Spotlight", "Manchester by the Sea",
        "Moonlight", "La La Land", "Three Billboards Outside Ebbing Missouri", "Green Book", "Parasite",
        "Nomadland", "Minari", "The Father", "Sound of Metal", "Judas and the Black Messiah"
    ],
    "horror": [
        "Get Out", "A Quiet Place", "Hereditary", "The Conjuring", "It Follows",
        "The Exorcist", "Halloween", "A Nightmare on Elm Street", "Friday the 13th", "Scream",
        "The Shining", "Psycho", "Jaws", "Alien", "The Thing", "Poltergeist", "The Omen",
        "Rosemary's Baby", "The Texas Chain Saw Massacre", "Night of the Living Dead", "Dawn of the Dead",
        "28 Days Later", "The Ring", "The Grudge", "Saw", "Hostel", "The Hills Have Eyes",
        "Wrong Turn", "Final Destination", "I Know What You Did Last Summer", "Urban Legend",
        "The Blair Witch Project", "Paranormal Activity", "Insidious", "Sinister", "The Babadook",
        "It", "Us", "Midsommar", "The Witch", "The Lighthouse", "Saint Maud", "His House",
        "Relic", "The Invisible Man", "Candyman", "Malignant", "Last Night in Soho", "X", "Barbarian"
    ],
    "sci-fi": [
        "Blade Runner 2049", "Interstellar", "The Matrix", "Inception", "Ex Machina",
        "2001: A Space Odyssey", "Star Wars", "Empire Strikes Back", "Return of the Jedi", "Alien",
        "Aliens", "Terminator", "Terminator 2", "Back to the Future", "E.T.", "Close Encounters",
        "Blade Runner", "The Fifth Element", "Total Recall", "Minority Report", "I, Robot",
        "War of the Worlds", "Independence Day", "Men in Black", "The Day the Earth Stood Still",
        "Forbidden Planet", "Planet of the Apes", "Logan's Run", "Soylent Green", "THX 1138",
        "Gattaca", "The Truman Show", "Dark City", "Strange Days", "eXistenZ", "The Thirteenth Floor",
        "Equilibrium", "Serenity", "District 9", "Elysium", "Chappie", "Arrival", "Annihilation",
        "Gravity", "The Martian", "Ad Astra", "First Man", "Tenet", "Dune", "Everything Everywhere All at Once"
    ],
    "romance": [
        "The Notebook", "Casablanca", "Titanic", "La La Land", "Before Sunrise",
        "When Harry Met Sally", "Sleepless in Seattle", "You've Got Mail", "Pretty Woman", "Ghost",
        "Dirty Dancing", "The Princess Bride", "Say Anything", "Jerry Maguire", "As Good as It Gets",
        "Notting Hill", "Four Weddings and a Funeral", "Love Actually", "Bridget Jones's Diary",
        "The Holiday", "50 First Dates", "Hitch", "The Proposal", "Crazy, Stupid, Love",
        "500 Days of Summer", "Eternal Sunshine of the Spotless Mind", "Her", "Lost in Translation",
        "Before Sunset", "Before Midnight", "Blue Valentine", "The Vow", "Dear John", "The Lucky One",
        "Safe Haven", "The Best of Me", "Me Before You", "The Fault in Our Stars", "If I Stay",
        "A Walk to Remember", "The Time Traveler's Wife", "About Time", "Midnight in Paris",
        "Silver Linings Playbook", "The Shape of Water", "Call Me by Your Name", "Lady Bird", "Brooklyn"
    ]
}

would_you_rather = [
    "Would you rather have the ability to fly or be invisible?",
    "Would you rather always be 10 minutes late or 20 minutes early?",
    "Would you rather have unlimited money or unlimited time?",
    "Would you rather be able to read minds or predict the future?",
    "Would you rather live in the past or the future?",
    "Would you rather have super strength or super speed?",
    "Would you rather never be able to use the internet again or never be able to watch TV/movies again?",
    "Would you rather be famous or be the best friend of someone famous?",
    "Would you rather have the power to heal others or the power to bring back the dead?",
    "Would you rather live forever or die tomorrow?"
]