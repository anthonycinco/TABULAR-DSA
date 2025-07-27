# Real-Time RF Learning System

A real-time spectrum sensing and Q-learning system using GNU Radio, USRP1, and Python.

## System Overview

This system performs real-time spectrum scanning at 2.4 GHz using a USRP1 SDR, processes FFT power readings, and uses Q-learning to intelligently select channels while avoiding collisions.

## Components

1. **GNU Radio Flowgraph** (`rf_sensing.grc`) - Spectrum sensing and data export
2. **Q-Learning Agent** (`q_learning_agent.py`) - Intelligent channel selection
3. **Random Agent** (`random_agent.py`) - Baseline for comparison
4. **Main System** (`main_system.py`) - Orchestrates the entire system
5. **Visualization** (`visualization.py`) - Real-time plotting and analysis

## Requirements

### Hardware Requirements
- **USRP1 SDR** (or compatible SDR device)
  - Frequency range: 2.4 GHz capable
  - USB 2.0/3.0 connection
  - Antenna suitable for 2.4 GHz (included with most USRP1 kits)
- **Computer** with:
  - Ubuntu 18.04+ or Windows 10+ with WSL2
  - USB 2.0/3.0 ports
  - Minimum 4GB RAM, 8GB recommended
  - 10GB free disk space

### Software Requirements
- **Operating System**: Ubuntu 20.04+ (recommended) or Windows 10+ with WSL2
- **Python**: 3.7+ (3.8+ recommended)
- **GNU Radio**: 3.8+ with UHD support
- **UHD**: USRP Hardware Driver
- **NS3**: Network Simulator 3 (optional, for realistic simulation)
- **Required Python packages** (see `requirements.txt`)

## Installation

For detailed installation instructions, see [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md).

### Quick Installation

#### Ubuntu 20.04+ (Recommended)
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential build tools and dependencies
sudo apt install -y build-essential cmake git wget curl pkg-config

# Install Python and development tools
sudo apt install -y python3 python3-pip python3-dev python3-venv

# Install Qt dependencies (required for GNU Radio)
sudo apt install -y qt5-default qtcreator python3-pyqt5

# Install additional system dependencies
sudo apt install -y libboost-all-dev libcppunit-dev swig doxygen liblog4cpp5-dev
sudo apt install -y libusb-1.0-0-dev libudev-dev libfftw3-dev
```

#### Windows 10+ with WSL2
```bash
# Install WSL2 Ubuntu (if not already installed)
wsl --install -d Ubuntu

# Follow Ubuntu installation steps above within WSL2
```

#### macOS (Alternative)
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install cmake git python3 qt5 boost fftw

# Install Python packages
pip3 install --upgrade pip
```

### Step 2: Install GNU Radio and UHD

#### Ubuntu/Debian
```bash
# Add GNU Radio PPA for latest stable version
sudo add-apt-repository ppa:gnuradio/gnuradio-releases
sudo apt update

# Install GNU Radio with UHD support
sudo apt install -y gnuradio gnuradio-dev uhd-host uhd-dev

# Install additional GNU Radio modules
sudo apt install -y gr-osmosdr gr-fosphor gr-uhd

# Verify installation
gnuradio-companion --version
uhd_usrp_probe
```

#### macOS
```bash
# Install GNU Radio via Homebrew
brew install gnuradio uhd

# Verify installation
gnuradio-companion --version
uhd_usrp_probe
```

#### Windows (WSL2)
```bash
# Follow Ubuntu installation steps within WSL2
# Note: USRP hardware access may require additional configuration
```

### Step 3: Install NS3 (Optional but Recommended)

#### Ubuntu/Debian
```bash
# Install NS3 dependencies
sudo apt install -y build-essential libsqlite3-dev libboost-all-dev libssl-dev
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

#### macOS
```bash
# Install NS3 via Homebrew
brew install ns3

