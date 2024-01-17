import './main.css'
import React from 'react';
import logo from '../../assets/logo.svg'
import { Link } from 'react-router-dom';

function Main(){
    return (
        <div className="main">
            <img src={logo} alt="" className='logo'/>
            <h1 >Connect Four</h1>
            <div className='buttons'>
                <button className='btn1'> <Link className='yo' to="/pvsp" >Player vs Player </Link></button> <br />
                <button className='btn2'><Link className='yo' to="/game" >Player vs Ai</Link></button> <br />
                <button className='btn3'><Link className='yo' to="/AIvsAI" >Ai vs Ai</Link></button> <br />
            </div>
            <h3>Problem solving project</h3>
        </div>
    )
}

export default Main 