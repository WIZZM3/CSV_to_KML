
import os

def generate_kml(data, csv_file):
    # Create a KML file
    kml_file_name = os.path.splitext(csv_file)[0] + ".kml"
    try:
        with open(kml_file_name, "w", encoding="utf-8") as kml_file:
            # Write the KML header
            kml_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            kml_file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            kml_file.write('  <Document>\n')

            # Write Placemark for each row
            for index, row in data.iterrows():
                kml_file.write('    <Placemark>\n')
                
                # Set the name (e.g., 'PRENOM')
                kml_file.write(f'      <name>{row["PRENOM"]}</name>\n')

                # Set description to an empty value (or remove if unnecessary)
                kml_file.write('      <description></description>\n')

                # Use the address for geolocation (display not required)
                address = f"{str(row['CP']).upper()} {str(row['VILLE']).upper()} {str(row['PAYS']).upper()}"
                kml_file.write(f'      <address>{address}</address>\n')

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

        return kml_file_name

    except Exception as e:
        print(f"Error while creating KML: {str(e)}")
        return None
