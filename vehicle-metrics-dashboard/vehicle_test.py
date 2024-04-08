from App import process_message, get_vehicle_metrics
import sqlite3

mock_data = [
    "Vehicle1;35.4;-117.9;45;120.5;xyza123",
    "Vehicle1;35.6;-118.2;30;622.7;xyza124",
    "Vehicle1;35.5;-117.8;90;50.3;xyza125",
    "Vehicle2;36.1;-118.5;180;210.2;bcdx234",
    "Vehicle2;36.2;-118.6;270;300.4;bcdx235",
    "Vehicle2;36.3;-118.7;0;110.1;bcdx236",
    "Vehicle3;34.9;-117.5;135;205.7;mnpq345",
    "Vehicle3;34.8;-117.4;225;505.9;mnpq346",
    "Vehicle4;35.0;-117.6;315;310.6;rstu456",
    "Vehicle4;35.1;-117.7;45;412.3;rstu457",
    "Vehicle5;35.2;-117.8;90;123.4;vwxy567",
    "Vehicle5;35.3;-117.9;180;321.7;vwxy568",
]

conn = sqlite3.connect("vehicle_data.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("DELETE FROM vehicle_measurements")  # Clear the table
conn.commit()
conn.close()

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

for entry in mock_data:
    process_message(entry)

result_list = get_vehicle_metrics()
print(result_list)

assert result_list == [
    {
        "name": "Vehicle1",
        "max_measurement": 622.7,
        "average_measurement": 264.5,
        "min_measurement": 50.3,
        "last_lat": 35.5,
        "last_lon": -117.8,
        "last_heading": 90.0,
        "id": "xyza125",
    },
    {
        "name": "Vehicle3",
        "max_measurement": 505.9,
        "average_measurement": 355.8,
        "min_measurement": 205.7,
        "last_lat": 34.8,
        "last_lon": -117.4,
        "last_heading": 225.0,
        "id": "mnpq346",
    },
    {
        "name": "Vehicle4",
        "max_measurement": 412.3,
        "average_measurement": 361.5,
        "min_measurement": 310.6,
        "last_lat": 35.1,
        "last_lon": -117.7,
        "last_heading": 45.0,
        "id": "rstu457",
    },
    {
        "name": "Vehicle5",
        "max_measurement": 321.7,
        "average_measurement": 222.6,
        "min_measurement": 123.4,
        "last_lat": 35.3,
        "last_lon": -117.9,
        "last_heading": 180.0,
        "id": "vwxy568",
    },
    {
        "name": "Vehicle2",
        "max_measurement": 300.4,
        "average_measurement": 206.9,
        "min_measurement": 110.1,
        "last_lat": 36.3,
        "last_lon": -118.7,
        "last_heading": 0.0,
        "id": "bcdx236",
    },
]

print(result_list)
