from flask import Flask, jsonify, request
from AI import Play
import traceback  # Import traceback module for error debugging

app = Flask(__name__)
play_instance = Play()

@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route('/move', methods=['POST'])
def receive_move():
    data = request.get_json()
    column = data.get('column')  # Assuming the frontend sends the column index

    success, message = play_instance.process_player_move(column)

    if success:
        game_state = play_instance.get_game_state()
        return jsonify({'message': message, 'success': True, 'game_state': game_state})
    else:
        return jsonify({'message': message, 'success': False})

@app.route('/ai-move', methods=['GET'])
def get_ai_move():
    try:
        column, row = play_instance.computerTurn()  # Assuming computerTurn returns the AI move's column and row
        game_state = play_instance.get_game_state()
        return jsonify({'success': True, 'move': {'column': column, 'row': row}, 'game_state': game_state})
    except Exception as e:
        traceback.print_exc()  # Print the traceback to the console for debugging
        print(f"Error getting AI move: {str(e)}")
        return jsonify({'success': False, 'message': 'Internal Server Error'})

if __name__ == "__main__":
    app.run(debug=True)


