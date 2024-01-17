import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import App from './App';
import Board from './Pages/board/board'
import Win from './Pages/board/win'
import Test from './testbackend'
import PvsP from './Pages/pvsp/PvsP';
import Lose from './Pages/board/lose';
import Draw from './Pages/board/draw';
import AIvsAI from './Pages/aivsai/aivsai';
import Win2 from './Pages/pvsp/win2';
const rootElement = document.getElementById('root');

ReactDOM.createRoot(rootElement).render(
  <Router>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/game" element={<Board />} />
      <Route path="/win" element={<Win/>} />
      <Route path="/test" element={<Test/>} />
      <Route path="/pvsp" element={<PvsP/>} />
      <Route path="/lose" element={<Lose/>} />
      <Route path="/draw" element={<Draw/>} />
      <Route path="/aivsai" element={<AIvsAI/>} />
      <Route path="/win2" element={<Win2/>} />
    </Routes>
  </Router>
);