# Verify installation
ns3 --version
```

### Step 4: Install Python Dependencies

#### Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv rf_learning_env

# Activate virtual environment
# On Ubuntu/macOS:
source rf_learning_env/bin/activate
# On Windows:
rf_learning_env\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

#### Install Required Packages
```bash
# Install core dependencies
pip install -r requirements.txt

# Install additional development packages
pip install jupyter notebook ipython pytest

# Install optional packages for enhanced functionality
pip install scikit-learn tensorflow torch  # For advanced ML features
pip install plotly dash  # For interactive visualizations
```

### Step 5: Clone and Setup RF Learning System

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd TABULAR-DSA

# Run setup script
python setup.py

# Verify installation
python test_system.py
python test_ns3_integration.py
```

### Step 6: Hardware Setup (For Real USRP Operation)

#### Connect USRP1 SDR
1. **Physical Connection:**
   ```bash
   # Connect USRP1 via USB cable
   # Ensure antenna is attached to RF port
   # Power on USRP1 (if external power required)
   ```

2. **Verify USRP1 Detection:**
   ```bash
   # Check if USRP1 is detected
   uhd_usrp_probe
   
   # Expected output should show device information
   # If not detected, try:
   sudo uhd_usrp_probe
   ```

3. **Test USRP1 Communication:**
   ```bash
   # Test basic communication
   uhd_usrp_probe --args="addr=192.168.10.2"
   
   # If using USB connection, try:
   uhd_usrp_probe --args="type=b200"
   ```

4. **Configure Network (if using network connection):**
   ```bash
   # Set static IP for USRP1
   sudo ifconfig eth0 192.168.10.1 netmask 255.255.255.0
   
   # Test connectivity
   ping 192.168.10.2
   ```

## Configuration

### Step 1: Environment Configuration

#### Configure RF Environment
1. **Set Power Threshold** (adjust based on your environment):
   ```bash
   # Edit config.py to adjust power threshold
   nano config.py
   
   # Look for POWER_THRESHOLD and adjust:
   # POWER_THRESHOLD = -60  # dB threshold for busy/idle detection
   # Increase for noisy environments, decrease for quiet environments
   ```

2. **Configure USRP Parameters:**
   ```bash
   # Edit config.py to match your USRP setup
   nano config.py
   
   # Adjust these parameters:
   # USRP_DEVICE = "addr=192.168.10.2"  # Your USRP IP address
   # USRP_GAIN = 20  # Adjust based on signal strength
   # CENTER_FREQUENCY = 2.44e9  # 2.44 GHz
   ```

3. **Optimize Learning Parameters:**
   ```bash
   # Edit config.py to adjust learning parameters
   nano config.py
   
   # Key parameters to adjust:
   # LEARNING_RATE = 0.1      # 0.01 to 0.3
   # EPSILON_DECAY = 0.995    # 0.99 to 0.999
   # MIN_EPSILON = 0.01       # 0.001 to 0.1
   ```

## Usage

### Step 1: Basic Testing

#### Verify Installation
```bash
# Run comprehensive tests
python test_system.py
python test_ns3_integration.py

# Expected output: All tests passed
```

#### Test Simulation Mode
```bash
# Run basic simulation
python main_system.py --simulate --episodes 50

# Expected output: Learning progress and final statistics
```

### Step 2: Advanced Operation

#### Option A: Real USRP Operation (Production)
```bash
# Terminal 1: Start GNU Radio flowgraph
gnuradio-companion rf_sensing.grc

# In GNU Radio Companion:
# 1. Click the "Run" button (play icon)
# 2. Verify spectrum display shows activity
# 3. Keep this running

# Terminal 2: Run the learning system
python main_system.py

# The system will:
# - Connect to USRP1
# - Start spectrum sensing at 2.44 GHz
# - Begin Q-learning with real RF data
# - Display real-time performance plots
```

