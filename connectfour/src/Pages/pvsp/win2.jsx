// Win2.js
import '../board/popups.css';
import logo from '../../assets/logo.svg';
import reply from '../../assets/reply.svg';
import { Link } from 'react-router-dom';

function Win2({ winner }) {
  let message;

  if (winner === 'Draw') {
    message = "It's a Draw!";
  } else {
    message = `${winner === 1 ? 'Player 1' : 'Player 2'} Won!`;
  }

  return (
    <div className="win">
      <div className="popup-container">
        <img src={logo} alt="" className="logo2" />
        <h2 className="uwon">{message}</h2>
        <div className="btns">
          <button className="btnn1">
            <Link className='yo' to="/"><h5>Replay</h5> </Link><img src={reply} alt="" className="awed" />
          </button>
          <button className="cancel">
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export default Win2;

