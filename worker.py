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
            else:
                print(f"Google API error: {data['status']}")
        return None, None

    def apply_blur(self, lat, lon, radius):
        """
        Blurs the latitude and longitude within the specified radius (in meters).
        """
        # Convert radius from meters to degrees (approximation)
        radius_in_degrees = radius / 111000  # 1 degree latitude ~ 111km

        # Generate random angle and distance for blurring
        angle = random.uniform(0, 360)  # Random direction in degrees
        distance = random.uniform(0, radius_in_degrees)  # Random distance within radius

        # Calculate the new latitude
        new_lat = lat + distance * cos(radians(angle))

        # Calculate the new longitude, adjusted by the latitude
        new_lon = lon + (distance * cos(radians(angle))) / cos(radians(lat))

        return new_lat, new_lon

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