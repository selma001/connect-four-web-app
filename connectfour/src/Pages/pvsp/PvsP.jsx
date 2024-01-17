import React, { useState } from 'react';
import smile from '../../assets/smile.svg';
import Win2 from './win2';
import './PvsP.css'

const PvsP = () => {
  const [board, setBoard] = useState(Array.from({ length: 7 }, () => Array(6).fill('')));
  const [currentPlayer, setCurrentPlayer] = useState(1);
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(null);

  const handleCellClick = (columnIndex, rowIndex) => {
    if (gameOver) {
      return;
    }

    if (!board[columnIndex][rowIndex]) {
      const newBoard = [...board];
      newBoard[columnIndex][rowIndex] = currentPlayer;
      setBoard(newBoard);

      // Send the move to the backend
      fetch('/pvsp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          column: columnIndex,
          row: 5 - rowIndex,
        }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            if (data.game_over) {
              setGameOver(true);
              setWinner(data.winner);
            } else {
              setCurrentPlayer(data.current_player);
            }
          } else {
            alert(data.message);
          }
        })
        .catch(error => console.error('Error:', error));
    }
  };

  return (
    <div className='mainboard'>
      <br />
      <div className="player1">
        <div className= 'rouge' ></div>
        <h4>{gameOver ? 'Game Over' : `Player ${currentPlayer}'s turn!`}</h4>
        <img className='smile' src={smile} alt="" />
      </div>
      <h3>Player 1</h3>

      <div className="board">
        {board.map((column, columnIndex) => (
          <div key={columnIndex} className="column">
            {column.map((cell, rowIndex) => (
              <div
                key={rowIndex}
                className={`cell ${cell === 1 ? 'red' : cell === 2 ? 'yellow' : ''}`}
                onClick={() => handleCellClick(columnIndex, rowIndex)}
              />
            ))}
          </div>
        ))}
      </div>

      <h3>Player 2</h3>
      <div className="player2">
        <img className='smile' src={smile} alt="" />
        <h4>{gameOver ? 'Game Over' : `Player ${currentPlayer === 1 ? 2 : 1}'s turn!`}</h4>
        <div className='jaune' ></div>
      </div>

      {gameOver && <Win2 winner={winner} />}
    </div>
  );
};

export default PvsP;

