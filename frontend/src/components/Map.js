import { MapContainer, Marker, Polyline, Popup, TileLayer } from "react-leaflet";
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

function Map({positions, bestRoute}) {
    const center = positions.length === 0 ? [48.8606, 2.3376] : positions[0];
    return <MapContainer center={center} zoom={13} style={{ height: '400px' }}>
        <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' />
        {positions.map((position, index) => {
            const [lat, lon] = position;
            return (
                <Marker position={position} key={index}>
                    <Popup>{lat}, {lon}</Popup>
                </Marker>
            );
        })}
        {(bestRoute.length > 1) && <Polyline
            pathOptions={{ color: 'red' }}
            positions={bestRoute} />}
    </MapContainer>;
}

export default Map;