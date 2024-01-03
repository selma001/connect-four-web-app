import React, { useState, useEffect } from 'react';
import smile from '../../assets/smile.svg';
import './aivsai.css';

const AIvsAI = () => {
  const [board, setBoard] = useState(Array.from({ length: 7 }, () => Array(6).fill('')));
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(null);
  const [alphaBetaMove, setAlphaBetaMove] = useState(null);
  const [bfsMove, setBfsMove] = useState(null);

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
          // Log the current board state before updating the React state
          console.log('Current Board State:', game_state.board);
  
          // Update the React state with the new game state
          setBoard(game_state.board);
          setAlphaBetaMove(game_state.ai_moves?.alphabeta);
          setBfsMove(game_state.ai_moves?.bfs);
          setGameOver(game_state.game_over);
          setWinner(game_state.winner);
  
          // Log the current board state after updating the React state
          console.log('Updated Board State:', game_state.board);
  
          // Log the moves made during the game
          game_state.moves.forEach((move, index) => {
            console.log(`Move ${index + 1}: Player ${move.current_player} moved to column ${move.move[0]}, row ${move.move[1]}`);
            console.log('Board State:', move.board);
          });
  
          // Log the final state
          console.log('Final Board State:', game_state.board);
          console.log('Winner:', game_state.winner);
          console.log('Game Over:', game_state.game_over);
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

  useEffect(() => {
    // Start the AI vs AI game when the component mounts
    startGame();
  }, []);

  return (
    <div className='mainboard'>
      <button onClick={startGame}>Start AI vs AI</button>
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
              />
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

      {gameOver && (
        <div>
          {winner ? <p>{`Player ${winner} wins!`}</p> : <p>It's a draw!</p>}
        </div>
      )}
    </div>
  );
};

export default AIvsAI;

