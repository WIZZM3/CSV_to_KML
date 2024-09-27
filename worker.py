import os
import time
import requests
import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
from kml_generator import generate_kml

class Worker(QThread):
    progress_updated = pyqtSignal(int)
    task_completed = pyqtSignal(str)

    def __init__(self, csv_file, api_key, output_file):
        super().__init__()
        self.csv_file = csv_file
        self.api_key = api_key
        self.output_file = output_file  # Pass the output file path

    def geocode_address(self, postalcode, city, country):
        """
        Geocode a location using Google Maps Geocoding API and return latitude and longitude.
        Constructs the address from postalcode, city, and country.
        """
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        address = f"{postalcode} {city} {country}".replace(" ", "+")  # Format address properly for URL
        params = {
            'address': address,  # The formatted address
            'key': self.api_key   # API key from the user
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                location = data['results'][0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                print(f"Google API error: {data['status']}")
        return None, None

    def run(self):
        try:
            # Load the CSV file
            data = pd.read_csv(self.csv_file)
            total_rows = len(data)

            # Add latitude and longitude columns
            data['LATITUDE'] = None
            data['LONGITUDE'] = None

            # Geocode each location using postal code, city, and country
            for index, row in data.iterrows():
                postalcode = row['CP']
                city = row['VILLE']
                country = row['PAYS']
                lat, lng = self.geocode_address(postalcode, city, country)

                if lat is not None and lng is not None:
                    data.at[index, 'LATITUDE'] = lat
                    data.at[index, 'LONGITUDE'] = lng
                else:
                    print(f"Failed to geocode location: {postalcode}, {city}, {country}")

                # Update progress
                self.progress_updated.emit(int((index + 1) / total_rows * 100))

                # Delay between API requests to avoid hitting rate limits
                time.sleep(0.1)

            # Generate KML with latitude and longitude and output file path
            result = generate_kml(data, self.csv_file, self.output_file)
            if result:
                self.task_completed.emit(result)
            else:
                self.task_completed.emit("Error: Could not generate KML")

        except Exception as e:
            self.task_completed.emit(f"Error: {str(e)}")