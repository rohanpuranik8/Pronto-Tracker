import unittest
from App import process_message, get_vehicle_metrics, create_database
import sqlite3


class TestVehicleMetrics(unittest.TestCase):
    """
    Test case for vehicle metrics processing and retrieval.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the database before any tests run.
        """
        create_database()

    # def setUp(self):

    def tearDown(self):
        """
        Clean up after each test.
        """
        """
        Clear the database and insert mock data before each test.
        """
        self.conn = sqlite3.connect("vehicle_data.db", check_same_thread=False)
        cur = self.conn.cursor()
        cur.execute("DELETE FROM vehicle_measurements")  # Clear the table
        self.conn.commit()
        self.conn.close()

    def test_get_vehicle_metrics(self):
        """
        Test that get_vehicle_metrics returns expected data.
        """
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
            "Vehicle6;35.4;-117.9;45;120.5;xyza123",
            "Vehicle6;35.6;-118.2;30;622.7;xyza124",
            "Vehicle6;35.5;-117.8;90;50.3;xyza125",
            "Vehicle7;36.1;-118.5;180;210.2;bcdx234",
            "Vehicle7;36.2;-118.6;270;300.4;bcdx235",
            "Vehicle7;36.3;-118.7;0;110.1;bcdx236",
            "Vehicle8;34.9;-117.5;135;205.7;mnpq345",
            "Vehicle8;34.8;-117.4;225;505.9;mnpq346",
            "Vehicle9;35.0;-117.6;315;310.6;rstu456",
            "Vehicle9;35.1;-117.7;45;412.3;rstu457",
            "Vehicle10;35.2;-117.8;90;123.4;vwxy567",
            "Vehicle10;35.3;-117.9;180;321.7;vwxy568",
        ]

        for entry in mock_data:
            print(entry)
            process_message(entry)

        result_list = get_vehicle_metrics()
        vehicle1_data = next(
            (item for item in result_list if item["name"] == "Vehicle1"), None
        )

        self.assertIsNotNone(vehicle1_data, "Vehicle1 data not found")

        expected = {
            "name": "Vehicle1",
            "max_measurement": 622.7,
            "average_measurement": 264.5,
            "min_measurement": 50.3,
            "total_measurements": 3,
            "last_lat": 35.5,
            "last_lon": -117.8,
            "last_heading": 90.0,
        }

        self.assertEqual(vehicle1_data["name"], expected["name"])
        self.assertAlmostEqual(
            vehicle1_data["max_measurement"], expected["max_measurement"], places=1
        )
        self.assertAlmostEqual(
            vehicle1_data["average_measurement"],
            expected["average_measurement"],
            places=1,
        )
        self.assertAlmostEqual(
            vehicle1_data["min_measurement"], expected["min_measurement"], places=1
        )
        self.assertAlmostEqual(
            vehicle1_data["last_lat"], expected["last_lat"], places=1
        )
        self.assertAlmostEqual(
            vehicle1_data["last_lon"], expected["last_lon"], places=1
        )
        self.assertEqual(vehicle1_data["last_heading"], expected["last_heading"])

    def test_get_vehicle_metrics1Vehicle(self):
        """
        Test that get_vehicle_metrics returns expected data.
        """
        mock_data = [
            "Vehicle1;35.4;-117.9;45;120.5;xyza123",
            "Vehicle1;35.6;-118.2;30;622.7;xyza124",
            "Vehicle1;35.5;-117.8;90;50.3;xyza125",
        ]

        for entry in mock_data:
            print(entry)
            process_message(entry)

        result_list = get_vehicle_metrics()
        vehicle1_data = next(
            (item for item in result_list if item["name"] == "Vehicle1"), None
        )

        self.assertIsNotNone(vehicle1_data, "Vehicle1 data not found")

        expected = {
            "name": "Vehicle1",
            "max_measurement": 622.7,
            "average_measurement": 264.5,
            "min_measurement": 50.3,
            "total_measurements": 3,
            "last_lat": 35.5,
            "last_lon": -117.8,
            "last_heading": 90.0,
        }

        self.assertEqual(vehicle1_data["name"], expected["name"])
        self.assertAlmostEqual(
            vehicle1_data["max_measurement"], expected["max_measurement"], places=1
        )
        self.assertAlmostEqual(
            vehicle1_data["average_measurement"],
            expected["average_measurement"],
            places=1,
        )
        self.assertAlmostEqual(
            vehicle1_data["min_measurement"], expected["min_measurement"], places=1
        )
        self.assertAlmostEqual(
            vehicle1_data["last_lat"], expected["last_lat"], places=1
        )
        self.assertAlmostEqual(
            vehicle1_data["last_lon"], expected["last_lon"], places=1
        )
        self.assertEqual(vehicle1_data["last_heading"], expected["last_heading"])

    @classmethod
    def tearDownClass(cls):
        """
        Clean up once after all tests run.
        """
        # If you want to delete the database file or perform any clean-up, do it here
        pass


if __name__ == "__main__":
    unittest.main()
