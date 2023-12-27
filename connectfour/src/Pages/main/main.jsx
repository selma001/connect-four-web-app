import './main.css'
import React from 'react';
import logo from '../../assets/logo.svg'

function Main(){
    return (
        <div className="main">
            <img src={logo} alt="" className='logo'/>
            <h1 >Connect Four</h1>
            <div className='buttons'>
                <button className='btn1'>Player vs Player</button> <br />
                <button className='btn2'>Player vs Ai</button> <br />
                <button className='btn3'>Ai vs Ai</button> <br />
            </div>
            <h3>Problem solving project</h3>
        </div>
    )
}

export default Main 