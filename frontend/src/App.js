import React, { useState } from 'react';
import Map from './components/Map';

function App() {
  const [positions, setPositions] = useState([
    '48.8606, 2.3376',
    '48.8530, 2.3499',
    '48.8738, 2.2950',
    '48.8867, 2.3431',
    '48.8609, 2.3267',
    '48.8698, 2.3075',
    '48.8635, 2.3274',
    '48.8462, 2.3447',
    '48.8656, 2.3212',
    '48.8556, 2.3158',
    ''
  ]);
  const [bestRoute, setBestRoute] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/api/calculate', {
        method: 'POST',
        body: JSON.stringify(positionsObj),
        headers: {
          'Content-type': 'application/json'
        }
      });
      const data = await response.json();
      setBestRoute(data);
    } catch (error) {
      console.error('Error optimizing positions:', error);
    }
  };

  const positionsObj = positions.filter(e => e !== '').map(p => p.split(",").map(e => parseFloat(e)));

  const handleChange = (e, index) => {
    const newPositions = [...positions];
    newPositions[index] = e.target.value;
    setPositions(newPositions);
  };

  const handlePaste = (e, index) => {
    e.preventDefault();
    const pastedTxt = e.clipboardData.getData('text');
    const newPositionsList = pastedTxt.split(/\r?\n/).filter(e => e !== '');
    setPositions(prev => [
      ...prev.slice(0, index),
      ...newPositionsList,
      ...prev.slice(index + 1)
    ]);
  };

  return (
    <div>
      <h1>Optimize GPS Positions</h1>
      <form onSubmit={handleSubmit}>
        <label>Enter GPS Positions:</label>
        {positions.map((position, index) => (
          <div key={index}>
            <input
              key={index}
              type="text"
              value={position}
              onChange={(e) => handleChange(e, index)}
              onPaste={(e) => handlePaste(e, index)}
            />
          </div>
        ))}
        <button type="button" onClick={() => setPositions([...positions, ''])}>
          Add Position
        </button>
        <button type="submit">Optimize Positions</button>
        <button type='button' onClick={() => setPositions([])}>Clear</button>
      </form>
        <div>
          <h2>Optimized Positions:</h2>
          <ul>
            {bestRoute.map(([lat, lon], index) => (
              <li key={index}>{lat}, {lon}</li>
            ))}
          </ul>
          <Map positions={positionsObj} bestRoute={bestRoute}/>
        </div>
    </div>
  );
}

export default App;


