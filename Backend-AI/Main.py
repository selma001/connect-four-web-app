from Play import Play
from ConnectFourBoard import ConnectFourBoard
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
