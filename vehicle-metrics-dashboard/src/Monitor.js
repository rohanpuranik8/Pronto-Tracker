import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';


// Function to get a divIcon based on vehicle index (rank)
const getArrowheadIcon = () => {
  // Construct class name dynamically. If the index is beyond your specific styles, use a default class.
  const className = `leaflet-arrowhead-marker arrowhead-rank-0` || 'leaflet-arrowhead-marker arrowhead-default';
  return L.divIcon({ className: className, iconSize: L.point(10, 10) }); // Adjust iconSize as needed
};

const Monitor = () => {
  const [vehicles, setVehicles] = useState([]);

  useEffect(() => {
    const fetchVehicles = () => {
      fetch('http://localhost:5000/metrics')
        .then(response => response.json())
        .then(data => {
          console.log('Fetched Data:', data); // Log fetched data
          setVehicles(data);
        })
        .catch(error => console.error('Error:', error));
    };

    fetchVehicles();
    const interval = setInterval(fetchVehicles, 2000); // Adjust based on your needs

    return () => clearInterval(interval);
  }, []);

  return (
    <MapContainer center={[38, -122]} zoom={6} style={{ height: '500px', width: '500px' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {vehicles.map((vehicle, index) => (
        <Marker key={index} position={[vehicle.last_lat, vehicle.last_lon]} icon={getArrowheadIcon(index)}>
          <Popup>
            Rank: {index + 1}<br />
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