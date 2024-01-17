import React, { useState} from 'react';
import smile from '../../assets/smile.svg';
import Win from './win3';
import './aivsai.css';

const AIvsAI = () => {
  const [board, setBoard] = useState(Array.from({ length: 7 }, () => Array(6).fill('')));
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(null);
  const [alphaBetaMove, setAlphaBetaMove] = useState(null);
  const [bfsMove, setBfsMove] = useState(null);
  const [currentMove, setCurrentMove] = useState(null);

  const startGame = async () => {
    try {
      const response = await fetch('/aivsai', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        const { game_state, success } = data;

        if (success) {
          console.log('Current Board State:', game_state.board);

          // Update the React state
          setBoard(game_state.board);
          setAlphaBetaMove(game_state.ai_moves?.alphabeta);
          setBfsMove(game_state.ai_moves?.bfs);
          setGameOver(game_state.game_over);
          setWinner(game_state.winner);

          console.log('Updated Board State:', game_state.board);

          // Log the moves with delay
          const logMovesWithDelay = async () => {
            for (let index = 0; index < game_state.moves.length; index++) {
              const move = game_state.moves[index];
              const delay = index === 0 ? 0 : 1000; // Adjust delay time as needed

              await new Promise((resolve) => {
                setTimeout(() => {
                  // Update the board and highlighted moves
                  setBoard(move.board);
                  setAlphaBetaMove(move.current_player === 1 ? move.move : null);
                  setBfsMove(move.current_player === 2 ? move.move : null);
                  setCurrentMove(move);

                  // Check for game over and set the winner
                  if (index === game_state.moves.length - 1) {
                    setGameOver(game_state.game_over);
                    setWinner(game_state.winner);
                  }

                  resolve();
                }, delay);
              });
            }
          };

          logMovesWithDelay();
        } else {
          console.error('Error in AI vs AI game:', data.message);
        }
      } else {
        console.error('Error starting AI vs AI game:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error.message);
    }
  };

  return (
    <div className='mainboard'>
      <button className='btnai' onClick={startGame}>
        Start AI vs AI
      </button>
      {gameOver && <Win winner={winner} />} {/* Pass the winner information to Win component */}
      <br />
      <div className="player1">
        <div className='rouge'></div>
        <h4>Player 1 turn!</h4>
        <img className='smile' src={smile} alt="" />
      </div>
      <h3>Player 1</h3>

      <div className="board">
        {board.map((column, columnIndex) => (
          <div key={columnIndex} className="column">
            {column.map((cell, rowIndex) => (
              <div
                key={rowIndex}
                className={`cell ${cell === 1 ? 'player1-piece' : cell === 2 ? 'player2-piece' : ''} ${
                  alphaBetaMove && columnIndex === alphaBetaMove[0] && rowIndex === alphaBetaMove[1]
                    ? 'alpha-beta-move'
                    : ''
                } ${
                  bfsMove && columnIndex === bfsMove[0] && rowIndex === bfsMove[1]
                    ? 'bfs-move'
                    : ''
                }`}
              >
                {currentMove &&
                  currentMove.move[0] === columnIndex &&
                  currentMove.move[1] === rowIndex && (
                    <div className="move-indicator">{`Move ${currentMove.index + 1}`}</div>
                  )}
              </div>
            ))}
          </div>
        ))}
      </div>

      <h3>Player 2</h3>
      <div className="player2">
        <img className='smile' src={smile} alt="" />
        <h4>Player 2 turn!</h4>
        <div className='jaune' ></div>
      </div>

      
    </div>
  );
};

export default AIvsAI;


