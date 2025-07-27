#!/usr/bin/env python3
"""
Setup script for RF Learning System
Installs dependencies and configures the system
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)
    print(f"Python version: {sys.version}")

def install_pip_packages():
    """Install required Python packages"""
    packages = [
        'numpy>=1.21.0',
        'matplotlib>=3.5.0',
        'pandas>=1.3.0',
        'scipy>=1.7.0',
        'seaborn>=0.11.0'
    ]
    
    print("Installing Python packages...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")
            return False
    
    return True

def check_gnuradio():
    """Check if GNU Radio is installed"""
    try:
        import gnuradio
        print("✓ GNU Radio is installed")
        return True
    except ImportError:
        print("✗ GNU Radio is not installed")
        print("  Install with: sudo apt-get install gnuradio")
        return False

def check_usrp():
    """Check if USRP drivers are available"""
    try:
        import uhd
        print("✓ UHD (USRP Hardware Driver) is available")
        return True
    except ImportError:
        print("✗ UHD is not installed")
        print("  Install with: sudo apt-get install libuhd-dev uhd-host")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'data', 'results']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")

def create_config_file():
    """Create a user-specific config file"""
    config_content = '''# User-specific configuration for RF Learning System
# Copy this to config_local.py and modify as needed

# USRP Configuration
USRP_DEVICE = "addr=192.168.10.2"  # Change to your USRP IP address
USRP_GAIN = 20  # Adjust based on your environment

# Learning Parameters
LEARNING_RATE = 0.1
EPSILON_DECAY = 0.995
POWER_THRESHOLD = -60  # Adjust based on your RF environment

# Simulation Parameters
SIMULATION_STEPS = 1000
SIMULATION_DURATION = 100
'''
    
    config_file = 'config_local.py'
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            f.write(config_content)
        print(f"✓ Created {config_file}")
        print("  Edit this file to customize your configuration")

def run_tests():
    """Run system tests"""
    print("\nRunning system tests...")
    try:
        subprocess.check_call([sys.executable, 'test_system.py'])
        print("✓ All tests passed")
        return True
    except subprocess.CalledProcessError:
        print("✗ Some tests failed")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Test the system:")
    print("   python test_system.py")
    print("\n2. Run simulation mode:")
    print("   python main_system.py --simulate --episodes 1000")
    print("\n3. Create GNU Radio flowgraph:")
    print("   python main_system.py --create-flowgraph")
    print("\n4. For real USRP operation:")
    print("   - Connect your USRP1")
    print("   - Open rf_sensing.grc in GNU Radio Companion")
    print("   - Run the flowgraph")
    print("   - In another terminal: python main_system.py")
    print("\n5. Customize configuration:")
    print("   - Edit config_local.py for your specific setup")
    print("\nDocumentation:")
    print("   - README.md: System overview and usage")
    print("   - config.py: Default configuration parameters")

def main():
    """Main setup function"""
    print("RF Learning System Setup")
    print("="*40)
    
    # Check Python version
    check_python_version()
    
    # Install packages
    if not install_pip_packages():
        print("Failed to install packages")
        sys.exit(1)
    
    # Check GNU Radio
    gnuradio_available = check_gnuradio()
    
    # Check USRP
    usrp_available = check_usrp()
    
    # Create directories
    create_directories()
    
    # Create config file
    create_config_file()
    
    # Run tests
    tests_passed = run_tests()
    
    # Print results
    print("\n" + "="*40)
    print("SETUP SUMMARY")
    print("="*40)
    print(f"Python packages: ✓")
    print(f"GNU Radio: {'✓' if gnuradio_available else '✗'}")
    print(f"USRP drivers: {'✓' if usrp_available else '✗'}")
    print(f"Directories: ✓")
    print(f"Configuration: ✓")
    print(f"Tests: {'✓' if tests_passed else '✗'}")
    
    if not gnuradio_available:
        print("\nNote: GNU Radio is not installed.")
        print("You can still run the system in simulation mode.")
    
    if not usrp_available:
        print("\nNote: USRP drivers are not installed.")
        print("You can still run the system in simulation mode.")
    
    print_next_steps()

if __name__ == "__main__":
    main() 