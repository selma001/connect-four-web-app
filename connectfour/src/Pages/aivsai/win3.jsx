// Win.js
import React from 'react';
import '../board/popups.css';
import logo from '../../assets/logo.svg';
import reply from '../../assets/reply.svg';
import { Link } from 'react-router-dom';

function Win({ winner }) {
  return (
    <div className="win">
      <div className="popup-container">
        <img src={logo} alt="" className="logo2" />
        <h2 className="uwon">{winner ? `AI ${winner} wins!` : "It's a draw!"}</h2>
        <div className="btns">
          <button className="btnn1">
            <Link className='yo' to="/">
              <h5>Replay</h5> 
            </Link>
            <img src={reply} alt="" className="awed" />
          </button>
          <button className="cancel">Cancel</button>
        </div>
      </div>
    </div>
  );
}

export default Win;

