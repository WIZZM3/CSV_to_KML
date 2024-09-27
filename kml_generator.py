import os
import pandas as pd

def generate_kml(data, csv_file, output_file_path):
    # Create a KML file with the provided output path
    try:
        with open(output_file_path, "w", encoding="utf-8") as kml_file:
            # Write the KML header
            kml_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            kml_file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            kml_file.write('  <Document>\n')

            # Write Placemark for each row
            for index, row in data.iterrows():
                kml_file.write('    <Placemark>\n')

                # Set the name (e.g., 'PRENOM')
                kml_file.write(f'      <name>{row["PRENOM"]}</name>\n')

                # Use the geocoded coordinates for the placemark location
                if pd.notna(row['LATITUDE']) and pd.notna(row['LONGITUDE']):
                    kml_file.write('      <Point>\n')
                    kml_file.write(f'        <coordinates>{row["LONGITUDE"]},{row["LATITUDE"]},0</coordinates>\n')
                    kml_file.write('      </Point>\n')

                # Add the ExtendedData block to display CP, VILLE, and PAYS
                kml_file.write('      <ExtendedData>\n')
                kml_file.write(f'        <Data name="CP">\n')
                kml_file.write(f'          <value>{row["CP"]}</value>\n')
                kml_file.write('        </Data>\n')

                kml_file.write(f'        <Data name="VILLE">\n')
                kml_file.write(f'          <value>{row["VILLE"]}</value>\n')
                kml_file.write('        </Data>\n')

                kml_file.write(f'        <Data name="PAYS">\n')
                kml_file.write(f'          <value>{row["PAYS"]}</value>\n')
                kml_file.write('        </Data>\n')
                kml_file.write('      </ExtendedData>\n')

                kml_file.write('    </Placemark>\n')

            kml_file.write('  </Document>\n')
            kml_file.write('</kml>\n')

        return output_file_path

    except Exception as e:
        print(f"Error while creating KML: {str(e)}")
        return None