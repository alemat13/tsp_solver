import { MapContainer, Marker, Polyline, Popup, TileLayer } from "react-leaflet";
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

function Map(props) {
    const {positions, drawPolyline} = props;
    return <MapContainer center={positions[0]} zoom={13} style={{ height: '400px' }}>
        <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' />
        {positions.map((position, index) => {
            console.log(position);
            const [lat, lon] = position;
            return (
                <Marker position={[parseFloat(lat), parseFloat(lon)]} key={index}>
                    <Popup>{position}</Popup>
                </Marker>
            );
        })}
        {drawPolyline && <Polyline
            pathOptions={{ color: 'red' }}
            positions={positions.map(p => [parseFloat(p[0]), parseFloat(p[1])])} />}
    </MapContainer>;
}

export default Map;