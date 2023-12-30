from collections import deque

class ConnectFourBoard :
    def __init__(self, board = None):
        self.board = board if board else [[0] * 7 for _ in range(6)]

    def get_current_state(self):
        return self.board

    def draw_board(self):
        #affichage de la matrice
        for row in self.board:
            print(" ".join(map(str, row)))
        print("")

    def getPossibleMoves(self):
        #mouvement possible
        moves = []
        for col in range(7):
            if self.board[0][col] == 0:
                moves.append(col)
        return moves

    def makeMove(self,row,column,piece):
        #placer la piece 
        self.board[row][column] = piece
        pass

    def win(self,piece):

        #horizontalement
        for row in range(6):
            for col in range(4):
                if all(self.board[row][col + i] == piece for i in range(4)):
                    return True
        #verticalement
        for row in range(3):
            for col in range(7):
                if all(self.board[row + i][col] == piece for i in range(4)):
                    return True
        # diagonale (bottom-left to top-right)
        for row in range(3, 6):
            for col in range(4):
                if all(self.board[row - i][col + i] == piece for i in range(4)):
                    return True
        # diagonale (top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                if all(self.board[row + i][col + i] == piece for i in range(4)):
                    return True
                
        return False


    def gameOver(self):
        return self.win(1) or self.win(2) or not any(0 in row for row in self.board)


    def heuristic_eval(self):
        score = 0
        for player in [1, 2]:
            for row in range(6):
                for col in range(4):
                    line = [self.board[row][col + i] for i in range(4)]
                    score += self.evaluate_line(line, player)

            for col in range(7):
                for row in range(3):
                    line = [self.board[row + i][col] for i in range(4)]
                    score += self.evaluate_line(line, player)

            for row in range(3, 6):
                for col in range(4):
                    line = [self.board[row - i][col + i] for i in range(4)]
                    score += self.evaluate_line(line, player)

            for row in range(3):
                for col in range(4):
                    line = [self.board[row + i][col + i] for i in range(4)]
                    score += self.evaluate_line(line, player)

        return score

    def evaluate_line(self, line, player):
        enemy = 3 - player  
        count_player = line.count(player)
        count_enemy = line.count(enemy)

        if count_player == 4:
            return 1000  # Winning move
        elif count_enemy == 4:
            return -1000  # Block opponent's winning move
        elif count_player == 3 and line.count(0) == 1:
            return 100  # Create a potential winning move
        elif count_enemy == 3 and line.count(0) == 1:
            return -200  # Block opponent's potential winning move 
        elif count_player == 2 and line.count(0) == 2:
            return 10  # Create a potential double move
        elif count_enemy == 2 and line.count(0) == 2:
            return -20  # Block opponent's potential double move 
        else:
            return 0  

    def winBFS(self, player, state=None):
        # Check if the given player has won in the specified state or the current state
        if state is None:
            state = self.board
        for row in range(6):
            for col in range(4):
                if all(state[row][col + i] == player for i in range(4)):
                    return True
        for row in range(3):
            for col in range(7):
                if all(state[row + i][col] == player for i in range(4)):
                    return True
        for row in range(3, 6):
            for col in range(4):
                if all(state[row - i][col + i] == player for i in range(4)):
                    return True
        for row in range(3):
            for col in range(4):
                if all(state[row + i][col + i] == player for i in range(4)):
                    return True

        return False

    def BFS(self, player):
        queue = deque()
        queue.append((self.board, []))

        while queue:
            current_state, path = queue.popleft()
            # Check if the current state is a winning state for the player
            if self.winBFS(player, state=current_state):
                # Return the first move from the path
                return path[0] if path else None
            # Enqueue possible next moves
            for col in range(7):
                if current_state[0][col] == 0:
                    new_state = [row[:] for row in current_state]
                    row = max([r for r in range(6) if new_state[r][col] == 0])
                    new_state[row][col] = player
                    queue.append((new_state, path + [col]))

        return None
    


