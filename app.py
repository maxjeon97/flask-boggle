from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start new game and return JSON about game.

    Returns: JSON of {
       gameId: "...uuid-of-game...",
       board: [ [ 'A', 'B', ... ], ... ]
    }
    """

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    game_info = {
        "gameId": game_id,
        "board": game.board
    }

    return jsonify(game_info)


@app.post("/api/score-word")
def score_word():
    """Receives request containing a gameID and a word, checks if the word is in
    the word list and findable on the board, then returns JSON about the result

    Receives: JSON of {
        gameId: "...uuid-of-game...",
        word: "...random-word..."
    }

    Returns: JSON of {
        result: "...word_status..."
    }
    """
    game_data = request.json

    game_id = game_data["gameId"]
    word = game_data["word"]
    game = games[game_id]

    word_status = ""

    if not game.is_word_in_word_list(word):
        word_status = "not-word"

    elif not game.check_word_on_board(word):
        word_status = "not-on-board"

    else:
        word_status = "ok"

    return jsonify({"result": f"{word_status}"})
