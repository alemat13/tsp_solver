import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function App() {
  const [positions, setPositions] = useState(['']);
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
          <MapContainer center={optimizedPositions[0]} zoom={13} style={{ height: '400px' }}>
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {optimizedPositions.map((position, index) => {
              console.log(position);
              const [lat, lon] = position;
              return (
                <Marker position={[parseFloat(lat), parseFloat(lon)]} key={index}>
                  <Popup>{position}</Popup>
                </Marker>
              );
            })}
            <Polyline
             pathOptions={{color: 'red'}}
             positions={optimizedPositions.map(p => [parseFloat(p[0]), parseFloat(p[1])])}
            />
          </MapContainer>
        </div>
      )}
    </div>
  );
}

export default App;
