import React from 'react';

const MarkerInput = ({ marker, onChange }) => {
    const { lat, lon, label } = marker;
    return (
        <li>
            <label>Latitude:</label>
            <input type="text" value={lat} onChange={onChange} name="lat" />
            <label>Longitude:</label>
            <input type="text" value={lon} onChange={onChange} name="long" />
            <label>Label:</label>
            <input type="text" value={label} onChange={onChange} name="label" />
        </li>
    );
};

export default MarkerInput;
