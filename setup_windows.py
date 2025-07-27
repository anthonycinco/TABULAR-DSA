#!/usr/bin/env python3
"""
RF Learning System Setup Script for Windows
Automated installation and configuration for Windows users
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(command, check=True, capture_output=False):
    """Run a shell command and handle errors"""
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, check=check, 
                                  capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(command, shell=True, check=check)
            return result.returncode == 0, "", ""
    except subprocess.CalledProcessError as e:
        return False, "", str(e)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("ERROR: Python 3.7+ is required. Current version: {}.{}".format(
            version.major, version.minor))
        return False
    print("Python version check passed: {}.{}.{}".format(
        version.major, version.minor, version.micro))
    return True

def check_wsl2():
    """Check if WSL2 is installed and enabled"""
    print("Checking WSL2 installation...")
    
    # Check if WSL is available
    success, output, error = run_command("wsl --list --verbose", 
                                       check=False, capture_output=True)
    if success:
        print("WSL detected:")
        print(output)
        return True
    else:
        print("WSL not detected or not properly configured")
        return False

def install_wsl2():
    """Install WSL2 with Ubuntu"""
    print("Installing WSL2 with Ubuntu...")
    
    # Enable WSL feature
    print("Enabling WSL feature...")
    success, _, error = run_command("dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart", 
                                   check=False, capture_output=True)
    if not success:
        print("Warning: Failed to enable WSL feature: {}".format(error))
    
    # Enable Virtual Machine feature
    print("Enabling Virtual Machine feature...")
    success, _, error = run_command("dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart", 
                                   check=False, capture_output=True)
    if not success:
        print("Warning: Failed to enable Virtual Machine feature: {}".format(error))
    
    # Install WSL2
    print("Installing WSL2...")
    success, _, error = run_command("wsl --install -d Ubuntu", 
                                   check=False, capture_output=True)
    if success:
        print("WSL2 installation initiated. Please restart your computer and complete the Ubuntu setup.")
        print("After restart, run this script again to continue with the installation.")
        return True
    else:
        print("WSL2 installation failed: {}".format(error))
        return False

def install_python_dependencies():
    """Install Python dependencies on Windows"""
    print("Installing Python dependencies...")
    
    # Upgrade pip
    run_command("python -m pip install --upgrade pip")
    
    # Install core requirements
    if os.path.exists("requirements.txt"):
        success, _, error = run_command("python -m pip install -r requirements.txt", 
                                       check=False, capture_output=True)
        if not success:
            print("Error installing requirements: {}".format(error))
            return False
    else:
        # Install packages individually if requirements.txt doesn't exist
        packages = ["numpy>=1.21.0", "matplotlib>=3.5.0", "pandas>=1.3.0", 
                   "scipy>=1.7.0", "seaborn>=0.11.0"]
        for package in packages:
            success, _, error = run_command("python -m pip install {}".format(package), 
                                           check=False, capture_output=True)
            if not success:
                print("Warning: Failed to install {}: {}".format(package, error))
    
    # Install additional development packages
    dev_packages = ["jupyter", "notebook", "ipython", "pytest"]
    for package in dev_packages:
        success, _, error = run_command("python -m pip install {}".format(package), 
                                       check=False, capture_output=True)
        if not success:
            print("Warning: Failed to install {}: {}".format(package, error))
    
    print("Python dependencies installation completed")
    return True

def create_virtual_environment():
    """Create and activate virtual environment"""
    print("Creating virtual environment...")
    
    venv_name = "rf_learning_env"
    if not os.path.exists(venv_name):
        success, _, error = run_command("python -m venv {}".format(venv_name), 
                                       check=False, capture_output=True)
        if success:
            print("Virtual environment created: {}".format(venv_name))
            print("To activate: {}\\Scripts\\activate".format(venv_name))
        else:
            print("Warning: Failed to create virtual environment: {}".format(error))
            return False
    else:
        print("Virtual environment already exists: {}".format(venv_name))
    
    return True

def run_tests():
    """Run system tests to verify installation"""
    print("Running system tests...")
    
    tests = [
        ("Basic system test", "python test_system.py"),
        ("NS3 integration test", "python test_ns3_integration.py")
    ]
    
    all_passed = True
    for test_name, test_cmd in tests:
        print("Running {}...".format(test_name))
        success, output, error = run_command(test_cmd, check=False, capture_output=True)
        if success:
            print("{} passed".format(test_name))
        else:
            print("{} failed: {}".format(test_name, error))
            all_passed = False
    
    return all_passed

def create_config_template():
    """Create a configuration template if it doesn't exist"""
    config_file = "config.py"
    if not os.path.exists(config_file):
        print("Creating configuration template...")
        config_template = '''"""
Configuration parameters for the RF Learning System
"""

# RF Sensing Parameters
CENTER_FREQUENCY = 2.44e9  # 2.44 GHz
SAMPLE_RATE = 10e6  # 10 MS/s
NUM_CHANNELS = 5
SENSING_INTERVAL = 0.1  # 100ms
POWER_THRESHOLD = -60  # dB threshold for busy/idle detection

# Q-Learning Parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
INITIAL_EPSILON = 1.0
EPSILON_DECAY = 0.995
MIN_EPSILON = 0.01

# USRP Parameters
USRP_DEVICE = "addr=192.168.10.2"  # Default USRP1 address
USRP_GAIN = 20  # dB
USRP_ANTENNA = "TX/RX"

# Reward Parameters
SUCCESS_REWARD = 1.0
COLLISION_PENALTY = -1.0
DEFER_REWARD = 0.0
'''
        with open(config_file, "w") as f:
            f.write(config_template)
        print("Configuration template created: {}".format(config_file))

