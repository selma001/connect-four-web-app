from flask import Flask, jsonify, request
from AI import Play, ConnectFourBoard
import time

app = Flask(__name__)
play_instance = Play()
connect_four_board = ConnectFourBoard()

@app.route('/move', methods=['POST'])
def receive_move():
    data = request.get_json()
    column = data.get('column')
    row = data.get('row') 

    success, message = play_instance.process_player_move(column, row)
    print(f"Received move from frontend: Column {column}, Row {row}")
    
    if success:
        
        play_instance.computerTurn()
        game_state = play_instance.get_game_state()

        return jsonify({'message': message, 'success': True, 'game_state': game_state, 'selected from front': {'column': column, 'row': row}})
    else:
        return jsonify({'message': message, 'success': False})


current_player = 1  

@app.route('/pvsp', methods=['POST'])
def player_vs_player():
    global current_player

    data = request.get_json()
    column = data.get('column')
    row = data.get('row')  

    success, message = play_instance.process_player_move(column, row)
    print(f"Received move from frontend: Column {column}, Row {row}")

    if success:
    
        if play_instance.board.gameOver():
            return jsonify({'message': message, 'success': True, 'game_state': play_instance.get_game_state2(), 'game_over': True})

        current_player = 3 - current_player 

        return jsonify({'message': message, 'success': True, 'game_state': play_instance.get_game_state2(), 'current_player': current_player})
    else:
        return jsonify({'message': message, 'success': False})

@app.route('/aivsai', methods=['POST'])
def AI_vs_AI():
    game_states = []  

    while not play_instance.board.gameOver():
        # AI with Alpha-Beta Pruning (Player 1) turn
        _, alphabeta_move = play_instance.minimaxAlphaBetaPruning(play_instance.board, depth=4, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
        row_alphabeta = max([r for r in range(6) if play_instance.board.board[r][alphabeta_move] == 0])
        play_instance.board.makeMove(row_alphabeta, alphabeta_move, 1)

        
        game_states.append({
            'current_player': 1,
            'move': alphabeta_move,
            'board': play_instance.board.get_current_state()
        })

        if play_instance.board.gameOver():
            break

        # AI with BFS (Player 2) turn
        bfs_move = play_instance.board.BFS(player=2)
        row_bfs = max([r for r in range(6) if play_instance.board.board[r][bfs_move] == 0])
        play_instance.board.makeMove(row_bfs, bfs_move, 2)

        
        game_states.append({
            'current_player': 2,
            'move': bfs_move,
            'board': play_instance.board.get_current_state()
        })

    
    final_state = {
        'winner': 1 if play_instance.board.win(1) else 2 if play_instance.board.win(2) else None,
        'board': play_instance.board.get_current_state(),
        'game_over': play_instance.board.gameOver(),
        'moves': game_states
    }

    return jsonify({'success': True, 'message': 'AI vs AI game completed', 'game_state': final_state})

if __name__ == "__main__":
    app.run(debug=True)

