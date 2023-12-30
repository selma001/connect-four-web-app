from flask import Flask, jsonify, request
from AI import Play

app = Flask(__name__)
play_instance = Play()

@app.route('/move', methods=['POST'])
def receive_move():
    data = request.get_json()
    column = data.get('column')
    row = data.get('row')  # Retrieve row from the request

    # Process player move
    success, message = play_instance.process_player_move(column, row)
    print(f"Received move from frontend: Column {column}, Row {row}")
    
    if success:
        # Process AI move
        play_instance.computerTurn()
        
        # Get the updated game state
        game_state = play_instance.get_game_state()

        return jsonify({'message': message, 'success': True, 'game_state': game_state, 'selected from front': {'column': column, 'row': row}})
    else:
        return jsonify({'message': message, 'success': False})


if __name__ == "__main__":
    app.run(debug=True)
