# Troubleshooting Guide - Simplified RF Learning System

This guide provides solutions for common issues encountered with the simplified RF learning system.

## Quick Diagnosis

### 1. Run System Tests
```bash
python test_system.py
```

### 2. Check System Log
```bash
tail -f system_log.txt
```

### 3. Verify Dependencies
```bash
pip list | grep -E "(numpy|matplotlib|seaborn)"
```

## Common Issues and Solutions

### Python Environment Issues

#### Issue: Import Errors
**Symptoms:**
```
ModuleNotFoundError: No module named 'numpy'
```

**Solutions:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install numpy matplotlib seaborn pickle5
```

#### Issue: Python Version Too Old
**Symptoms:**
```
SyntaxError: f-string expressions
```

**Solutions:**
```bash
# Check Python version
python --version

# Install Python 3.7+ if needed
# Ubuntu/Debian:
sudo apt install python3.8 python3.8-pip

# macOS:
brew install python@3.8
```

### Simulation Issues

#### Issue: Simulation Not Starting
**Symptoms:**
```
Error: Cannot start simulation
```

**Solutions:**
1. Check configuration parameters in `config.py`
2. Verify all required parameters are set
3. Run with verbose logging:
   ```bash
   python main_system.py --episodes 10
   ```

#### Issue: Poor Learning Performance
**Symptoms:**
- Q-agent not improving over time
- High collision rates
- Low success rates

**Solutions:**
1. **Adjust Learning Parameters** in `config.py`:
   ```python
   LEARNING_RATE = 0.15      # Increase from 0.1
   EPSILON_DECAY = 0.99      # Slower decay
   MIN_EPSILON = 0.05        # Higher minimum
   ```

2. **Adjust Reward Structure**:
   ```python
   SUCCESS_REWARD = 2.0      # Increase success reward
   COLLISION_PENALTY = -2.0  # Increase collision penalty
   ```

3. **Run Longer Simulations**:
   ```bash
   python main_system.py --episodes 2000
   ```

#### Issue: Visualization Not Working
**Symptoms:**
- No plots appearing
- Matplotlib errors

**Solutions:**
1. **Set Matplotlib Backend**:
   ```python
   import matplotlib
   matplotlib.use('TkAgg')  # or 'Qt5Agg'
   ```

2. **Install GUI Dependencies**:
   ```bash
   # Ubuntu/Debian:
   sudo apt install python3-tk

   # macOS:
   brew install python-tk
   ```

3. **Use Non-Interactive Mode**:
   ```python
   # In config.py, set:
   PLOT_UPDATE_INTERVAL = 0  # Disable real-time plots
   ```

### NS3 Integration Issues

#### Issue: NS3 Not Found
**Symptoms:**
```
NS3 integration test failed: [Errno 2] No such file or directory: 'ns3'
```

**Solutions:**
1. **Install NS3** (optional):
   ```bash
   # Ubuntu/Debian:
   sudo apt update
   sudo apt install build-essential libsqlite3-dev libboost-all-dev libssl-dev
   git clone https://gitlab.com/nsnam/ns-3-dev.git
   cd ns-3-dev
   ./ns3 configure --enable-examples --enable-tests
   ./ns3 build
   
   # Add to PATH:
   echo 'export PATH=$PATH:~/ns-3-dev' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Use Simulation Mode** (fallback):
   ```bash
   python main_system.py  # Will use simulated data
   ```

#### Issue: NS3 Compilation Errors
**Symptoms:**
```
g++: error: unrecognized command line option
```

**Solutions:**
1. **Update Build Tools**:
   ```bash
   sudo apt update
   sudo apt install build-essential cmake
   ```

2. **Check NS3 Requirements**:
   ```bash
   # Install additional dependencies
   sudo apt install libxml2-dev libgtk-3-dev libgsl-dev
   ```

3. **Use Pre-built NS3**:
   ```bash
   # macOS:
   brew install ns3
   ```

#### Issue: NS3 Simulation Crashes
**Symptoms:**
```
NS3 simulation terminated unexpectedly
```

**Solutions:**
1. **Check NS3 Script**:
   ```bash
   # Verify NS3 script exists
   ls -la rf_learning_simulation.cc
   ```

2. **Run NS3 Manually**:
   ```bash
   ns3 run rf_learning_simulation.cc
   ```

3. **Use Fallback Mode**:
   ```bash
   python main_system.py  # Will use simulated data
   ```

