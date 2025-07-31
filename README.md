# Simplified RF Learning System

A spectrum sensing and Q-learning system using simulation and NS3 network simulation.

## Overview

This system performs spectrum sensing simulation at 2.4 GHz and uses Q-learning to intelligently select channels while avoiding collisions. It provides two modes of operation:

1. **Simulated Data Mode** - Uses realistic spectrum simulation
2. **NS3 Simulation Mode** - Uses NS3 network simulator for realistic wireless network conditions

## Features

- **Q-Learning Agent**: Intelligent channel selection using tabular Q-learning
- **Random Agent**: Baseline comparison agent
- **Real-time Visualization**: Live plots showing agent performance
- **NS3 Integration**: Realistic wireless network simulation
- **Configurable Parameters**: Easy tuning of learning and simulation parameters

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Q-Learning    │    │   Random Agent  │    │   Visualization │
│     Agent       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Spectrum Data  │
                    │    Provider     │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │  NS3 Simulator  │
                    │   (Optional)    │
                    └─────────────────┘
```

## Requirements

### Software Requirements
- **Python**: 3.7+
- **NS3**: 3.35+ (optional, for realistic network simulation)
- **Dependencies**: See `requirements.txt`

### Dependencies
```
numpy>=1.19.0
matplotlib>=3.3.0
seaborn>=0.11.0
pickle5>=0.0.11
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test the System
```bash
python test_system.py
```

### 3. Run Basic Simulation
```bash
python main_system.py
```

### 4. Run NS3 Simulation (if NS3 is installed)
```bash
python main_system.py --ns3
```

## Usage Examples

### Basic Simulation (1000 episodes)
```bash
python main_system.py --episodes 1000
```

### NS3 Simulation (60 seconds)
```bash
python main_system.py --ns3 --time 60
```

### Load Existing Q-Table
```bash
python main_system.py --load-qtable
```

### Custom Parameters
```bash
python main_system.py --episodes 500 --time 30
```

## Configuration

Key parameters can be modified in `config.py`:

```python
# Learning Parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
INITIAL_EPSILON = 1.0

# Simulation Parameters
NUM_CHANNELS = 5
SENSING_INTERVAL = 0.1  # seconds
POWER_THRESHOLD = -60   # dB

# Reward Parameters
SUCCESS_REWARD = 1.0
COLLISION_PENALTY = -1.0
DEFER_REWARD = 0.0
```

## Output Files

The system generates several output files:

- **`final_results.png`**: Final performance comparison plots
- **`channel_heatmap.png`**: Channel usage heatmaps
- **`q_table.pkl`**: Saved Q-learning table
- **`system_log.txt`**: System execution log

## NS3 Integration

### Installing NS3 (Optional)

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install build-essential libsqlite3-dev libboost-all-dev libssl-dev
git clone https://gitlab.com/nsnam/ns-3-dev.git
cd ns-3-dev
./ns3 configure --enable-examples --enable-tests
./ns3 build
```

#### macOS
```bash
brew install ns3
```

#### Windows (WSL2 recommended)
```bash
# Use Ubuntu instructions in WSL2
```

### NS3 Features
- Realistic 802.11 network simulation
- Multiple wireless nodes
- Interference modeling
- Dynamic channel conditions
- Spectrum data export

## System Components

### Core Files
- **`main_system.py`**: Main system orchestrator
- **`q_learning_agent.py`**: Q-learning implementation
- **`random_agent.py`**: Random baseline agent
- **`ns3_integration.py`**: NS3 simulation interface
- **`visualization.py`**: Real-time plotting
- **`config.py`**: Configuration parameters

### Test Files
- **`test_system.py`**: System test suite
- **`test_ns3_integration.py`**: NS3 integration tests

## Performance Metrics

The system tracks several key metrics:

- **Total Reward**: Cumulative reward over time
- **Collision Rate**: Percentage of failed transmissions
- **Success Rate**: Percentage of successful transmissions
- **Defer Rate**: Percentage of times agent chooses to defer
- **Channel Usage**: Distribution of channel selections

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **NS3 Not Found**: NS3 integration is optional
   - System will fall back to simulated data
   - Install NS3 for realistic network simulation

3. **Visualization Issues**: Check matplotlib backend
   ```python
   import matplotlib
   matplotlib.use('TkAgg')  # or 'Qt5Agg'
   ```

### Getting Help

1. Run the test suite: `python test_system.py`
2. Check the system log: `system_log.txt`
3. Review configuration: `config.py`

## Development

### Adding New Agents
1. Create agent class with `observe_and_act()` and `learn()` methods
2. Integrate into `main_system.py`
3. Add to visualization system

### Extending NS3 Simulation
1. Modify `rf_learning_simulation.cc`
2. Update `ns3_integration.py`
3. Test with `test_ns3_integration.py`

## License

This project is provided as-is for educational and research purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Note**: This is a simplified version focused on simulation and NS3 integration. All hardware dependencies have been removed for easier deployment and testing. 