class Play:
    def __init__(self):
        self.board = ConnectFourBoard()

    def get_game_state(self):
        ai_move = self.computerTurn()
        return {
            "board": self.board.get_current_state(),
            "game_over": self.board.gameOver(),
            "winner": 1 if self.board.win(1) else 2 if self.board.win(2) else None,
            "ai_move": ai_move
        }

    def process_player_move(self, column, row):
        # Check if the game is already over
        if self.board.gameOver():
            return False, "The game is already over."

        # Check if the selected column is valid
        possible_moves = self.board.getPossibleMoves()
        if column not in possible_moves:
            return False, "Invalid move. The selected column is full."

        # Find the row to place the player's piece in the selected column
        # row = max([r for r in range(6) if self.board.board[r][column] == 0])

        # Make the move
        self.board.makeMove(row, column, 1)

        # Check if the player wins after the move
        if self.board.win(1):
            return True, "You win! Congratulations!"
        
        # Check if the game is a draw
        if self.board.gameOver():
            return True, "The game is a draw."

        # If the game is still ongoing, return success
        return True, "Move processed successfully"
    
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

        # Adjust the AI move to use 0-based indexing before returning
        ai_move = (best_move, row)
        self.board.makeMove(row, best_move, 2)

        return ai_move

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
        

import time

connect_four_board = ConnectFourBoard()

def display_board():
    connect_four_board.draw_board()
def get_valid_input():
    while True:
        try:
            return int(input("Enter a valid column number: "))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def PlayerVsPlayer():
    current_player = 1
    while not connect_four_board.gameOver():
        display_board()
        possible_moves = connect_four_board.getPossibleMoves()
        print(f"Possible moves for Player {current_player}: {possible_moves}")
        column = get_valid_input()
        
        if column not in possible_moves:
            print("Invalid move. Try again.")
            continue

        row = max([r for r in range(6) if connect_four_board.board[r][column] == 0])
        connect_four_board.makeMove(row, column, current_player)

        if connect_four_board.win(current_player):
            display_board()
            print(f"Player {current_player} wins!")
            break

        current_player = 3 - current_player  # Switch between player 1 and 2 
    display_board()
    if not connect_four_board.win(1) and not connect_four_board.win(2):
        print("It's a draw!")

def AiVsPlayer():
        play = Play()
        while not play.board.gameOver():

            play.humanTurn()
            if  play.board.gameOver():
                break

            play.display_board()
            play.computerTurn()

        play.display_board()

        if play.board.win(1):
            print("Congratulations! You win!")
        elif play.board.win(2):
            print("AI wins! Better luck next time.")
        else:
            print("It's a draw!")



def AI_vs_AI_BFS_vs_AlphaBetaPruning():
    connect_four_board = ConnectFourBoard()
    play_instance = Play()  # Create an instance of the Play class

    while not connect_four_board.gameOver():
        # AI with BFS (Player 1) turn
        bfs_move = connect_four_board.BFS(player=1)
        row_bfs = max([r for r in range(6) if connect_four_board.board[r][bfs_move] == 0])
        connect_four_board.makeMove(row_bfs, bfs_move, 1)

        print("BFS :")
        connect_four_board.draw_board()
        time.sleep(1) 

        if connect_four_board.gameOver():
            break

        # AI with Alpha-Beta Pruning (Player 2) turn
        _, alphabeta_move = play_instance.minimaxAlphaBetaPruning(connect_four_board, depth=4, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
        row_alphabeta = max([r for r in range(6) if connect_four_board.board[r][alphabeta_move] == 0])
        connect_four_board.makeMove(row_alphabeta, alphabeta_move, 2)
        
        print("MiniMax Alpha Beta Prunning :")
        connect_four_board.draw_board()
        time.sleep(1)  

    connect_four_board.draw_board()

    if connect_four_board.win(1):
        print("AI with BFS wins!")
    elif connect_four_board.win(2):
        print("AI with Alpha-Beta Pruning wins!")
    else:
        print("It's a draw!")



def main():
    print("Welcome to Connect Four!")

    while True:
        print("Choose an option:")
        print("1. Player vs Player")
        print("2. Player vs AI")
        print("3. AI vs AI")
        print("4. QUIT")

        choice = input("Enter the number of your choice: ")

        if choice == "1":
            PlayerVsPlayer()
        elif choice == "2":
            AiVsPlayer()
        if choice == "3":
            AI_vs_AI_BFS_vs_AlphaBetaPruning()
        elif choice =="4":
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid number.")

if __name__ == "__main__":
    main()
