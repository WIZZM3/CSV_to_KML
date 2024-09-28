import os
import winsound  # Import winsound for sound notification
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QProgressBar, QLineEdit, QMessageBox, QCheckBox, QComboBox
)
from PyQt5.QtGui import QIcon  # Import QIcon for the window icon
from PyQt5.QtCore import Qt
from worker import Worker

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV to KML")  # Updated the window title
        self.setWindowIcon(QIcon('ressources/icon.ico'))  # Set the window icon from ressources

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.csv_file_path = None
        self.api_key = None
        self.output_file_path = None

        # Label and button to select CSV file
        self.csv_label = QLabel("Select CSV File:")
        self.layout.addWidget(self.csv_label)

        self.csv_button = QPushButton("Browse CSV")
        self.csv_button.clicked.connect(self.select_csv_file)
        self.layout.addWidget(self.csv_button)

        # Input field for API Key
        self.api_key_input = QLineEdit(self)
        self.api_key_input.setPlaceholderText("Enter your Google API key")
        self.layout.addWidget(self.api_key_input)

        # Anonymity checkbox
        self.anonymity_checkbox = QCheckBox("Enable anonymity (blur geolocation)", self)
        self.anonymity_checkbox.stateChanged.connect(self.toggle_radius_dropdown)  # Connect checkbox to toggle function
        self.layout.addWidget(self.anonymity_checkbox)

        # Horizontal layout for the radius label and dropdown
        radius_layout = QHBoxLayout()
        self.radius_label = QLabel("Select blur radius (in meters):", self)
        radius_layout.addWidget(self.radius_label)

        self.radius_dropdown = QComboBox(self)
        # Adding radius options (100m default, then +50m increments)
        self.radius_options = [f"{i} meters" for i in range(100, 501, 50)]
        self.radius_dropdown.addItems(self.radius_options)
        self.radius_dropdown.setCurrentIndex(0)  # Default to 100 meters
        self.radius_dropdown.setFixedWidth(100)  # Set fixed width for the dropdown
        radius_layout.addWidget(self.radius_dropdown)

        self.layout.addLayout(radius_layout)  # Add the horizontal layout to the main layout

        # Initially disable the dropdown, will be enabled if the checkbox is checked
        self.radius_label.setEnabled(False)
        self.radius_dropdown.setEnabled(False)

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
            # Extract only the file name and extension
            file_name = os.path.basename(file_path)
            self.csv_file_path = file_path
            self.csv_label.setText(f"CSV File: {file_name}")
            self.generate_button.setEnabled(True)

    def select_output_file(self):
        # Get the user's Downloads folder path
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Prompt the user to select the output file name and directory, defaulting to Downloads folder
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save KML File", downloads_path, "KML Files (*.kml)", options=options)
        return file_path

    def toggle_radius_dropdown(self, state):
        """
        Enable or disable the radius dropdown based on the checkbox state.
        """
        if state == Qt.Checked:
            self.radius_label.setEnabled(True)
            self.radius_dropdown.setEnabled(True)
        else:
            self.radius_label.setEnabled(False)
            self.radius_dropdown.setEnabled(False)

    def generate_kml(self):
        # Ensure a CSV file is selected before starting
        if not self.csv_file_path:
            QMessageBox.critical(self, "Error", "Please select a CSV file.")
            return

        # Ensure API key is entered
        self.api_key = self.api_key_input.text()
        if not self.api_key:
            QMessageBox.critical(self, "Error", "Please enter a Google API key.")
            return

        # Select output file
        self.output_file_path = self.select_output_file()
        if not self.output_file_path:
            QMessageBox.critical(self, "Error", "Please select a location to save the KML file.")
            return

        # Get the anonymity and radius values
        anonymity_enabled = self.anonymity_checkbox.isChecked()
        selected_radius = int(self.radius_dropdown.currentText().split()[0])  # Get the radius value in meters

        # Disable button and start background processing
        self.generate_button.setEnabled(False)
        
        # Pass csv_file_path, api_key, output_file_path, anonymity flag, and radius to the Worker class
        self.worker = Worker(self.csv_file_path, self.api_key, self.output_file_path, anonymity_enabled, selected_radius)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.task_completed.connect(self.on_task_completed)
        self.worker.start()

    def update_progress(self, progress_value):
        self.progress.setValue(progress_value)

    def on_task_completed(self, result):
        if "Error" in result:
            print(f"Error: {result}")
        else:
            print(f"KML file created: {result}")
        self.progress.setValue(0)
        self.generate_button.setEnabled(True)
        
        # Play a sound when the task is complete
        winsound.Beep(1000, 500)  # Frequency in Hz, duration in milliseconds