### Performance Issues

#### Issue: Slow Simulation
**Symptoms:**
- Long episode times
- High CPU usage

**Solutions:**
1. **Reduce Visualization Updates**:
   ```python
   # In config.py:
   PLOT_UPDATE_INTERVAL = 5.0  # Update every 5 seconds
   ```

2. **Reduce Episode Frequency**:
   ```python
   # In config.py:
   SENSING_INTERVAL = 0.2  # Increase from 0.1
   ```

3. **Disable Real-time Plots**:
   ```python
   # In main_system.py, comment out:
   # self._update_visualization()
   ```

#### Issue: Memory Usage High
**Symptoms:**
- System becomes slow
- Out of memory errors

**Solutions:**
1. **Limit Episode Count**:
   ```bash
   python main_system.py --episodes 500
   ```

2. **Clear Old Data**:
   ```bash
   rm -f q_table.pkl final_results.png channel_heatmap.png
   ```

3. **Reduce Q-table Size**:
   ```python
   # In config.py, reduce state space:
   NUM_CHANNELS = 3  # Reduce from 5
   ```

### Configuration Issues

#### Issue: Invalid Configuration
**Symptoms:**
```
Configuration test failed - missing parameter
```

**Solutions:**
1. **Check config.py**:
   ```bash
   python -c "import config; print(dir(config))"
   ```

2. **Restore Default Configuration**:
   ```bash
   # Recreate config.py with default values
   ```

3. **Validate Parameters**:
   ```python
   # In config.py, ensure all required parameters exist:
   NUM_CHANNELS = 5
   SENSING_INTERVAL = 0.1
   POWER_THRESHOLD = -60
   LEARNING_RATE = 0.1
   DISCOUNT_FACTOR = 0.9
   # ... etc
   ```

## Debugging Techniques

### 1. Enable Verbose Logging
```python
# In config.py:
LOG_LEVEL = "DEBUG"
```

### 2. Run with Debug Output
```bash
python -u main_system.py --episodes 10 2>&1 | tee debug.log
```

### 3. Test Individual Components
```bash
# Test agents only
python -c "
from q_learning_agent import TabularQAgent
from random_agent import RandomAgent
agent = TabularQAgent()
print('Q-Agent test passed')
"

# Test visualization only
python -c "
from visualization import RFLearningVisualizer
viz = RFLearningVisualizer()
print('Visualization test passed')
"
```

### 4. Check File Permissions
```bash
# Ensure write permissions
chmod 755 *.py
chmod 644 *.txt *.md
```

## Getting Help

### 1. Check System Information
```bash
# Python version
python --version

# Installed packages
pip list

# System info
uname -a
```

### 2. Collect Error Information
```bash
# Run with full error output
python main_system.py 2>&1 | tee error.log

# Check system log
tail -50 system_log.txt
```

### 3. Minimal Test Case
```bash
# Create minimal test
python -c "
import numpy as np
import matplotlib.pyplot as plt
print('Basic dependencies OK')
"
```

## Performance Optimization

### 1. Faster Learning
```python
# In config.py:
LEARNING_RATE = 0.2        # Faster learning
EPSILON_DECAY = 0.99       # Faster exploration decay
SENSING_INTERVAL = 0.05    # Faster episodes
```

### 2. Better Performance
```python
# In config.py:
SUCCESS_REWARD = 2.0       # Higher success reward
COLLISION_PENALTY = -2.0   # Higher collision penalty
POWER_THRESHOLD = -65      # More sensitive detection
```

### 3. Stable Learning
```python
# In config.py:
MIN_EPSILON = 0.05         # Maintain some exploration
DISCOUNT_FACTOR = 0.95     # Slightly higher discount
```

## Common Commands

### System Management
```bash
# Test system
python test_system.py

# Run simulation
python main_system.py

# Run with NS3
python main_system.py --ns3

# Load existing Q-table
python main_system.py --load-qtable

# Custom parameters
python main_system.py --episodes 500 --time 60
```

### File Management
```bash
# Clean output files
rm -f *.png *.pkl system_log.txt

# Backup Q-table
cp q_table.pkl q_table_backup.pkl

# Check file sizes
ls -lh *.pkl *.png *.txt
```

---

**Note**: This simplified version focuses on simulation and NS3 issues. All hardware-related troubleshooting has been removed. 