from flask import Flask, jsonify, request
from AI import Play, ConnectFourBoard

app = Flask(__name__)
play_instance = Play()


@app.route("/members")
def members():
    return{"members":["Member1","Member2","Member3"]}


@app.route("/start_game", methods=["GET"])
def start_game():
    play_instance.board = ConnectFourBoard()  # Reset the board
    return jsonify(success=True)

@app.route("/make_move", methods=["POST"])
def make_move():
    data = request.get_json()
    column = data.get("column")

    if column is None:
        return jsonify(error="Invalid move"), 400

    play_instance.humanTurn(column)

    if play_instance.board.gameOver():
        return jsonify(game_over=True)

    play_instance.computerTurn()

    if play_instance.board.gameOver():
        return jsonify(game_over=True)

    return jsonify(success=True)

@app.route("/get_game_state", methods=["GET"])
def get_game_state():
    game_state = play_instance.get_game_state()
    return jsonify(game_state)

if __name__ == "__main__":
    app.run(debug=True)
