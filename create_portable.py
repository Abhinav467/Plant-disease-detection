import os
import subprocess

def create_portable():
    """Create portable executable"""
    
    # Install PyInstaller
    subprocess.run(["pip", "install", "pyinstaller"])
    
    # Create executable
    cmd = [
        "pyinstaller",
        "--onefile",
        "--add-data", "trained_plant_disease_1model.keras;.",
        "--add-data", "trained_plant_disease_1model.h5;.",
        "offline_main.py"
    ]
    
    subprocess.run(cmd)
    print("Portable app created in dist/ folder")

if __name__ == "__main__":
    create_portable()