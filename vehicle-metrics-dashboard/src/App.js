import React from 'react';
import './App.css';
import VehicleList from './VehicleList';
import Monitor from './Monitor';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div className="VehicleList">
          <VehicleList />{ /*Use the component */}
        </div>
        <div className="Monitor">
          <Monitor />{/* Use the component */}
        </div>
      </header>
    </div>
  );
}

export default App;
