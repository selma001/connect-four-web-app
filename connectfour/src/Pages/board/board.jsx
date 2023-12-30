import React, { useState, useEffect } from 'react';
import smile from '../../assets/smile.svg';
import './board.css';

// ... (other imports and components)

const Board = () => {
  const [board, setBoard] = useState(Array.from({ length: 7 }, () => Array(6).fill({ player: null, clicked: false })));
  const [playerTurn, setPlayerTurn] = useState(true);
  const [loading, setLoading] = useState(false);
  const [aiMove, setAiMove] = useState(null);

  const handleCellClick = async (columnIndex, rowIndex) => {
    if (!playerTurn || loading || board[columnIndex][rowIndex].clicked) {
      return;
    }

    setLoading(true);
    console.log(`Player move: Column ${columnIndex}, Row ${5-rowIndex}`);
    await sendMoveToBackend(columnIndex, rowIndex);
    setLoading(false);
  };

  const sendMoveToBackend = async (columnIndex, rowIndex) => {
    try {
      const response = await fetch('/move', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          column:  columnIndex,  // Send column and row as they are
          row: 5 - rowIndex,
        }),
      });

      const data = await response.json();
      console.log('Backend response:', data);

      if (data.success) {
        const newBoard = board.map(column => column.map(cell => ({ ...cell })));

        // Update the player's move
        newBoard[columnIndex][rowIndex] = { player: 1, clicked: true };

        // Update the AI's move
        const newAiMove = data.game_state.ai_move;
        console.log(`AI move: Column ${newAiMove[0]}, Row ${newAiMove[1]}`);
        setAiMove(newAiMove);

        // Check if newAiMove is defined before accessing newBoard[newAiMove[0]]
        if (newAiMove !== undefined && newAiMove.length === 2) {
          const aiRowIndex = Math.max(...Array.from({ length: 6 }, (_, r) => r).filter(r => newBoard[newAiMove[0]][r].player === null));

          // Ensure the AI's move is not overridden
          if (newBoard[newAiMove[0]][aiRowIndex] && newBoard[newAiMove[0]][aiRowIndex].player === null) {
            newBoard[newAiMove[0]][aiRowIndex] = { player: 2, clicked: true };
          }
        }

        setBoard(newBoard);
        setPlayerTurn(true);

        if (data.game_state.game_over) {
          console.log('Game over!');
        }
      } else {
        console.log('Error processing move:', data.message);
      }
    } catch (error) {
      console.error('Error sending move to backend:', error);
    }
  };

  useEffect(() => {
    // Reset aiMove when player's turn begins
    if (playerTurn) {
      setAiMove(null);
    }
  }, [playerTurn]);

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
                className={`cell ${cell.clicked ? 'clicked' : ''} ${aiMove && aiMove[0] === columnIndex && aiMove[1] === rowIndex ? 'ai-move' : ''}`}
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