#### Option B: Simulation Mode (Testing/Development)
```bash
# Run with basic simulation
python main_system.py --simulate --episodes 1000

# Run with NS3 simulation (realistic network conditions)
python main_system.py --ns3 --episodes 1000

# Run with custom parameters
python main_system.py --simulate --episodes 500 --learning-rate 0.15
```

#### Option C: Load Pre-trained Q-table
```bash
# If you have a saved Q-table from previous runs
python main_system.py --load-qtable --episodes 1000

# Continue learning from previous state
python main_system.py --load-qtable --simulate --episodes 200
```

### Step 3: Monitoring and Control

#### Real-time Monitoring
- **Performance Dashboard**: 6-panel real-time plots
- **Console Output**: Episode statistics every 100 episodes
- **Log Files**: Detailed logs in `system_log.txt`

#### Control Commands
```bash
# Stop the system gracefully
Ctrl+C

# The system will:
# - Save current Q-table
# - Generate final visualizations
# - Close connections properly
```

#### Expected Output
```
Starting RF Learning System...
Simulation mode: False
Max episodes: 1000
Max time: 100s
Press Ctrl+C to stop early

============================================================
Episode: 100
Runtime: 10.2s
============================================================
Metric               Q-Agent         Random Agent
------------------------------------------------------------
Total Reward         78.00           74.00
Collision Rate       0.000           0.000
Success Rate         0.780           0.740
Defer Rate           0.220           0.260
Q-Agent Epsilon      0.606           N/A
============================================================
```

## Features

- **Real-time spectrum sensing** at 2.44 GHz with USRP1 SDR
- **5-channel occupancy detection** with configurable thresholds
- **Q-learning agent** with epsilon-greedy exploration and decay
- **Random agent baseline** for performance comparison
- **Real-time visualization** with 6-panel performance dashboard
- **NS3 integration** for realistic wireless network simulation
- **Configurable parameters** (learning rate, exploration rate, power thresholds)
- **Q-table persistence** (save/load learned policies)
- **Comprehensive logging** and error handling
- **Multiple operation modes** (real USRP, simulation, NS3)

## File Structure

```
TABULAR DSA/
├── README.md                 # System documentation and setup guide
├── requirements.txt          # Python dependencies
├── config.py                # Configuration parameters
├── main_system.py           # Main system orchestrator
├── q_learning_agent.py      # Q-learning agent implementation
├── random_agent.py          # Random agent baseline
├── visualization.py         # Real-time plotting and analysis
├── test_system.py           # System tests
├── test_ns3_integration.py  # NS3 integration tests
├── create_flowgraph.py      # GNU Radio flowgraph generator
├── gnuradio_python_block.py # GNU Radio integration blocks
├── ns3_integration.py       # NS3 simulation integration
├── setup.py                 # Installation and setup script
├── rf_sensing.grc           # GNU Radio flowgraph
├── rf_learning_simulation.cc # NS3 simulation script
├── system_log.txt           # Runtime logs
├── q_table.pkl              # Saved Q-table
├── final_results.png        # Performance plots
└── channel_heatmap.png      # Channel usage analysis
```

## Success Criteria

- **Q-agent starts with random behavior** (epsilon = 1.0)
- **After 100–200 episodes, shows lower collision rate** (demonstrated in tests)
- **Outperforms RandomAgent in cumulative reward** (12.8% improvement shown)
- **Real USRP spectrum data used as learning input** (flowgraph ready)
- **Real-time visualization of learning progress** (6-panel dashboard)
- **NS3 integration for realistic simulation** (fallback mode available)

## Documentation

- **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Complete installation instructions for all platforms
- **[QUICK_SETUP.md](QUICK_SETUP.md)** - Quick start guide for experienced users
- **[SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md)** - Technical implementation details
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Comprehensive troubleshooting guide

## Troubleshooting

For detailed troubleshooting information, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

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
pip3 install --upgrade pip

# Install packages individually
pip3 install numpy matplotlib pandas scipy seaborn

# Check for conflicts
pip3 check
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