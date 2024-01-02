import './popups.css'
import logo from '../../assets/logo.svg'
import reply from '../../assets/reply.svg'

function Win(){
    return(
        <div className="win">
            <div className="popup-container">   
                <img src={logo}alt=""  className='logo2'/> 
                <h2 className='uwon'>You Won !</h2>
                <div className='btns'>
                    <button className='btnn1'>
                        <h5>Reply</h5> <img src={reply} alt="" className='awed'/>
                    </button>
                    <button className='cancel'>Cancel</button>
                </div>
            </div>
        </div>
    )
}

export default Win