def create_windows_batch_file():
    """Create a Windows batch file for easy execution"""
    batch_content = '''@echo off
REM RF Learning System - Windows Launcher
REM This script helps you run the RF Learning System on Windows

echo RF Learning System - Windows Launcher
echo ======================================

REM Check if virtual environment exists
if exist rf_learning_env\\Scripts\\activate.bat (
    echo Activating virtual environment...
    call rf_learning_env\\Scripts\\activate.bat
) else (
    echo Virtual environment not found. Using system Python.
)

echo.
echo Available commands:
echo 1. Test system: python test_system.py
echo 2. Run simulation: python main_system.py --simulate --episodes 50
echo 3. Run NS3 simulation: python main_system.py --ns3 --episodes 100
echo 4. Load pre-trained model: python main_system.py --load-qtable --episodes 100
echo.

set /p choice="Enter your choice (1-4) or press Enter to exit: "

if "%choice%"=="1" (
    python test_system.py
) else if "%choice%"=="2" (
    python main_system.py --simulate --episodes 50
) else if "%choice%"=="3" (
    python main_system.py --ns3 --episodes 100
) else if "%choice%"=="4" (
    python main_system.py --load-qtable --episodes 100
) else (
    echo Exiting...
)

pause
'''
    
    with open("run_rf_learning.bat", "w") as f:
        f.write(batch_content)
    print("Windows launcher created: run_rf_learning.bat")

def main():
    """Main setup function for Windows"""
    print("=" * 60)
    print("RF Learning System Setup - Windows")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if running on Windows
    if platform.system().lower() != "windows":
        print("ERROR: This script is for Windows only")
        sys.exit(1)
    
    print("Windows detected. Setting up RF Learning System...")
    
    # Check WSL2
    wsl2_available = check_wsl2()
    if not wsl2_available:
        print("\nWSL2 is required for full functionality (GNU Radio, USRP support)")
        print("However, you can still run the system in simulation mode.")
        
        install_choice = input("Do you want to install WSL2 now? (y/n): ").lower()
        if install_choice == 'y':
            if install_wsl2():
                print("\nWSL2 installation initiated. Please restart your computer")
                print("and run this script again to complete the setup.")
                return
            else:
                print("WSL2 installation failed. Continuing with Windows-only setup.")
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("Python dependency installation failed")
        sys.exit(1)
    
    # Create virtual environment
    create_virtual_environment()
    
    # Create configuration template
    create_config_template()
    
    # Create Windows batch file
    create_windows_batch_file()
    
    # Run tests
    tests_passed = run_tests()
    
    print("\n" + "=" * 60)
    print("Setup Summary - Windows")
    print("=" * 60)
    print("Platform: Windows")
    print("WSL2: {}".format("Available" if wsl2_available else "Not available"))
    print("Python Dependencies: Installed")
    print("Virtual Environment: Created")
    print("Tests: {}".format("Passed" if tests_passed else "Failed"))
    
    if tests_passed:
        print("\nSetup completed successfully!")
        print("\nNext steps:")
        print("1. For simulation mode (no hardware required):")
        print("   - Double-click run_rf_learning.bat")
        print("   - Or run: python main_system.py --simulate --episodes 50")
        print("\n2. For full functionality with GNU Radio and USRP:")
        print("   - Install WSL2: wsl --install -d Ubuntu")
        print("   - Follow Ubuntu installation steps in README.md")
        print("   - Run the system within WSL2")
        print("\n3. Check documentation: README.md")
    else:
        print("\nSetup completed with warnings. Some tests failed.")
        print("Please check the error messages above and install missing dependencies.")
    
    print("\nFor detailed usage instructions, see README.md")

if __name__ == "__main__":
    main() 