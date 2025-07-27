#!/usr/bin/env python3
"""
Main RF Learning System
Orchestrates spectrum sensing, Q-learning, and visualization
"""

import argparse
import time
import threading
import numpy as np
import logging
import os
import signal
import sys
from datetime import datetime

import config
from q_learning_agent import TabularQAgent
from random_agent import RandomAgent
from visualization import RFLearningVisualizer
from ns3_integration import NS3SpectrumProvider

class RFLearningSystem:
    """
    Main RF Learning System that coordinates all components
    """
    
    def __init__(self, simulate=False, load_q_table=False, use_ns3=False):
        """
        Initialize the RF learning system
        
        Args:
            simulate: Whether to use simulated data instead of real USRP
            load_q_table: Whether to load existing Q-table
            use_ns3: Whether to use NS3 simulation
        """
        self.simulate = simulate
        self.load_q_table = load_q_table
        self.use_ns3 = use_ns3
        self.running = False
        
        # Setup logging
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Initialize agents
        self.q_agent = TabularQAgent()
        self.random_agent = RandomAgent()
        
        # Load Q-table if requested
        if load_q_table:
            self.q_agent.load_q_table()
        
        # Initialize visualizer
        self.visualizer = RFLearningVisualizer()
        
        # Initialize spectrum data provider
        if use_ns3:
            self.spectrum_provider = NS3SpectrumProvider(use_ns3=True)
            self.logger.info("NS3 spectrum provider initialized")
        else:
            self.spectrum_provider = None
        
        # Initialize spectrum data
        self.spectrum_data = None
        self.data_lock = threading.Lock()
        
        # Statistics
        self.episode_count = 0
        self.start_time = None
        
        self.logger.info("RF Learning System initialized")
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, config.LOG_LEVEL),
            format=config.LOG_FORMAT,
            handlers=[
                logging.FileHandler(config.LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def _simulate_spectrum_data(self):
        """
        Simulate spectrum data for testing without USRP
        
        Returns:
            List of 5 power levels in dB
        """
        # Simulate realistic 2.4 GHz spectrum with some channels busy
        base_power = -70  # Base noise floor
        
        # Randomly make some channels busy
        busy_channels = np.random.choice([0, 1], size=config.NUM_CHANNELS, p=[0.7, 0.3])
        
        power_levels = []
        for i in range(config.NUM_CHANNELS):
            if busy_channels[i]:
                # Busy channel: higher power with some variation
                power = base_power + np.random.normal(20, 5)  # -50 to -40 dB
            else:
                # Idle channel: lower power with noise
                power = base_power + np.random.normal(0, 2)  # -72 to -68 dB
            
            power_levels.append(power)
        
        return power_levels
    
    def _read_usrp_data(self):
        """
        Read spectrum data from USRP (placeholder for real implementation)
        
        Returns:
            List of 5 power levels in dB
        """
        # This is a placeholder - in real implementation, this would:
        # 1. Read from GNU Radio flowgraph output
        # 2. Process FFT data
        # 3. Extract power levels for 5 channels
        
        try:
            # For now, simulate data
            # In real implementation, read from file or socket
            if os.path.exists("spectrum_data.bin"):
                # Read binary data from GNU Radio
                with open("spectrum_data.bin", "rb") as f:
                    # This is a simplified version - real implementation would
                    # parse the actual GNU Radio data format
                    data = f.read()
                
                # Process data to extract power levels
                # For now, return simulated data
                return self._simulate_spectrum_data()
            else:
                # No data file, use simulation
                return self._simulate_spectrum_data()
                
        except Exception as e:
            self.logger.warning(f"Error reading USRP data: {e}")
            return self._simulate_spectrum_data()
    
    def _get_spectrum_data(self):
        """
        Get current spectrum data
        
        Returns:
            List of 5 power levels in dB
        """
        if self.use_ns3 and self.spectrum_provider:
            return self.spectrum_provider.get_power_levels()
        elif self.simulate:
            return self._simulate_spectrum_data()
        else:
            return self._read_usrp_data()
    
    def _simulate_transmission_result(self, action, power_levels):
        """
        Simulate transmission success/failure based on channel state
        
        Args:
            action: Selected action (0-4 for channels, 5 for defer)
            power_levels: Current power levels
            
        Returns:
            Tuple of (reward, collision_occurred)
        """
        if action == config.NUM_CHANNELS:
            # Defer action
            return config.DEFER_REWARD, False
        
        # Check if selected channel is busy
        channel_power = power_levels[action]
        is_busy = channel_power > config.POWER_THRESHOLD
        
        if is_busy:
            # Collision
            return config.COLLISION_PENALTY, True
        else:
            # Success
            return config.SUCCESS_REWARD, False
    
    def _run_episode(self):
        """
        Run a single learning episode
        
        Returns:
            Dictionary with episode results
        """
        # Get current spectrum data
        power_levels = self._get_spectrum_data()
        
        # Agents observe and act
        q_action = self.q_agent.observe_and_act(power_levels)
        random_action = self.random_agent.observe_and_act(power_levels)
        
        # Simulate transmission results
        q_reward, q_collision = self._simulate_transmission_result(q_action, power_levels)
        random_reward, random_collision = self._simulate_transmission_result(random_action, power_levels)
        
        # Agents learn
        self.q_agent.learn(power_levels, q_reward, q_collision)
        self.random_agent.learn(power_levels, random_reward, random_collision)
        
        # Log episode details
        self.logger.debug(f"Episode {self.episode_count}: "
                         f"Q-Action={q_action}, Q-Reward={q_reward:.2f}, Q-Collision={q_collision}, "
                         f"R-Action={random_action}, R-Reward={random_reward:.2f}, R-Collision={random_collision}")
        
        return {
            'power_levels': power_levels,
            'q_action': q_action,
            'q_reward': q_reward,
            'q_collision': q_collision,
            'random_action': random_action,
            'random_reward': random_reward,
            'random_collision': random_collision
        }
    
    def _update_visualization(self):
        """Update visualization with current data"""
        try:
            self.visualizer.update_plots(self.q_agent, self.random_agent, self.episode_count)
        except Exception as e:
            self.logger.error(f"Error updating visualization: {e}")
    
    def _print_statistics(self):
        """Print current statistics to console"""
        q_stats = self.q_agent.get_statistics()
        random_stats = self.random_agent.get_statistics()
        
        print(f"\n{'='*60}")
        print(f"Episode: {self.episode_count}")
        print(f"Runtime: {time.time() - self.start_time:.1f}s")
        print(f"{'='*60}")
        print(f"{'Metric':<20} {'Q-Agent':<15} {'Random Agent':<15}")
        print(f"{'-'*60}")
        print(f"{'Total Reward':<20} {q_stats['total_reward']:<15.2f} {random_stats['total_reward']:<15.2f}")
        print(f"{'Collision Rate':<20} {q_stats['collision_rate']:<15.3f} {random_stats['collision_rate']:<15.3f}")
        print(f"{'Success Rate':<20} {q_stats['success_rate']:<15.3f} {random_stats['success_rate']:<15.3f}")
        print(f"{'Defer Rate':<20} {q_stats['defer_rate']:<15.3f} {random_stats['defer_rate']:<15.3f}")
        if hasattr(self.q_agent, 'epsilon'):
            print(f"{'Q-Agent Epsilon':<20} {self.q_agent.epsilon:<15.3f} {'N/A':<15}")
        print(f"{'='*60}")
    
    def run(self, max_episodes=None, max_time=None):
        """
        Run the RF learning system
        
        Args:
            max_episodes: Maximum number of episodes to run
            max_time: Maximum time to run in seconds
        """
        self.running = True
        self.start_time = time.time()
        
        self.logger.info(f"Starting RF Learning System (Simulate: {self.simulate})")
        print(f"Starting RF Learning System...")
        print(f"Simulation mode: {self.simulate}")
        print(f"Max episodes: {max_episodes}")
        print(f"Max time: {max_time}s")
        print(f"Press Ctrl+C to stop early")
        
        try:
            while self.running:
                # Check termination conditions
                if max_episodes and self.episode_count >= max_episodes:
                    self.logger.info(f"Reached maximum episodes: {max_episodes}")
                    break
                
                if max_time and (time.time() - self.start_time) >= max_time:
                    self.logger.info(f"Reached maximum time: {max_time}s")
                    break
                
                # Run episode
                episode_result = self._run_episode()
                self.episode_count += 1
                
                # Update visualization periodically
                if self.episode_count % 10 == 0:
                    self._update_visualization()
                
                # Print statistics periodically
                if self.episode_count % 100 == 0:
                    self._print_statistics()
                
                # Sleep between episodes
                time.sleep(config.SENSING_INTERVAL)
                
        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal, stopping...")
            print("\nStopping RF Learning System...")
        
        finally:
            self.stop()
    
    def stop(self):
        """Stop the RF learning system"""
        self.running = False
        
        # Save Q-table
        self.q_agent.save_q_table()
        
        # Print final statistics
        self._print_statistics()
        
        # Create final visualizations
        self.logger.info("Creating final visualizations...")
        self.visualizer.plot_final_results(self.q_agent, self.random_agent, "final_results.png")
        self.visualizer.create_channel_heatmap(self.q_agent, self.random_agent, "channel_heatmap.png")
        
        # Close visualizer
        self.visualizer.close()
        
        self.logger.info("RF Learning System stopped")
        print("RF Learning System stopped")
        print("Final results saved to:")
        print("- final_results.png")
        print("- channel_heatmap.png")
        print(f"- {config.Q_TABLE_FILE}")

def signal_handler(signum, frame):
    """Handle interrupt signals"""
    print("\nReceived interrupt signal")
    sys.exit(0)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='RF Learning System')
    parser.add_argument('--simulate', action='store_true', 
                       help='Use simulated data instead of real USRP')
    parser.add_argument('--ns3', action='store_true',
                       help='Use NS3 simulation for realistic network conditions')
    parser.add_argument('--load-qtable', action='store_true',
                       help='Load existing Q-table from file')
    parser.add_argument('--episodes', type=int, default=config.SIMULATION_STEPS,
                       help=f'Maximum number of episodes (default: {config.SIMULATION_STEPS})')
    parser.add_argument('--time', type=int, default=config.SIMULATION_DURATION,
                       help=f'Maximum runtime in seconds (default: {config.SIMULATION_DURATION})')
    parser.add_argument('--create-flowgraph', action='store_true',
                       help='Create GNU Radio flowgraph file')
    
    args = parser.parse_args()
    
    # Handle signal interrupts
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create flowgraph if requested
    if args.create_flowgraph:
        from create_flowgraph import create_flowgraph
        create_flowgraph()
        return
    
    # Create and run system
    system = RFLearningSystem(simulate=args.simulate, 
                             load_q_table=args.load_qtable,
                             use_ns3=args.ns3)
    
    try:
        system.run(max_episodes=args.episodes, max_time=args.time)
    except Exception as e:
        logging.error(f"Error running system: {e}")
        system.stop()
        raise

if __name__ == "__main__":
    main() 