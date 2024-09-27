import os
import zipfile

def generate_kmz(data, csv_file, png_file):
    # Create a KML file
    kml_file_name = os.path.splitext(csv_file)[0] + ".kml"
    try:
        with open(kml_file_name, "w", encoding="utf-8") as kml_file:
            kml_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            kml_file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            kml_file.write('  <Document>\n')
            
            # Include the custom icon reference
            kml_file.write('    <Style id="customPin">\n')
            kml_file.write('      <IconStyle>\n')
            kml_file.write('        <Icon>\n')
            kml_file.write(f'          <href>images/{os.path.basename(png_file)}</href>\n')
            kml_file.write('        </Icon>\n')
            kml_file.write('      </IconStyle>\n')
            kml_file.write('    </Style>\n')

            # Write Placemark for each row with address (uppercase)
            for index, row in data.iterrows():
                # Format the address in uppercase
                address = f"{str(row['CP']).upper()} {str(row['VILLE']).upper()}, {str(row['PAYS']).upper()}"
                kml_file.write('    <Placemark>\n')
                kml_file.write(f'      <name>{row["PRENOM"]}</name>\n')
                kml_file.write('      <styleUrl>#customPin</styleUrl>\n')
                kml_file.write(f'      <address>{address}</address>\n')
                kml_file.write('    </Placemark>\n')

            kml_file.write('  </Document>\n')
            kml_file.write('</kml>\n')

        # Create KMZ file, placing the KML in the root and the PNG in "images/"
        kmz_file_name = os.path.splitext(csv_file)[0] + ".kmz"
        with zipfile.ZipFile(kmz_file_name, 'w', zipfile.ZIP_DEFLATED) as kmz:
            kmz.write(kml_file_name, os.path.basename(kml_file_name))  # KML in root
            kmz.write(png_file, f'images/{os.path.basename(png_file)}')  # PNG in images/

        os.remove(kml_file_name)  # Clean up the KML file
        return kmz_file_name
    except Exception as e:
        return f"Error: {str(e)}"