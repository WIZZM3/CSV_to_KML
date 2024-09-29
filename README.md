# CSV to KML Converter

This Python project allows you to convert a CSV file containing postal codes, cities, and countries into a KML file. The KML file includes geocoded placemarks, with their locations automatically retrieved via the **Google Maps Geocoding API**. You need a valid Google API key for geocoding.

## Features
- **CSV to KML Conversion**: Converts a CSV file with postal code, city, and country information into a KML file with geocoded placemarks.
- **Google Geocoding**: Automatically geocodes the addresses (postal code, city, country) using the Google Maps Geocoding API.
- **Progress Tracking**: The application tracks and displays the progress of geocoding and KML file generation.
- **Anonymity Mode**: Users can enable an anonymity feature that blurs geocoded locations within a configurable radius.

## Requirements

The following Python libraries are required for this project:

```bash
pip install -r requirements.txt
```

### Python Dependencies:
- `pandas`
- `PyQt5`
- `requests`
- `chardet`

### Additional System Requirements (Linux):

If you are running this project on Linux, you need to ensure that the required system dependencies are installed. These dependencies include OpenGL support and other essential libraries for the application to function correctly.

To install the necessary packages, run the following script:

```bash
./install_linux_deps.sh
```

This script will automatically install the required packages using `apt`.

Additionally, you will need a **Google API key** to use the Google Maps Geocoding API. You can obtain one from [Google API Key Documentation](https://developers.google.com/maps/documentation/geocoding/get-api-key?hl=fr).

## How to Use

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/CSV_to_KML.git
   cd CSV_to_KML
   ```

2. **Install the Requirements**:
   Make sure you have Python and pip installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install System Dependencies (Linux only)**:
   If you are on a Linux system, install additional system dependencies by running:
   ```bash
   ./install_linux_deps.sh
   ```

4. **Run the Application**:
   You can run the GUI application using the following command:
   ```bash
   python main.py
   ```

5. **Provide CSV File and API Key**:
   - Use the GUI to select a CSV file containing the columns: `PRENOM`, `CP` (Postal Code), `VILLE` (City), and `PAYS` (Country).
   - Enter your **Google Maps API key** for geocoding.
   - Click on the **Generate KML** button to generate the KML file.

6. **Output KML File**:
   The KML file will be saved in the location you choose, and it will include placemarks geocoded from the provided postal code, city, and country.

7. **Visualize on Google MyMaps**:
   Once the KML file is generated, you can upload it to [Google MyMaps](https://www.google.com/mymaps) to visualize the placemarks.

## CSV File Format

The CSV file should have the following columns:

- `PRENOM` (Name)
- `CP` (Postal Code)
- `VILLE` (City)
- `PAYS` (Country)

Example:

```csv
PRENOM,CP,VILLE,PAYS
John,55000,LOISEY,FRANCE
Jane,75001,PARIS,FRANCE
```

## Directory Structure

```
CSV_to_KML/
│
├── main.py                # Main entry point for the PyQt app
├── ui.py                  # The PyQt GUI logic
├── worker.py              # The worker thread for file processing and geocoding
├── kml_generator.py       # KML generation logic
├── ressources/            # Directory for resources (images, etc.)
│   └── icon.png           # The icon used in the GUI
├── install_linux_deps.sh   # Script to install Linux system dependencies
└── requirements.txt       # Python dependencies list
```

## How It Works

1. **CSV Parsing**: The script reads the CSV file and ensures that the necessary columns (`PRENOM`, `CP`, `VILLE`, `PAYS`) are present.
2. **Google Geocoding**: The addresses are geocoded using the Google Maps Geocoding API by passing the postal code, city, and country from the CSV file.
3. **KML Generation**: Once geocoded, the KML file is generated, containing the geocoded placemarks.

## License

This project is licensed under the MIT License.