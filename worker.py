import os
import time
import requests
import pandas as pd
import random
from math import cos, radians
from PyQt5.QtCore import QThread, pyqtSignal
from kml_generator import generate_kml

class Worker(QThread):
    progress_updated = pyqtSignal(int)
    task_completed = pyqtSignal(str)

    def __init__(self, csv_file, api_key, output_file, anonymity_enabled, blur_radius):
        super().__init__()
        self.csv_file = csv_file
        self.api_key = api_key
        self.output_file = output_file
        self.anonymity_enabled = anonymity_enabled  # Whether to blur or not
        self.blur_radius = blur_radius  # Blurring radius in meters

    def geocode_address(self, postalcode, city, country):
        """
        Geocode a location using Google Maps Geocoding API and return latitude and longitude,
        with a random blur added to the result within the specified radius if anonymity is enabled.
        """
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        address = f"{postalcode} {city} {country}".replace(" ", "+")  # Format address for URL
        params = {
            'address': address,
            'key': self.api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                location = data['results'][0]['geometry']['location']
                lat, lon = location['lat'], location['lng']
                
                if self.anonymity_enabled:
                    # Apply blurring within the selected radius
                    lat, lon = self.apply_blur(lat, lon, self.blur_radius)
                
                return lat, lon
        return None, None

    def apply_blur(self, lat, lon, radius):
        """
        Blurs the latitude and longitude within the specified radius (in meters).
        """
        radius_in_degrees = radius / 111000  # 1 degree latitude ~ 111km
        angle = random.uniform(0, 360)
        distance = random.uniform(0, radius_in_degrees)
        new_lat = lat + distance * cos(radians(angle))
        new_lon = lon + (distance * cos(radians(angle))) / cos(radians(lat))
        return new_lat, new_lon

    def validate_csv(self, data):
        """
        Validate that the CSV file has the correct columns.
        """
        required_columns = {'PRENOM', 'CP', 'VILLE', 'PAYS'}
        csv_columns = set(data.columns)
        missing_columns = required_columns - csv_columns
        if missing_columns:
            raise ValueError(f"Missing columns: {', '.join(missing_columns)}")

    def run(self):
        try:
            # Load the CSV file
            data = pd.read_csv(self.csv_file)

            # Check if the CSV has the correct format (columns)
            self.validate_csv(data)

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

        except ValueError as ve:
            # CSV formatting error, send the error to the main thread
            self.task_completed.emit(f"Error: {str(ve)}")
        except Exception as e:
            # Handle general exceptions silently and send error to main thread
            self.task_completed.emit(f"Error: {str(e)}")