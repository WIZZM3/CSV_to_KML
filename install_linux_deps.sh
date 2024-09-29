#!/bin/bash

# List of required packages
packages=(
    libglib2.0-dev
    libgl1
    libgl1-mesa-dri
    mesa-utils  # Replacing libgl1-mesa-glx with mesa-utils
    sox
    libxcb-xinerama0
    libfontconfig1
    libxcb-icccm4
    libxcb-image0
    libxcb-keysyms1
    libxcb-randr0
    libxcb-render0
    libxcb-render-util0
    libxcb-shape0
    libxcb-sync1
    libxcb-xfixes0
    libxcb-dri3-0
    libxcb-util1
)

# Update the package list to ensure we get the latest versions
echo "Updating package lists..."
sudo apt update -y

# Function to check if a package is installed
is_installed() {
    dpkg -l | grep -q "^ii  $1" 
}

# Loop through the packages and install missing ones
for pkg in "${packages[@]}"; do
    if is_installed "$pkg"; then
        echo "$pkg is already installed."
    else
        echo "Installing missing package: $pkg"
        sudo apt install -y "$pkg"
        if [ $? -ne 0 ]; then
            echo "Failed to install $pkg. Please check your internet connection or package repository."
            exit 1  # Exit the script if installation fails for any package
        fi
    fi
done

# After installation, update the library cache
echo "Updating the library cache..."
sudo ldconfig

echo "All required packages are installed."