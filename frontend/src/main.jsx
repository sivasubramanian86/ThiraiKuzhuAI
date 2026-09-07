import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './App';
import '../style.css';
import './theme/cinema_themes.css';

const rootElement = document.getElementById('root');
if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}
