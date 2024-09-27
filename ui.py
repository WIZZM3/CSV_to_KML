import os
from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog, QLabel, QMessageBox, QVBoxLayout, QWidget, QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from worker import Worker
import chardet

class CSVtoKMZApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV to KMZ")
        self.setGeometry(300, 300, 500, 300)

        # Set the window icon from the 'ressources/' directory
        icon_path = os.path.join('ressources', 'icon.png')
        self.setWindowIcon(QIcon(icon_path))

        # Labels to show file selections (French)
        self.csv_label = QLabel("Fichier CSV : Non sélectionné", self)
        self.png_label = QLabel("Icône personnalisée (PNG) : Non sélectionné", self)
        self.csv_label.resize(400, 30)
        self.png_label.resize(400, 30)
        
        # Buttons to browse CSV and PNG (French)
        self.csv_button = QPushButton('Parcourir Fichier CSV', self)
        self.csv_button.clicked.connect(self.select_csv_file)
        
        self.png_button = QPushButton('Parcourir Icône Personnalisée (PNG)', self)
        self.png_button.clicked.connect(self.select_png_file)
        
        # Progress bar (French)
        self.progress = QProgressBar(self)
        self.progress.setAlignment(Qt.AlignCenter)
        
        # Validate button (initially disabled, French)
        self.validate_button = QPushButton('Valider et Générer KMZ', self)
        self.validate_button.setEnabled(False)
        self.validate_button.clicked.connect(self.process_files)
        
        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.csv_label)
        layout.addWidget(self.csv_button)
        layout.addWidget(self.png_label)
        layout.addWidget(self.png_button)
        layout.addWidget(self.progress)
        layout.addWidget(self.validate_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Variables to hold file paths
        self.csv_file_path = None
        self.png_file_path = None

    def select_csv_file(self):
        # Open file dialog to select a CSV file
        csv_file, _ = QFileDialog.getOpenFileName(self, "Ouvrir fichier CSV", "", "Fichiers CSV (*.csv)")
        if csv_file:
            encoding = self.detect_encoding(csv_file)  # Detect encoding
            self.csv_file_path = (csv_file, encoding)  # Store both file path and encoding
            self.csv_label.setText(f"Fichier CSV : {csv_file}")
        else:
            self.csv_file_path = None
            self.csv_label.setText("Fichier CSV : Non sélectionné")
        self.check_files_selected()

    def detect_encoding(self, file_path):
        # Detect the encoding of the file
        with open(file_path, 'rb') as file:
            result = chardet.detect(file.read())
        return result['encoding']

    def select_png_file(self):
        # Open file dialog to select a PNG file
        png_file, _ = QFileDialog.getOpenFileName(self, "Ouvrir Icône PNG", "", "Fichiers PNG (*.png)")
        if png_file:
            self.png_file_path = png_file
            self.png_label.setText(f"Icône personnalisée (PNG) : {png_file}")
        else:
            self.png_file_path = None
            self.png_label.setText("Icône personnalisée (PNG) : Non sélectionné")
        self.check_files_selected()

    def check_files_selected(self):
        # Enable validate button if both CSV and PNG files are selected
        if self.csv_file_path and self.png_file_path:
            self.validate_button.setEnabled(True)
        else:
            self.validate_button.setEnabled(False)

    def process_files(self):
        # Ensure both files are selected before processing
        if not self.csv_file_path or not self.png_file_path:
            QMessageBox.critical(self, "Erreur", "Veuillez sélectionner un fichier CSV et une icône PNG.")
            return
        
        # Start background processing in a new thread
        self.worker = Worker(self.csv_file_path[0], self.csv_file_path[1], self.png_file_path)  # Pass encoding to Worker
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.task_completed.connect(self.on_task_completed)
        self.worker.start()

    def update_progress(self, progress_value):
        self.progress.setValue(progress_value)

    def on_task_completed(self, result):
        if "Error" in result:
            QMessageBox.critical(self, "Erreur", result)
        else:
            QMessageBox.information(self, "Succès", f"Fichier KMZ créé : {result}")
        self.progress.setValue(0)