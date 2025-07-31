# Quick Setup Guide - Simplified RF Learning System

This guide provides quick setup instructions for the simplified RF learning system focused on simulation and NS3 integration.

## Prerequisites

- Python 3.7+
- pip package manager
- Git (optional, for cloning)

## Installation Steps

### 1. Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 2. Test the System

```bash
# Run the test suite
python test_system.py
```

### 3. Run Basic Simulation

```bash
# Run with default settings (1000 episodes)
python main_system.py
```

## Optional: NS3 Installation

For realistic network simulation, install NS3:

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install build-essential libsqlite3-dev libboost-all-dev libssl-dev
git clone https://gitlab.com/nsnam/ns-3-dev.git
cd ns-3-dev
./ns3 configure --enable-examples --enable-tests
./ns3 build
```

### macOS
```bash
brew install ns3
```

### Windows (WSL2)
```bash
# Use Ubuntu instructions in WSL2
```

## Usage Examples

### Basic Simulation
```bash
python main_system.py --episodes 500
```

### NS3 Simulation
```bash
python main_system.py --ns3 --time 60
```

### Load Existing Q-Table
```bash
python main_system.py --load-qtable
```

## Expected Output

The system will display:
- Real-time performance metrics
- Live visualization plots
- Final results saved as PNG files
- Q-table saved as PKL file

## Troubleshooting

### Import Errors
```bash
pip install -r requirements.txt
```

### NS3 Not Found
- System will automatically fall back to simulated data
- Install NS3 for realistic network simulation

### Visualization Issues
```python
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg'
```

## Next Steps

1. Review `config.py` to adjust parameters
2. Run longer simulations for better learning
3. Experiment with different reward structures
4. Add custom agents or extend NS3 simulation

---

**Note**: This simplified version removes all hardware dependencies for easier deployment and testing. 