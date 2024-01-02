import React, { useState } from 'react';
import smile from '../../assets/smile.svg';
import './PvsP.css';

const PvsP = () => {
  const [board, setBoard] = useState(Array.from({ length: 7 }, () => Array(6).fill('')));
  const [currentPlayer, setCurrentPlayer] = useState(1);

  const handleCellClick = (columnIndex, rowIndex) => {
    // Check if the cell is empty before making a move
    if (!board[columnIndex][rowIndex]) {
      const newBoard = [...board];
      newBoard[columnIndex][rowIndex] = currentPlayer === 1 ? 'red' : 'yellow';
      setBoard(newBoard);

      // Send the move to the backend
      fetch('/pvsp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          column: columnIndex,
          row:5 - rowIndex,
        }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // Check for game over
            if (data.game_over) {
              alert('Game over!');  // You can replace this with a more user-friendly notification
            } else {
              setCurrentPlayer(data.current_player);
            }
          } else {
            alert(data.message);  // You can replace this with a more user-friendly notification
          }
        })
        .catch(error => console.error('Error:', error));
    }
  };

  return (
    <div className='mainboard'>
      <br />
      <div className="player1">
        <div className='rouge'></div>
        <h4>{`Player ${currentPlayer}'s turn!`}</h4>
        <img className='smile' src={smile} alt="" />
      </div>
      <h3>Player 1</h3>

      <div className="board">
        {board.map((column, columnIndex) => (
          <div key={columnIndex} className="column">
            {column.map((cell, rowIndex) => (
              <div
                key={rowIndex}
                className={`cell ${cell}`}
                onClick={() => handleCellClick(columnIndex, rowIndex)}
              />
            ))}
          </div>
        ))}
      </div>

      <h3>Player 2</h3>
      <div className="player2">
        <img className='smile' src={smile} alt="" />
        <h4>{`Player ${currentPlayer === 1 ? 2 : 1}'s turn!`}</h4>
        <div className='jaune' ></div>
      </div>
    </div>
  );
};

export default PvsP;
