import sys
from PyQt5.QtWidgets import QApplication
from ui import CSVtoKMZApp

# Main entry point for the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CSVtoKMZApp()
    window.show()
    sys.exit(app.exec_())