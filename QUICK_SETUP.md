# RF Learning System - Quick Setup Guide

## 🚀 One-Minute Setup (Ubuntu 20.04+)

### Prerequisites Check
```bash
# Check if you have the required hardware
lsusb | grep Ettus  # Should show USRP1 if connected
python3 --version   # Should be 3.7+
```

### Quick Installation
```bash
# 1. Install system dependencies
sudo apt update && sudo apt install -y build-essential cmake git python3 python3-pip qt5-default

# 2. Install GNU Radio and UHD
sudo add-apt-repository ppa:gnuradio/gnuradio-releases
sudo apt update
sudo apt install -y gnuradio uhd-host uhd-dev

# 3. Install Python packages
pip3 install numpy matplotlib pandas scipy seaborn

# 4. Test installation
uhd_usrp_probe
gnuradio-companion --version
```

## 🎯 Quick Start Commands

### Test the System
```bash
# Run basic tests
python3 test_system.py

# Test NS3 integration
python3 test_ns3_integration.py
```

### Run Different Modes

#### Simulation Mode (No Hardware Required)
```bash
python3 main_system.py --simulate --episodes 100
```

#### NS3 Mode (Realistic Network Simulation)
```bash
python3 main_system.py --ns3 --episodes 100
```

#### Real USRP Mode (With Hardware)
```bash
# Terminal 1: Start GNU Radio
gnuradio-companion rf_sensing.grc

# Terminal 2: Run learning system
python3 main_system.py
```

## ⚙️ Essential Configuration

### Edit `config.py` for Your Environment
```python
# USRP Settings
USRP_DEVICE = "addr=192.168.10.2"  # Your USRP IP
USRP_GAIN = 20                     # Adjust based on signal strength

# RF Environment
POWER_THRESHOLD = -60              # Adjust for your environment
CENTER_FREQUENCY = 2.44e9          # 2.44 GHz

# Learning Parameters
LEARNING_RATE = 0.1                # 0.01 to 0.3
EPSILON_DECAY = 0.995              # 0.99 to 0.999
```

## 🔧 Common Commands

### System Control
```bash
# Start system
python3 main_system.py [--simulate|--ns3] [--episodes 1000]

# Stop system
Ctrl+C

# Load pre-trained Q-table
python3 main_system.py --load-qtable
```

### Monitoring
```bash
# View logs
tail -f system_log.txt

# Check Q-table
python3 -c "import pickle; print(pickle.load(open('q_table.pkl', 'rb')))"
```

### Troubleshooting
```bash
# Check USRP connection
uhd_usrp_probe

# Check GNU Radio
gnuradio-companion --version

# Check Python packages
pip3 list | grep -E "(numpy|matplotlib|pandas|scipy|seaborn)"
```

## 📊 Expected Performance

### Learning Progress
- **Episodes 1-50**: Random exploration (epsilon ≈ 1.0)
- **Episodes 50-200**: Learning phase (epsilon decreasing)
- **Episodes 200+**: Exploitation phase (epsilon ≈ 0.01)

### Success Metrics
- Q-agent should outperform random agent by 10-20%
- Collision rate should decrease over time
- Success rate should increase to 70-90%

## 🎨 Output Files

After running, you'll get:
- `final_results.png` - Performance comparison plots
- `channel_heatmap.png` - Channel usage analysis
- `q_table.pkl` - Learned Q-table
- `system_log.txt` - Detailed logs

## 🆘 Quick Fixes

### USRP Not Detected
```bash
sudo uhd_usrp_probe
sudo usermod -a -G usb $USER
sudo reboot
```

### GNU Radio Issues
```bash
sudo apt remove gnuradio
sudo apt install gnuradio
```

### Python Package Issues
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## 📞 Support

- Check `system_log.txt` for detailed error messages
- Run `python3 test_system.py` to verify installation
- Review the full README.md for comprehensive documentation

---

**Ready to start learning!** 🚀 