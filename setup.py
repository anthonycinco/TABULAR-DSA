#!/usr/bin/env python3
"""
RF Learning System Setup Script
Automated installation and configuration for the RF Learning System
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

def detect_platform():
    """Detect the operating system and return platform info"""
    system = platform.system().lower()
    if system == "linux":
        # Try to detect specific Linux distribution
        try:
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                if "ubuntu" in content:
                    return "ubuntu"
                elif "debian" in content:
                    return "debian"
                else:
                    return "linux"
        except:
            return "linux"
    elif system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    else:
        return "unknown"

def install_system_dependencies(platform_type):
    """Install system dependencies based on platform"""
    print("Installing system dependencies for {}...".format(platform_type))
    
    if platform_type in ["ubuntu", "debian", "linux"]:
        commands = [
            "sudo apt update",
            "sudo apt install -y build-essential cmake git wget curl pkg-config",
            "sudo apt install -y python3 python3-pip python3-dev python3-venv",
            "sudo apt install -y qt5-default qtcreator python3-pyqt5",
            "sudo apt install -y libboost-all-dev libcppunit-dev swig doxygen liblog4cpp5-dev",
            "sudo apt install -y libusb-1.0-0-dev libudev-dev libfftw3-dev"
        ]
        
        for cmd in commands:
            print("Running: {}".format(cmd))
            success, _, error = run_command(cmd, check=False, capture_output=True)
            if not success:
                print("Warning: Command failed: {}".format(error))
                print("You may need to install dependencies manually.")
    
    elif platform_type == "macos":
        # Check if Homebrew is installed
        if not shutil.which("brew"):
            print("Installing Homebrew...")
            install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            run_command(install_cmd)
        
        commands = [
            "brew install cmake git python3 qt5 boost fftw",
            "brew install gnuradio uhd"
        ]
        
        for cmd in commands:
            print("Running: {}".format(cmd))
            success, _, error = run_command(cmd, check=False, capture_output=True)
            if not success:
                print("Warning: Command failed: {}".format(error))
    
    elif platform_type == "windows":
        print("Windows detected. Please install dependencies manually:")
        print("1. Install WSL2: wsl --install -d Ubuntu")
        print("2. Follow Ubuntu installation steps within WSL2")
        print("3. Install Python packages: pip install -r requirements.txt")
        return False
    
    return True

def install_gnuradio(platform_type):
    """Install GNU Radio and UHD"""
    print("Installing GNU Radio and UHD...")
    
    if platform_type in ["ubuntu", "debian", "linux"]:
        commands = [
            "sudo add-apt-repository ppa:gnuradio/gnuradio-releases -y",
            "sudo apt update",
            "sudo apt install -y gnuradio gnuradio-dev uhd-host uhd-dev",
            "sudo apt install -y gr-osmosdr gr-fosphor gr-uhd"
        ]
        
        for cmd in commands:
            print("Running: {}".format(cmd))
            success, _, error = run_command(cmd, check=False, capture_output=True)
            if not success:
                print("Warning: Command failed: {}".format(error))
    
    elif platform_type == "macos":
        # Already installed in system dependencies
        pass
    
    # Verify installation
    success, output, _ = run_command("gnuradio-companion --version", 
                                   check=False, capture_output=True)
    if success:
        print("GNU Radio installation verified: {}".format(output.strip()))
    else:
        print("Warning: GNU Radio installation verification failed")
    
    success, output, _ = run_command("uhd_usrp_probe", 
                                   check=False, capture_output=True)
    if success:
        print("UHD installation verified")
    else:
        print("Warning: UHD installation verification failed")

def install_ns3(platform_type):
    """Install NS3 (optional)"""
    print("Installing NS3 (optional)...")
    
    if platform_type in ["ubuntu", "debian", "linux"]:
        commands = [
            "sudo apt install -y libsqlite3-dev libboost-all-dev libssl-dev",
            "sudo apt install -y libxml2-dev libgtk-3-dev libgsl-dev",
            "cd /tmp && wget https://www.nsnam.org/releases/ns-allinone-3.37.tar.bz2",
            "cd /tmp && tar xjf ns-allinone-3.37.tar.bz2",
            "cd /tmp/ns-allinone-3.37 && ./build.py --enable-examples --enable-tests --enable-modules=core,network,internet,wifi,spectrum"
        ]
        
        for cmd in commands:
            print("Running: {}".format(cmd))
            success, _, error = run_command(cmd, check=False, capture_output=True)
            if not success:
                print("Warning: NS3 installation failed: {}".format(error))
                print("NS3 is optional - continuing without it...")
                return False
        
        # Add to PATH
        path_cmd = 'echo \'export PATH=$PATH:/tmp/ns-allinone-3.37/ns-3.37\' >> ~/.bashrc'
        run_command(path_cmd)
        print("NS3 added to PATH. Please restart your terminal or run: source ~/.bashrc")
    
    elif platform_type == "macos":
        success, _, error = run_command("brew install ns3", 
                                       check=False, capture_output=True)
        if not success:
            print("Warning: NS3 installation failed: {}".format(error))
            return False
    
    # Verify NS3 installation
    success, output, _ = run_command("ns3 --version", 
                                   check=False, capture_output=True)
    if success:
        print("NS3 installation verified: {}".format(output.strip()))
        return True
    else:
        print("NS3 installation verification failed - continuing without NS3")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    
    # Upgrade pip
    run_command("pip install --upgrade pip")
    
    # Install core requirements
    if os.path.exists("requirements.txt"):
        success, _, error = run_command("pip install -r requirements.txt", 
                                       check=False, capture_output=True)
        if not success:
            print("Error installing requirements: {}".format(error))
            return False
    else:
        # Install packages individually if requirements.txt doesn't exist
        packages = ["numpy>=1.21.0", "matplotlib>=3.5.0", "pandas>=1.3.0", 
                   "scipy>=1.7.0", "seaborn>=0.11.0"]
        for package in packages:
            success, _, error = run_command("pip install {}".format(package), 
                                           check=False, capture_output=True)
            if not success:
                print("Warning: Failed to install {}: {}".format(package, error))
    
    # Install additional development packages
    dev_packages = ["jupyter", "notebook", "ipython", "pytest"]
    for package in dev_packages:
        success, _, error = run_command("pip install {}".format(package), 
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
        success, _, error = run_command("python3 -m venv {}".format(venv_name), 
                                       check=False, capture_output=True)
        if success:
            print("Virtual environment created: {}".format(venv_name))
            print("To activate: source {}/bin/activate".format(venv_name))
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

def main():
    """Main setup function"""
    print("=" * 60)
    print("RF Learning System Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Detect platform
    platform_type = detect_platform()
    print("Detected platform: {}".format(platform_type))
    
    if platform_type == "unknown":
        print("ERROR: Unsupported platform")
        sys.exit(1)
    
    # Install system dependencies
    if not install_system_dependencies(platform_type):
        print("System dependency installation failed")
        sys.exit(1)
    
    # Install GNU Radio
    install_gnuradio(platform_type)
    
    # Install NS3 (optional)
    ns3_installed = install_ns3(platform_type)
    
    # Create virtual environment
    create_virtual_environment()
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("Python dependency installation failed")
        sys.exit(1)
    
    # Create configuration template
    create_config_template()
    
    # Run tests
    tests_passed = run_tests()
    
    print("\n" + "=" * 60)
    print("Setup Summary")
    print("=" * 60)
    print("Platform: {}".format(platform_type))
    print("GNU Radio: Installed")
    print("NS3: {}".format("Installed" if ns3_installed else "Not installed (optional)"))
    print("Python Dependencies: Installed")
    print("Tests: {}".format("Passed" if tests_passed else "Failed"))
    
    if tests_passed:
        print("\nSetup completed successfully!")
        print("\nNext steps:")
        print("1. Activate virtual environment: source rf_learning_env/bin/activate")
        print("2. Run simulation: python main_system.py --simulate --episodes 50")
        print("3. Check documentation: README.md")
    else:
        print("\nSetup completed with warnings. Some tests failed.")
        print("Please check the error messages above and install missing dependencies.")
    
    print("\nFor detailed usage instructions, see README.md")

if __name__ == "__main__":
    main() 