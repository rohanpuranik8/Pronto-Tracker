import React from 'react';
import './App.css';
import VehicleList from './VehicleList';
import Monitor from './Monitor';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <VehicleList /> {/* Use the component */}
        <Monitor />{/* Use the component */}
      </header>
    </div>
  );
}

export default App;
