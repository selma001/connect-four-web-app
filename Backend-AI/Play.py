from ConnectFourBoard import ConnectFourBoard


class Play:
    def __init__(self):
        self.board = ConnectFourBoard()

    def get_game_state(self):
        return {
            "board": self.board.get_current_state(),
            "game_over": self.board.gameOver(),
            "winner": 1 if self.board.win(1) else 2 if self.board.win(2) else None
        }

    def humanTurn(self):
        self.display_board()
        move = int(input("Your turn! Enter your move (column 0-6): "))
        possible_moves = self.board.getPossibleMoves()

        while move not in possible_moves:
            print("Invalid move. Try again.")
            move = int(input("Your turn! Enter your move (column 0-6): "))

        row = max([r for r in range(6) if self.board.board[r][move] == 0])
        self.board.makeMove(row, move, 1)

    def display_board(self):
        self.board.draw_board()

    def computerTurn(self):
        _, best_move = self.minimaxAlphaBetaPruning(self.board, depth=4, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
        row = max([r for r in range(6) if self.board.board[r][best_move] == 0])
        self.board.makeMove(row, best_move, 2)

    def minimaxAlphaBetaPruning(self, connect_four_board, depth, alpha, beta, maximizing_player):
        if depth == 0 or connect_four_board.gameOver():
            return connect_four_board.heuristic_eval(), None

        possible_moves = connect_four_board.getPossibleMoves()

        if maximizing_player:
            
            value = float('-inf')
            best_move = None
            for move in possible_moves:
                row = max([r for r in range(6) if connect_four_board.board[r][move] == 0])
                connect_four_board.makeMove(row, move, 2)

                new_value, _ = self.minimaxAlphaBetaPruning(connect_four_board, depth - 1, alpha, beta, False)

                connect_four_board.board[row][move] = 0  # Undo the move

                if new_value > value:
                    value = new_value
                    best_move = move

                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return value, best_move

        else:

            value = float('inf')
            best_move = None
            for move in possible_moves:
                row = max([r for r in range(6) if connect_four_board.board[r][move] == 0])
                connect_four_board.makeMove(row, move, 1)

                new_value, _ = self.minimaxAlphaBetaPruning(connect_four_board, depth - 1, alpha, beta, True)

                connect_four_board.board[row][move] = 0  # Undo the move

                if new_value < value:
                    value = new_value
                    best_move = move

                beta = min(beta, value)
                if beta <= alpha:
                    break

            return value, best_move

    

