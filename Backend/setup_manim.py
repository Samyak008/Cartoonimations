import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible with Manim."""
    print("Checking Python version...")
    if sys.version_info < (3, 7):
        print("Error: Manim requires Python 3.7 or higher")
        sys.exit(1)
    print(f"Using Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def install_dependencies():
    """Install Manim and its dependencies."""
    print("Installing Manim and dependencies...")
    
    # First, upgrade pip
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install Manim
    subprocess.run([sys.executable, "-m", "pip", "install", "manim"])
    
    # Install additional dependencies
    dependencies = [
        "numpy",
        "scipy",
        "matplotlib",
        "tqdm",
        "pycairo",
        "pygments",
        "colour",
        "networkx",
        "pillow"
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        subprocess.run([sys.executable, "-m", "pip", "install", dep])
    
    # Install FFmpeg if needed
    check_ffmpeg()
    
    print("\nAll dependencies installed!")

def check_ffmpeg():
    """Check if FFmpeg is installed and available."""
    print("Checking for FFmpeg...")
    try:
        # Try to run ffmpeg -version
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, 
                              text=True)
        
        print("FFmpeg is installed and available.")
        print(f"FFmpeg version: {result.stdout.splitlines()[0]}")
    except FileNotFoundError:
        print("FFmpeg is not installed or not in PATH.")
        print("Please install FFmpeg manually:")
        
        if platform.system() == "Windows":
            print("  1. Download FFmpeg from https://ffmpeg.org/download.html")
            print("  2. Extract the files to a folder like C:\\ffmpeg")
            print("  3. Add the bin folder (e.g., C:\\ffmpeg\\bin) to your PATH environment variable")
        
        elif platform.system() == "Darwin":  # macOS
            print("  Run: brew install ffmpeg")
        
        elif platform.system() == "Linux":
            print("  Run: sudo apt-get install ffmpeg")

def verify_installation():
    """Verify that Manim is installed correctly."""
    print("\nVerifying Manim installation...")
    
    try:
        # Import manim to check if it's installed correctly
        import manim
        print(f"Manim {manim.__version__} is installed correctly!")
        
        # Check for common Manim dependencies
        import cairo
        print("Cairo is installed correctly!")
        
        import numpy
        print(f"NumPy {numpy.__version__} is installed correctly!")
        
        import matplotlib
        print(f"Matplotlib {matplotlib.__version__} is installed correctly!")
        
        print("\nSetup complete! You're ready to create animations with Manim.")
        return True
    
    except ImportError as e:
        print(f"Error during verification: {e}")
        return False

if __name__ == "__main__":
    print("===== Manim Setup Utility =====")
    check_python_version()
    install_dependencies()
    verify_installation()