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
    '48.8556, 2.3158'
  ]);
  const [optimizedPositions, setOptimizedPositions] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/api/calculate', {
        method: 'POST',
        body: JSON.stringify(positions),
        headers: {
          'Content-type': 'application/json'
        }
      });
      const data = await response.json();
      setOptimizedPositions(data);
    } catch (error) {
      console.error('Error optimizing positions:', error);
    }
  };

  const handleChange = (e, index) => {
    const newPositions = [...positions];
    newPositions[index] = e.target.value;
    setPositions(newPositions);
  };

  return (
    <div>
      <h1>Optimize GPS Positions</h1>
      <form onSubmit={handleSubmit}>
        <label>Enter GPS Positions:</label>
        {positions.map((position, index) => (
          <div>
            <input
              key={index}
              type="text"
              value={position}
              onChange={(e) => handleChange(e, index)}
            />
          </div>
        ))}
        <button type="button" onClick={() => setPositions([...positions, ''])}>
          Add Position
        </button>
        <div>
          <h2>...or add from list</h2>
          <textarea value=""></textarea>
          <button type="button" onClick={() => {
            // todo
          }}>
            Add positions list
          </button>
        </div>
        <button type="submit">Optimize Positions</button>
      </form>
      {optimizedPositions.length > 0 && (
        <div>
          <h2>Optimized Positions:</h2>
          <ul>
            {optimizedPositions.map((position, index) => (
              <li key={index}>{position.join(', ')}</li>
            ))}
          </ul>
          <Map positions={optimizedPositions} drawPolyline={true}/>
        </div>
      )}
    </div>
  );
}

export default App;


