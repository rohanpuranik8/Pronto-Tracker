import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const Monitor = () => {
  const [vehicles, setVehicles] = useState([]);

  useEffect(() => {
    const fetchVehicles = () => {
      fetch('http://localhost:5000/metrics')
        .then(response => response.json())
        .then(data => setVehicles(data))
        .catch(error => console.error('Error:', error));
    };

    fetchVehicles();
    const interval = setInterval(fetchVehicles, 5000); // Adjust based on your needs

    return () => clearInterval(interval);
  }, []);

  return (
    <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: '100vh', width: '100wh' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {vehicles.map((vehicle, index) => (
        <Marker key={index} position={[vehicle.last_lat, vehicle.last_lon]}>
          <Popup>
            Name: {vehicle.name}<br />
            Max Measure: {vehicle.max_measurement}<br />
            Avg Measure: {vehicle.average_measurement}<br />
            Min Measure: {vehicle.min_measurement}<br />
            Last Heading: {vehicle.last_heading}<br />
            Total Data Points: {vehicle.total_measurements}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default Monitor;