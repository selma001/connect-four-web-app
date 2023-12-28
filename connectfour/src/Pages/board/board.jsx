import React, { useState, useEffect } from 'react';
import smile from '../../assets/smile.svg';
import './board.css';

const Board = () => {
  const [board, setBoard] = useState(Array.from({ length: 7 }, () => Array(6).fill({ player: null, clicked: false })));
  const [playerTurn, setPlayerTurn] = useState(true); // Assuming player goes first
  const [loading, setLoading] = useState(false);
  const [aiMove, setAiMove] = useState(null);

  useEffect(() => {
    // Trigger AI's turn when the component mounts
    if (!playerTurn && !loading) {
      handleAITurn();
    }
  }, [playerTurn, loading]);

  const handleCellClick = async (columnIndex, rowIndex) => {
    if (!playerTurn || loading || board[columnIndex][rowIndex].clicked) {
      // If it's not the player's turn, if the previous move is being processed, or if the cell is already clicked, do nothing
      return;
    }

    setLoading(true); // Set loading to true when a move is being processed

    // Send the position to the backend
    await sendMoveToBackend(columnIndex, rowIndex);

    setLoading(false); // Reset loading to false after the response is received

    // AI's turn (if the game is still ongoing)
    if (!board[columnIndex][rowIndex].clicked) {
      await handleAITurn();
    }
  };

  const sendMoveToBackend = async (columnIndex, rowIndex) => {
    try {
      const response = await fetch('/move', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          column: columnIndex,
        }),
      });

      // Handle the response from the backend
      const data = await response.json();
      console.log('Backend response:', data);

      if (data.success) {
        const newBoard = board.map(column => column.map(cell => ({ ...cell }))); // Create a new copy of the board
        newBoard[columnIndex][rowIndex] = { player: 1, clicked: true }; // Assuming the player is represented by 1

        setBoard(newBoard);
        setPlayerTurn(!playerTurn);

        if (data.game_state.game_over) {
          console.log('Game over!');
          // Handle game over logic
        }
      } else {
        // Handle unsuccessful move
        console.log('Error processing move:', data.message);
      }
    } catch (error) {
      console.error('Error sending move to backend:', error);
    }
  };

  const handleAITurn = async () => {
    try {
      const response = await fetch('/ai-move', {
        method: 'GET',
      });

      // Handle the response from the backend
      const data = await response.json();
      console.log('AI Move response:', data);

      if (data.success) {
        const { column, row } = data.move;
        const newBoard = board.map(column => column.map(cell => ({ ...cell }))); // Create a new copy of the board
        newBoard[row][column] = { player: 2, clicked: true }; // Assuming the AI is represented by 2

        setBoard(newBoard);
        setAiMove({ column, row });
        setPlayerTurn(true);

        if (data.game_state.game_over) {
          console.log('Game over!');
          // Handle game over logic
        }
      } else {
        // Handle unsuccessful AI move
        console.log('Error processing AI move:', data.message);
      }
    } catch (error) {
      console.error('Error getting AI move from backend:', error);
    }
  };

  return (
    <div className='mainboard'>
      <br />
      <div className="player1">
        <div className="rouge"></div>
        <h4>Your turn!</h4>
        <img className='smile' src={smile} alt="" />
      </div>
      <h3>Player 1</h3>

      <div className="board">
        {board.map((column, columnIndex) => (
          <div key={columnIndex} className="column">
            {column.map((cell, rowIndex) => (
              <div
                key={rowIndex}
                className={`cell ${cell.clicked ? 'clicked' : ''} ${aiMove && aiMove.column === columnIndex && aiMove.row === rowIndex ? 'ai-move' : ''}`}
                onClick={() => handleCellClick(columnIndex, rowIndex)}
              />
            ))}
          </div>
        ))}
      </div>

      <h3>AI</h3>
      <div className="player2">
        <img className='smile' src={smile} alt="" />
        <h4>AI's turn!</h4>
        <div className="jaune"></div>
      </div>
    </div>
  );
};

export default Board;
