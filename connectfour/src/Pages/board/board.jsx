import React, { useState } from 'react';
import smile from '../../assets/smile.svg'
import './board.css';

const Board = () => {

  const [board, setBoard] = useState(Array.from({ length: 7 }, () => Array(6).fill(null)));
  
  return (
    <div className='mainboard'>
        <br /> 
        <div className="player1">
            <div className="rouge"></div>
            <h4>Your turn !</h4>
            <img className='smile' src={smile} alt="" />
        </div> 
        <h3>Player 1</h3>
        <div className="board">
            {board.map((column, columnIndex) => (
                <div key={columnIndex} className="column" >
                {column.map((cell, rowIndex) => (
                <div key={rowIndex} className={`cell ${cell}`} />
                ))}
                </div>
            ))}
        </div>
        <h3>player 2</h3>
        <div className="player2">
            <img className='smile' src={smile} alt="" />
            <h4>Your turn !</h4>
            <div className="jaune"></div>
        </div>
    </div>
  );
};

export default Board;
