# CSV to KMZ with Geocoding

This Python script allows you to convert a CSV file with postal codes, cities, and countries into a KMZ file for use in Google Earth. The script will geocode the addresses into latitude and longitude coordinates, create a KML file, and compress it into a KMZ file.

## Features
- Geocodes addresses from a CSV file (postal code, city, country)
- Converts geocoded data into a KML file
- Compresses the KML file into a KMZ for easy use in Google Earth
- Modern GUI built using PyQt5 to select your CSV file

## Requirements

Before running the script, install the necessary dependencies:

```bash
pip install -r requirements.txt