import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import App from './App';
import Board from './Pages/board/board'
import Win from './Pages/popups/win'
import Test from './testbackend';

const rootElement = document.getElementById('root');

ReactDOM.createRoot(rootElement).render(
  <Router>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/game" element={<Board />} />
      <Route path="/win" element={<Win/>} />
      <Route path="/test" element={<Test/>} />
    </Routes>
  </Router>
);


