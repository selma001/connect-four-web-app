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

"""connect_four_board = ConnectFourBoard()
shortest_path = connect_four_board.BFS(player=1)
if shortest_path:
    print(f"Shortest path to winning for Player 1: {shortest_path}")
else:
    print("No winning path found.")"""
