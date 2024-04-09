ProntoApp


ProntoApp is a dynamic vehicle tracking application designed to monitor and display real-time metrics of vehicles. Built with React, Flask, and SQLite, it showcases vehicle positions on an interactive map and ranks vehicles based on their maximum measurements.

Features
real-time vehicle data visualization on an interactive map.
Ranking of vehicles based on max measurements.
REST API for easy integration with external systems.
Lightweight SQLite database for efficient data handling.
Responsive design for a seamless experience across devices.
Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
Node.js and npm
Python 3
Flask
SQLite
Installing

Clone the repository:
bash
git clone https://github.com/rohanpuranik8/prontoapp.git
cd prontoapp

Setting up the Backend

Install the required Python packages:
bash
pip install -r requirements.txt

Start the Flask application:
bash
flask run
Setting up the Frontend


Navigate to the frontend directory and install the necessary npm packages:
bash
cd ../vehicle-metrics-dashboard
npm install


Start the React development server:
bash
npm start
The application should now be running and accessible at http://localhost:3000.

Usage
Navigate to http://localhost:3000 in your web browser to view the application. The main page displays a map with real-time vehicle positions and a sidebar listing the top-ranked vehicles based on their maximum measurement.

API Reference
Clear Database
URL: /api/clear
Method: POST
Description: Clears the vehicle measurements from the database.
Fetch Top 10 Vehicles
URL: /api/metrics
Method: GET
Description: Retrieves metrics for the top 10 ranked vehicles.


License
This project is licensed under the MIT License - see the LICENSE.md file for details.

Acknowledgments
Thanks to the React community for the comprehensive documentation.
Flask for a simple yet powerful web framework.
SQLite for providing a lightweight database solution.
