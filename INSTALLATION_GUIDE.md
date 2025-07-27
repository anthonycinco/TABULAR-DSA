# RF Learning System - Complete Installation Guide

This guide provides comprehensive installation instructions for the RF Learning System across all supported platforms.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Platform-Specific Installation](#platform-specific-installation)
3. [Verification and Testing](#verification-and-testing)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)
6. [Quick Start](#quick-start)

## System Requirements

### Minimum Requirements
- **Operating System**: Ubuntu 20.04+, Windows 10+ (with WSL2), or macOS 10.15+
- **Python**: 3.7+ (3.8+ recommended)
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 10GB free disk space
- **Network**: Internet connection for package installation

### Recommended Requirements
- **Operating System**: Ubuntu 22.04 LTS
- **Python**: 3.9+ or 3.10+
- **Memory**: 16GB RAM
- **Storage**: 20GB free disk space
- **Hardware**: USRP1 SDR (for real RF sensing)

## Platform-Specific Installation

### Ubuntu/Debian Linux (Recommended)

#### Step 1: System Preparation
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential build tools
sudo apt install -y build-essential cmake git wget curl pkg-config

# Install Python and development tools
sudo apt install -y python3 python3-pip python3-dev python3-venv

# Install Qt dependencies (required for GNU Radio)
sudo apt install -y qt5-default qtcreator python3-pyqt5

# Install additional system dependencies
sudo apt install -y libboost-all-dev libcppunit-dev swig doxygen liblog4cpp5-dev
sudo apt install -y libusb-1.0-0-dev libudev-dev libfftw3-dev
```

#### Step 2: Install GNU Radio and UHD
```bash
# Add GNU Radio PPA for latest stable version
sudo add-apt-repository ppa:gnuradio/gnuradio-releases -y
sudo apt update

# Install GNU Radio with UHD support
sudo apt install -y gnuradio gnuradio-dev uhd-host uhd-dev

# Install additional GNU Radio modules
sudo apt install -y gr-osmosdr gr-fosphor gr-uhd

# Verify installation
gnuradio-companion --version
uhd_usrp_probe
```

#### Step 3: Install NS3 (Optional but Recommended)
```bash
# Install NS3 dependencies
sudo apt install -y libsqlite3-dev libboost-all-dev libssl-dev
sudo apt install -y libxml2-dev libgtk-3-dev libgsl-dev

# Download and install NS3
cd /tmp
wget https://www.nsnam.org/releases/ns-allinone-3.37.tar.bz2
tar xjf ns-allinone-3.37.tar.bz2
cd ns-allinone-3.37

# Build NS3 with all modules
./build.py --enable-examples --enable-tests --enable-modules=core,network,internet,wifi,spectrum

# Add NS3 to PATH permanently
echo 'export PATH=$PATH:/tmp/ns-allinone-3.37/ns-3.37' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/tmp/ns-allinone-3.37/ns-3.37' >> ~/.bashrc
source ~/.bashrc

# Verify NS3 installation
ns3 --version
```

#### Step 4: Install Python Dependencies
```bash
# Create virtual environment (recommended)
python3 -m venv rf_learning_env
source rf_learning_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install core dependencies
pip install -r requirements.txt

# Install additional development packages
pip install jupyter notebook ipython pytest

# Install optional packages for enhanced functionality
pip install scikit-learn tensorflow torch  # For advanced ML features
pip install plotly dash  # For interactive visualizations
```

### macOS

#### Step 1: Install Homebrew
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add Homebrew to PATH (if needed)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

#### Step 2: Install System Dependencies
```bash
# Install dependencies
brew install cmake git python3 qt5 boost fftw

# Install GNU Radio and UHD
brew install gnuradio uhd

# Install NS3 (optional)
brew install ns3
```

#### Step 3: Install Python Dependencies
```bash
# Create virtual environment
python3 -m venv rf_learning_env
source rf_learning_env/bin/activate

# Install packages
pip install -r requirements.txt
pip install jupyter notebook ipython pytest
```

### Windows

#### Option A: Windows with WSL2 (Recommended)

##### Step 1: Install WSL2
```powershell
# Open PowerShell as Administrator and run:
wsl --install -d Ubuntu

# Restart your computer when prompted
# After restart, complete Ubuntu setup with username and password
```

##### Step 2: Follow Ubuntu Installation Steps
Within WSL2 Ubuntu, follow the Ubuntu installation steps above.

#### Option B: Windows Native (Simulation Only)

##### Step 1: Install Python
1. Download Python 3.9+ from https://www.python.org/downloads/
2. Install with "Add Python to PATH" option checked
3. Verify installation: `python --version`

##### Step 2: Install Dependencies
```cmd
# Open Command Prompt and run:
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install jupyter notebook ipython pytest
```

##### Step 3: Create Virtual Environment
```cmd
python -m venv rf_learning_env
rf_learning_env\Scripts\activate
```

## Verification and Testing

### Step 1: Clone and Setup Repository
```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd TABULAR-DSA

# Run automated setup
python setup.py  # For Linux/macOS
python setup_windows.py  # For Windows
```

### Step 2: Run System Tests
```bash
# Test basic functionality
python test_system.py

# Test NS3 integration
python test_ns3_integration.py

# Expected output: All tests passed
```

### Step 3: Test Simulation Mode
```bash
# Run basic simulation
python main_system.py --simulate --episodes 50

# Expected output: Learning progress and final statistics
```

## Configuration

### Step 1: Environment Configuration
Edit `config.py` to match your environment:

```python
# USRP Settings (for real hardware)
USRP_DEVICE = "addr=192.168.10.2"  # Your USRP IP address
USRP_GAIN = 20                     # Adjust based on signal strength
CENTER_FREQUENCY = 2.44e9          # 2.44 GHz

# RF Environment
POWER_THRESHOLD = -60              # Adjust for your environment
# For noisy environments: -50 to -40
# For quiet environments: -70 to -80

# Learning Parameters
LEARNING_RATE = 0.1                # 0.01 to 0.3
EPSILON_DECAY = 0.995              # 0.99 to 0.999
MIN_EPSILON = 0.01                 # 0.001 to 0.1
```

### Step 2: Hardware Setup (For Real USRP Operation)

#### Connect USRP1 SDR
1. **Physical Connection:**
   - Connect USRP1 via USB cable
   - Ensure antenna is attached to RF port
   - Power on USRP1 (if external power required)

2. **Verify USRP1 Detection:**
   ```bash
   # Check if USRP1 is detected
   uhd_usrp_probe
   
   # Expected output should show device information
   # If not detected, try:
   sudo uhd_usrp_probe
   ```

3. **Configure Network (if using network connection):**
   ```bash
   # Set static IP for USRP1
   sudo ifconfig eth0 192.168.10.1 netmask 255.255.255.0
   
   # Test connectivity
   ping 192.168.10.2
   ```

## Troubleshooting

### Common Issues and Solutions

#### USRP1 Not Detected
```bash
# Check USB connection
lsusb | grep Ettus

# Check UHD installation
uhd_usrp_probe

# If not detected, try:
sudo uhd_usrp_probe

# Add user to usb group
sudo usermod -a -G usb $USER
sudo reboot
```

#### GNU Radio Not Starting
```bash
# Check GNU Radio installation
gnuradio-companion --version

# Reinstall if needed
sudo apt remove gnuradio
sudo apt install gnuradio

# Check Qt dependencies
sudo apt install qt5-default python3-pyqt5
```

#### Permission Issues
```bash
# Add user to usb group
sudo usermod -a -G usb $USER

# Reboot or logout/login
sudo reboot
```

#### NS3 Not Found
```bash
# Check NS3 installation
ns3 --version

# If not found, reinstall:
cd /tmp/ns-allinone-3.37
./build.py --enable-examples
```

#### Python Package Issues
```bash
# Upgrade pip
pip install --upgrade pip

# Install packages individually
pip install numpy matplotlib pandas scipy seaborn

# Check for conflicts
pip check
```

#### Windows-Specific Issues

##### WSL2 Not Working
```powershell
# Enable WSL feature
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Enable Virtual Machine feature
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart computer
# Install WSL2
wsl --install -d Ubuntu
```

##### Python Path Issues
```cmd
# Check Python installation
python --version
pip --version

# If not found, reinstall Python with "Add to PATH" option
```

### Performance Tuning

#### Adjust Power Threshold
```python
# In config.py, adjust based on your environment:
POWER_THRESHOLD = -60  # Default
# For noisy environments: -50 to -40
# For quiet environments: -70 to -80
```

#### Optimize Learning Parameters
```python
# In config.py, adjust learning parameters:
LEARNING_RATE = 0.1      # 0.01 to 0.3
EPSILON_DECAY = 0.995    # 0.99 to 0.999
MIN_EPSILON = 0.01       # 0.001 to 0.1
```

#### USRP Gain Settings
```python
# In config.py, adjust USRP gain:
USRP_GAIN = 20  # 10 to 50 dB
# Higher gain = more sensitive to weak signals
# Lower gain = less interference from strong signals
```

## Quick Start

### Step 1: Basic Testing
```bash
# Verify installation
python test_system.py
python test_ns3_integration.py

# Expected output: All tests passed
```

### Step 2: Run Simulation
```bash
# Basic simulation (no hardware required)
python main_system.py --simulate --episodes 100

# NS3 simulation (realistic network conditions)
python main_system.py --ns3 --episodes 100

# Load pre-trained model
python main_system.py --load-qtable --episodes 100
```

### Step 3: Real USRP Operation
```bash
# Terminal 1: Start GNU Radio
gnuradio-companion rf_sensing.grc

# Terminal 2: Run learning system
python main_system.py
```

### Step 4: Monitor Performance
- **Real-time Dashboard**: 6-panel performance plots
- **Console Output**: Episode statistics every 100 episodes
- **Log Files**: Detailed logs in `system_log.txt`
- **Final Results**: Performance plots and heatmaps

## Expected Performance

### Learning Progress
- **Episodes 1-50**: Random exploration (epsilon ≈ 1.0)
- **Episodes 50-200**: Learning phase (epsilon decreasing)
- **Episodes 200+**: Exploitation phase (epsilon ≈ 0.01)

### Success Metrics
- Q-agent should outperform random agent by 10-20%
- Collision rate should decrease over time
- Success rate should increase to 70-90%

## Support

- **Documentation**: README.md, QUICK_SETUP.md, SYSTEM_SUMMARY.md
- **Logs**: Check `system_log.txt` for detailed error messages
- **Tests**: Run `python test_system.py` to verify installation
- **Configuration**: Edit `config.py` for environment-specific settings

## Next Steps

After successful installation:

1. **Experiment with Parameters**: Adjust learning rates and thresholds
2. **Test Different Scenarios**: Try various RF environments
3. **Extend Functionality**: Add new features or modify existing ones
4. **Real Hardware Testing**: Connect USRP1 for actual RF sensing
5. **Performance Analysis**: Run longer experiments and analyze results

The system is now ready for research, education, and practical RF applications! 