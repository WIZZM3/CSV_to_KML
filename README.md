# CSV to KMZ Converter

This Python project allows you to convert a CSV file containing postal codes, cities, and countries into a KMZ file, which can be used in Google MyMaps. The KMZ file includes placemarks with custom icons, and addresses are automatically geocoded by Google MyMaps.

## Features
- **CSV to KMZ Conversion**: Converts a CSV file with address information into a KMZ file.
- **Custom Icons**: Allows you to select a custom PNG icon for the placemarks.
- **Automatic Geocoding**: The CSV addresses are not geocoded by the script but instead handled by Google MyMaps when the KMZ file is uploaded.
- **Uppercase Addresses**: The addresses in the KMZ file are formatted in uppercase for consistency.

## Requirements

The following Python libraries are required for this project:

```bash
pip install -r requirements.txt
```

Dependencies:

- `pandas`
- `PyQt5`
- `chardet`

## How to Use

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/CSV_to_KMZ.git
   cd CSV_to_KMZ
   ```

2. **Install the Requirements**:
   Make sure you have Python and pip installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   You can run the GUI application using the following command:
   ```bash
   python main.py
   ```

4. **Select CSV and PNG Files**:
   - Use the GUI to select a CSV file containing the columns: `PRENOM`, `CP` (Postal Code), `VILLE` (City), and `PAYS` (Country).
   - Select a custom PNG icon to be used for the placemarks.
   - Click on the **Validate and Generate KMZ** button to generate the KMZ file.

5. **Upload to Google MyMaps**:
   Once the KMZ file is generated, you can upload it to [Google MyMaps](https://www.google.com/mymaps) to visualize the placemarks. Google will automatically geocode the addresses.

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
CSV_to_KMZ/
│
├── main.py                # Main entry point for the PyQt app
├── ui.py                  # The PyQt GUI logic
├── worker.py              # The worker thread for file processing
├── kmz_generator.py       # KMZ and KML generation logic
├── ressources/            # Directory for resources (images)
│   └── icon.png           # The icon used in the GUI
└── requirements.txt       # Dependencies list
```

## How It Works

1. **CSV Parsing**: The script reads the CSV file and ensures that the necessary columns (`PRENOM`, `CP`, `VILLE`, `PAYS`) are present.
2. **KMZ Generation**: It generates a KML file, which is compressed into a KMZ file. The addresses are included in the KML as `<address>` tags, and Google MyMaps handles the geocoding.
3. **Custom Icons**: You can choose a custom PNG icon, which will be embedded in the KMZ and displayed for each placemark.

## License

This project is licensed under the MIT License.

---

### Summary of Changes in the `README.md`:
1. **Updated Project Name**: Changed to **`CSV to KMZ Converter`**.
2. **New Features**: Detailed the use of custom icons and automatic geocoding by Google MyMaps.
3. **Installation Instructions**: Clear instructions on how to clone the repo, install dependencies, and run the application.
4. **CSV Format and Example**: Added detailed instructions on the required CSV columns.
5. **Directory Structure**: Updated the file structure for clarity.
6. **How It Works**: Explained the workflow, from CSV reading to KMZ generation and MyMaps integration.

---

Once you've updated the `README.md` locally, follow these steps to commit the change:

### Commit the Updated `README.md` to GitHub:

1. **Add the file**:
   ```bash
   git add README.md
   ```

2. **Commit the changes**:
   ```bash
   git commit -m "Updated README.md with project details and renamed repository to CSV_to_KMZ"
   ```

3. **Push the changes**:
   ```bash
   git push origin main
   ```

Let me know if you need any further changes!