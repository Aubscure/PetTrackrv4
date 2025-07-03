import subprocess
import sys
import os

# Path to requirements.txt
REQUIREMENTS_PATH = os.path.join(os.path.dirname(__file__), "requirements.txt")

def install_requirements():
    """Install required packages from requirements.txt."""
    try:
        print("📦 Checking and installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_PATH])
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        sys.exit(1)

def run_pettrackr():
    """Launch the PetTrackr application."""
    from frontend.gui import launch_gui

    print("🐾 Starting PetTrackr...")
    launch_gui()

if __name__ == "__main__":
    install_requirements()
    run_pettrackr()