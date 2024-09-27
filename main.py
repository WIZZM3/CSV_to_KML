import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow

# Main entry point for the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())