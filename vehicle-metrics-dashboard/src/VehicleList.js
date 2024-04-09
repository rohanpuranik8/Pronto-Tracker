import React, { useState, useEffect } from 'react';


function clearDatabase() {
  fetch('http://localhost:5000/clear-database', { method: 'POST' })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
}

function VehicleList() {
  const [vehicles, setVehicles] = useState([]); // Correctly use useState

  useEffect(() => {
    const fetchVehicles = () => {
    // Fetch data from the Flask API upon component mount
        fetch('http://localhost:5000/metrics')
        .then(response => response.json())
        .then(data => {
            setVehicles(data); // Update state with fetched data
        })
        .catch(error => console.error('Error fetching data:', error));
    };

    fetchVehicles(); // Fetch immediately on component mount
    const interval = setInterval(fetchVehicles, 1000); // Then fetch every .5 seconds

    return () => clearInterval(interval); // Cleanup interval on component unmount
  
},[]); // Empty dependency array means this effect runs once on mount

  // Correctly structure the return statement
  return (
    <div>
      <h2>Top 10 Ranked Vehicles By Max Measurement</h2>
      <table>
        <thead>
          <tr>
            <th>Rank </th>
            <th>Name </th>
            <th>Max Measure </th>
            <th>Average Measure </th>
            <th>Min Measurement </th>
            <th>Last Latitude </th>
            <th>Last Longitude </th>
            <th>Last Heading </th>
            <th>Total Data Points </th>
          </tr>
        </thead>
        <tbody>
          {vehicles.map((vehicle, index) => (
            <tr key={index}>
              <td>{index + 1}</td> {/* Rank: Adjust index to start from 1 */}
              <td>{vehicle.name}</td>
              <td>{vehicle.max_measurement}</td>
              <td>{vehicle.average_measurement}</td>
              <td>{vehicle.min_measurement}</td>
              <td>{vehicle.last_lat}</td>
              <td>{vehicle.last_lon}</td>
              <td>{vehicle.last_heading}</td>
              <td>{vehicle.total_measurements}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button  className="my-button" onClick={clearDatabase}>Clear Database</button>
    </div>
  );
}

export default VehicleList;
