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


current_player = 1  # Initialize the current player

@app.route('/pvsp', methods=['POST'])
def player_vs_player():
    global current_player

    data = request.get_json()
    column = data.get('column')
    row = data.get('row')  # Retrieve row from the request

    # Process player move
    success, message = play_instance.process_player_move(column, row)
    print(f"Received move from frontend: Column {column}, Row {row}")

    if success:
        # Check for game over or switch to the next player
        if play_instance.board.gameOver():
            return jsonify({'message': message, 'success': True, 'game_state': play_instance.get_game_state2(), 'game_over': True})

        # Switch to the next player
        current_player = 3 - current_player  # Toggle between 1 and 2

        return jsonify({'message': message, 'success': True, 'game_state': play_instance.get_game_state2(), 'current_player': current_player})
    else:
        return jsonify({'message': message, 'success': False})


if __name__ == "__main__":
    app.run(debug=True)
