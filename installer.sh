#!/bin/bash

read -p "Do you wish to install anaconda? Please take note that if you already have an anaconda installation, it will be overwritten. (yes/no): " INSTALL_CHOICE

while [[ "$INSTALL_CHOICE" != "yes" ]] && [[ "$INSTALL_CHOICE" != "no" ]]; then
    read -p "Error, you must select one of the two corresponding options (yes/no): " INSTALL_CHOICE
done

if [[ "$INSTALL_CHOICE" == "yes" ]]; then
    echo "Starting installation..."
    # Download and install Anaconda, based on the October 2024 version
    ANACONDA_LOCATION="Anaconda3-2024.10-1-Linux-x86_64.sh"
    wget https://repo.anaconda.com/archive/$ANACONDA_INSTALLER
    bash $ANACONDA_INSTALLER -b -p $HOME/anaconda3
    source ~/.bashrc
    conda init

else;
    echo "Anaconda installation skipped."
fi

if command -v conda &> /dev/null; then
    echo "Anaconda has been successfully found."
else
    echo "Anaconda is not installed. You must install anaconda before continuing the installation process."
    exit 1
fi


# Create and enter a new conda environment
conda create -n fastapi_env python=3.11 -y
conda activate fastapi_env

# Install FastAPI
pip install -r installFiles/requirements.txt

echo "The environnement was successfully created, and with the required packages."
echo "You can restart the anaconda environement at any time by running 'conda activate fastapi_env'"
