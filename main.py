import sys
import os
import platform
import subprocess
from PyQt5.QtWidgets import QApplication
from ui import MainWindow

# Define the necessary packages for PyQt5 to run on Linux
required_packages = [
    "libxcb-xinerama0",
    "libfontconfig1",
    "libxcb-icccm4",
    "libxcb-image0",
    "libxcb-keysyms1",
    "libxcb-randr0",
    "libxcb-render0",
    "libxcb-render-util0",
    "libxcb-shape0",
    "libxcb-sync1",
    "libxcb-xfixes0",
    "libxcb-dri3-0",
    "libxcb-util1",
    "libglib2.0-dev",  # Required for GThread
    "libgl1",          # Required for rendering (libGL.so.1)
    "libgl1-mesa-dri", # DRI drivers for OpenGL
    "libgl1-mesa-glx", # Mesa GLX for OpenGL
    "sox"              # For sound notifications
]

def is_linux():
    """Check if the current platform is Linux."""
    return platform.system() == "Linux"

def is_package_installed(package_name):
    """Check if a package is installed using dpkg."""
    try:
        result = subprocess.run(['dpkg', '-s', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False

def install_missing_packages(packages):
    """Install missing packages using apt-get."""
    missing_packages = [pkg for pkg in packages if not is_package_installed(pkg)]
    if missing_packages:
        try:
            # Run installation command, suppress output and errors
            subprocess.run(f"sudo apt-get install -y {' '.join(missing_packages)}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            # Handle any error silently
            pass

def check_and_install_dependencies():
    """Check and install dependencies if running on Linux."""
    if is_linux():
        try:
            install_missing_packages(required_packages)
            # After installation, run ldconfig to update the library cache silently
            subprocess.run("sudo ldconfig", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            # Handle any error silently
            pass

# Main entry point for the application
if __name__ == "__main__":
    # Check and install dependencies on Linux before launching the PyQt5 application
    check_and_install_dependencies()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())