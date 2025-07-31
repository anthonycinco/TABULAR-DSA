"""
Configuration parameters for the Simplified RF Learning System
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

# Simulation Parameters
SIMULATION_STEPS = 1000
SIMULATION_DURATION = 100  # seconds

# File Paths
DATA_FILE = "spectrum_data.csv"
Q_TABLE_FILE = "q_table.pkl"
LOG_FILE = "system_log.txt"

# Visualization Parameters
PLOT_UPDATE_INTERVAL = 1.0  # seconds
FIGURE_SIZE = (15, 10)
DPI = 100

# Channel Parameters
CHANNEL_BANDWIDTH = 20e6  # 20 MHz per channel
TOTAL_BANDWIDTH = NUM_CHANNELS * CHANNEL_BANDWIDTH

# Reward Parameters
SUCCESS_REWARD = 1.0
COLLISION_PENALTY = -1.0
DEFER_REWARD = 0.0  # Reward for choosing to defer transmission

# NS3 Parameters
NS3_NUM_NODES = 5
NS3_SIMULATION_TIME = 100
NS3_CHANNEL_WIDTH = 20  # MHz
NS3_FREQUENCY = 2440  # MHz
NS3_ENABLE_INTERFERENCE = True

# Logging Parameters
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 