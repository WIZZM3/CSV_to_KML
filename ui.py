
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QProgressBar
)
from PyQt5.QtCore import Qt
from worker import Worker

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("KML Generator")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.csv_file_path = None

        # Label and button to select CSV file
        self.csv_label = QLabel("Select CSV File:")
        self.layout.addWidget(self.csv_label)
        self.csv_button = QPushButton("Browse CSV")
        self.csv_button.clicked.connect(self.select_csv_file)
        self.layout.addWidget(self.csv_button)

        # Button to start generating KML
        self.generate_button = QPushButton("Generate KML")
        self.generate_button.clicked.connect(self.generate_kml)
        self.layout.addWidget(self.generate_button)
        self.generate_button.setEnabled(False)

        # Progress bar for task
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.progress)

    def select_csv_file(self):
        # Select the CSV file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)", options=options)
        
        if file_path:
            self.csv_file_path = file_path
            self.csv_label.setText(f"CSV File: {file_path}")
            self.generate_button.setEnabled(True)

    def generate_kml(self):
        # Ensure a CSV file is selected before starting
        if not self.csv_file_path:
            QMessageBox.critical(self, "Error", "Please select a CSV file before generating KML.")
            return
        
        # Disable button and start background processing
        self.generate_button.setEnabled(False)
        self.worker = Worker(self.csv_file_path)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.task_completed.connect(self.on_task_completed)
        self.worker.start()

    def update_progress(self, progress_value):
        self.progress.setValue(progress_value)

    def on_task_completed(self, result):
        if "Error" in result:
            QMessageBox.critical(self, "Error", result)
        else:
            QMessageBox.information(self, "Success", f"KML file created: {result}")
        self.progress.setValue(0)
        self.generate_button.setEnabled(True)
