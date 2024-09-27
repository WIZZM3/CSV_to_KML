
import os
import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
from kml_generator import generate_kml

class Worker(QThread):
    progress_updated = pyqtSignal(int)
    task_completed = pyqtSignal(str)

    def __init__(self, csv_file):
        super().__init__()
        self.csv_file = csv_file

    def run(self):
        try:
            # Load the CSV file
            data = pd.read_csv(self.csv_file)
            total_rows = len(data)

            # Generate KML
            result = generate_kml(data, self.csv_file)
            if result:
                self.task_completed.emit(result)
            else:
                self.task_completed.emit("Error: Could not generate KML")

        except Exception as e:
            self.task_completed.emit(f"Error: {str(e)}")