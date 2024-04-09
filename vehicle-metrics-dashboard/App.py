from flask import Flask, jsonify
from flask_cors import CORS
import threading
import logging
import zmq
from collections import defaultdict
import sqlite3

app = Flask(__name__)

##################################################################################################################################
# Unit for Real-time data analysis for vehicle metrics
####################################################################################################################################

data = defaultdict(
    lambda: {
        "measurements": [],
        "last_position": (None, None, None),
        "id": (None),
    }
)


##################################################################################################################################
# Functions to create the database, get the vehicle metrics and process the data
####################################################################################################################################
def create_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("vehicle_data.db", check_same_thread=False)
    c = conn.cursor()

    # Create the table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS vehicle_measurements (
        measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        latitude REAL,
        longitude REAL,
        heading REAL,
        measurement REAL,
        id TEXT)
    """
    )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def get_vehicle_metrics():
    conn = sqlite3.connect("vehicle_data.db", check_same_thread=False)
    cur = conn.cursor()

    # Updated query to fetch last position correctly

    cur.execute(
        """
    SELECT 
        agg.name, 
        agg.max_measurement, 
        agg.avg_measurement, 
        agg.min_measurement, 
        agg.total_measurement,
        latest_entry.latitude AS last_lat, 
        latest_entry.longitude AS last_lon, 
        latest_entry.heading AS last_heading, 
        latest_entry.measurement_id
    FROM
        (SELECT 
            name, 
            MAX(measurement) AS max_measurement, 
            AVG(measurement) AS avg_measurement, 
            MIN(measurement) AS min_measurement,
            COUNT(measurement) AS total_measurement,
            MAX(measurement_id) AS latest_measurement_id 
            
        FROM vehicle_measurements
        GROUP BY name
    ) AS agg
    INNER JOIN vehicle_measurements AS latest_entry
    ON agg.name = latest_entry.name
    AND agg.latest_measurement_id = latest_entry.measurement_id
    ORDER BY agg.max_measurement DESC
    LIMIT 10;

    """
    )

    rows = cur.fetchall()

    result = [
        {
            "name": row[0],
            "max_measurement": row[1],
            "average_measurement": round(row[2], 1),
            "min_measurement": row[3],
            "total_measurements": row[4],  # Ensure this matches your alias in the SQL
            "last_lat": row[5],
            "last_lon": row[6],
            "last_heading": row[7],
        }
        for row in rows
    ]

    conn.close()
    return result


def process_data():
    # ZMQ subscription
    context = zmq.Context()

    socket = context.socket(zmq.SUB)

    socket.connect("tcp://13.56.210.223:5555")

    socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all topics
    print("Starting to listen for ZMQ messages...")

    while True:

        message = socket.recv_string()
        message = process_message(message)

    # Mock data ingestion for demonstration
    # mock_data = [
    # "Vehicle1;34.1;-118.2;90;10.1;abcd1234",
    # "Vehicle2;34.2;-118.3;180;20.2;abcd1235",
    # ]
    # for entry in mock_data:
    #    process_message(entry)


def process_message(message):
    # Split the message into its components
    name, lat, lon, heading, measurement, id = message.split(";")
    # Convert appropriate fields from the message
    message = update_data(
        name, float(lat), float(lon), float(heading), float(measurement), id
    )
    # print(f"Updated data for {name}: {data[name]}")
    return message


def update_data(name, lat, lon, heading, measurement, id):
    # Check if the vehicle name is already in the data dictionary
    if name not in data:
        data[name] = {
            "measurements": [],
            "last_position": (None, None, None),
            "id": None,
        }

    # Update the data dictionary with the new measurement
    vehicle_data = data[name]
    vehicle_data["measurements"].append(measurement)  # Append the new measurement
    vehicle_data["last_position"] = (
        lat,
        lon,  # Update the last known position
        heading,
    )
    vehicle_data["id"] = id  # Update the vehicle ID

    # Call the insert_measurement function to insert data into the database
    insert_measurement(name, lat, lon, heading, measurement, id)


def insert_measurement(name, lat, lon, heading, measurement, id):
    try:
        # The 'with' statement ensures the connection is closed automatically
        with sqlite3.connect("vehicle_data.db", check_same_thread=False) as conn:
            c = conn.cursor()
            c.execute(
                """INSERT INTO vehicle_measurements ( name, latitude, longitude, heading, measurement, id) VALUES (?, ?, ?, ?, ?, ?)""",
                (name, lat, lon, heading, measurement, id),
            )
            # Auto-commit is enabled with the 'with' statement
            print(f"Successfully inserted measurement for {name}: {data[name]}.")
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: Constraint violation for {name}. Error: {e}")
    except sqlite3.OperationalError as e:
        print(f"OperationalError: Operational issue for {name}. Error: {e}")
    except sqlite3.DatabaseError as e:
        print(f"DatabaseError: Database error for {name}. Error: {e}")
    except Exception as e:
        print(f"Unexpected error for {name}. Error: {e}")

    # Close the connection
    conn.close()


####################################################################################################################################
def initialize_flask_app():
    CORS(app)
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.WARNING)
    create_database()
    threading.Thread(target=process_data, daemon=True).start()
    return app


##################################################################################################################################
# Route to get the vehicle metrics
####################################################################################################################################


@app.route("/metrics")
def get_metrics():
    result_list = get_vehicle_metrics()
    return jsonify(result_list)


@app.route("/clear-database", methods=["POST"])
def clear_database():
    conn = sqlite3.connect("vehicle_data.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute("DELETE FROM vehicle_measurements")  # Clear the table
    conn.commit()
    conn.close()
    return jsonify({"message": "Database cleared successfully"})

    ##################################################################################################################################
    # Run API
    ####################################################################################################################################


if __name__ == "__main__":
    app = initialize_flask_app()
    app.run(debug=True)
