import unittest
import weather_app
import os


class TestWeatherApp(unittest.TestCase):

    def test_valid_connection(self):
        # weather_app.load_dotenv()
        # self.assertEqual(os.getenv("API_KEY"), weather_app.get_key(), "Invalid API key")


if __name__ == "__main__":
    unittest.main()