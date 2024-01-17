import './popups.css'
import logo from '../../assets/logo.svg'
import reply from '../../assets/reply.svg'

function Lose(){
    return(
        <div className="win">
            <div className="popup-container">   
                <img src={logo}alt=""  className='logo2'/> 
                <h2 className='uwon'>You Lose !</h2>
                <div className='btns '>
                    <button className='btnn1 lose'>
                        <h5>Reply</h5> <img src={reply} alt="" className='awed'/>
                    </button>
                    <button className='cancel'>Cancel</button>
                </div>
            </div>
        </div>
    )
}

export default Lose