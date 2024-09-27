import os
import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
from kmz_generator import generate_kmz

class Worker(QThread):
    progress_updated = pyqtSignal(int)
    task_completed = pyqtSignal(str)

    def __init__(self, csv_file, encoding, png_file):
        super().__init__()
        self.csv_file = csv_file
        self.encoding = encoding  # Store encoding
        self.png_file = png_file

    def run(self):
        try:
            # Load the CSV file with the detected encoding
            data = pd.read_csv(self.csv_file, encoding=self.encoding)
            
            # Proceed without geocoding (just address formatting)
            total_rows = len(data)

            # Generate KML and KMZ
            result = generate_kmz(data, self.csv_file, self.png_file)
            self.task_completed.emit(result)

        except Exception as e:
            self.task_completed.emit(f"Error: {str(e)}")