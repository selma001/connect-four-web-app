// Win.js
import './popups.css';
import logo from '../../assets/logo.svg';
import reply from '../../assets/reply.svg';
import { Link } from 'react-router-dom';

function Win({ show, onClose, winner }) {
  return (
    // Render the popup only when show is true
    show && (
      <div className="win">
        <div className="popup-container">
          <img src={logo} alt="" className="logo2" />
          <h2 className="uwon">{winner === 'Draw' ? "It's a Draw!" : `${winner} Won!`}</h2>
          <div className="btns">
            
            <button className="btnn1" >
            <Link className='yo' to="/" ><h5>Replay</h5> </Link><img src={reply} alt="" className="awed" />
            </button>
            <button className="cancel" onClick={onClose}>
              Cancel
            </button>
          </div>
        </div>
      </div>
    )
  );
}

export default Win;
