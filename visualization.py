#!/usr/bin/env python3
"""
Visualization module for RF Learning System
Provides real-time plotting and analysis of agent performance
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from collections import defaultdict
import config
import logging

class RFLearningVisualizer:
    """
    Real-time visualizer for RF learning system performance
    """
    
    def __init__(self):
        """Initialize the visualizer"""
        self.logger = logging.getLogger(__name__)
        
        # Setup matplotlib for real-time plotting
        plt.ion()  # Turn on interactive mode
        sns.set_style("whitegrid")
        
        # Create figure with subplots
        self.fig, self.axes = plt.subplots(2, 3, figsize=config.FIGURE_SIZE, dpi=config.DPI)
        self.fig.suptitle('RF Learning System Performance', fontsize=16, fontweight='bold')
        
        # Initialize plot data
        self.episode_data = []
        self.q_reward_data = []
        self.random_reward_data = []
        self.q_collision_data = []
        self.random_collision_data = []
        self.q_channel_usage = defaultdict(int)
        self.random_channel_usage = defaultdict(int)
        
        # Setup plots
        self._setup_plots()
        
    def _setup_plots(self):
        """Setup the initial plots"""
        # Reward comparison
        self.axes[0, 0].set_title('Cumulative Reward')
        self.axes[0, 0].set_xlabel('Episode')
        self.axes[0, 0].set_ylabel('Total Reward')
        self.axes[0, 0].grid(True)
        
        # Collision rate comparison
        self.axes[0, 1].set_title('Collision Rate')
        self.axes[0, 1].set_xlabel('Episode')
        self.axes[0, 1].set_ylabel('Collision Rate')
        self.axes[0, 1].grid(True)
        
        # Q-agent channel usage heatmap
        self.axes[0, 2].set_title('Q-Agent Channel Usage')
        self.axes[0, 2].set_xlabel('Channel')
        self.axes[0, 2].set_ylabel('Usage Count')
        
        # Random agent channel usage heatmap
        self.axes[1, 0].set_title('Random Agent Channel Usage')
        self.axes[1, 0].set_xlabel('Channel')
        self.axes[1, 0].set_ylabel('Usage Count')
        
        # Success rate comparison
        self.axes[1, 1].set_title('Success Rate')
        self.axes[1, 1].set_xlabel('Episode')
        self.axes[1, 1].set_ylabel('Success Rate')
        self.axes[1, 1].grid(True)
        
        # Epsilon decay
        self.axes[1, 2].set_title('Q-Agent Epsilon')
        self.axes[1, 2].set_xlabel('Episode')
        self.axes[1, 2].set_ylabel('Epsilon')
        self.axes[1, 2].grid(True)
        
        plt.tight_layout()
        plt.show()
    
    def update_plots(self, q_agent, random_agent, episode):
        """
        Update all plots with current data
        
        Args:
            q_agent: Q-learning agent
            random_agent: Random agent
            episode: Current episode number
        """
        # Get statistics
        q_stats = q_agent.get_statistics()
        random_stats = random_agent.get_statistics()
        
        # Update data arrays
        self.episode_data.append(episode)
        self.q_reward_data.append(q_stats['total_reward'])
        self.random_reward_data.append(random_stats['total_reward'])
        self.q_collision_data.append(q_stats['collision_rate'])
        self.random_collision_data.append(random_stats['collision_rate'])
        
        # Update channel usage
        q_channel_stats = q_agent.get_channel_usage_stats()
        random_channel_stats = random_agent.get_channel_usage_stats()
        
        for channel in range(config.NUM_CHANNELS):
            self.q_channel_usage[channel] = q_channel_stats.get(channel, 0)
            self.random_channel_usage[channel] = random_channel_stats.get(channel, 0)
        
        # Clear all plots
        for ax in self.axes.flat:
            ax.clear()
        
        # Re-setup plots
        self._setup_plots()
        
        # Plot reward comparison
        self.axes[0, 0].plot(self.episode_data, self.q_reward_data, 'b-', label='Q-Agent', linewidth=2)
        self.axes[0, 0].plot(self.episode_data, self.random_reward_data, 'r-', label='Random Agent', linewidth=2)
        self.axes[0, 0].legend()
        
        # Plot collision rate comparison
        self.axes[0, 1].plot(self.episode_data, self.q_collision_data, 'b-', label='Q-Agent', linewidth=2)
        self.axes[0, 1].plot(self.episode_data, self.random_collision_data, 'r-', label='Random Agent', linewidth=2)
        self.axes[0, 1].legend()
        
        # Plot Q-agent channel usage
        channels = list(range(config.NUM_CHANNELS))
        q_usage = [self.q_channel_usage[ch] for ch in channels]
        self.axes[0, 2].bar(channels, q_usage, color='blue', alpha=0.7)
        self.axes[0, 2].set_xticks(channels)
        
        # Plot random agent channel usage
        random_usage = [self.random_channel_usage[ch] for ch in channels]
        self.axes[1, 0].bar(channels, random_usage, color='red', alpha=0.7)
        self.axes[1, 0].set_xticks(channels)
        
        # Plot success rate comparison
        q_success_rate = [q_stats['success_rate']] * len(self.episode_data) if self.episode_data else [0]
        random_success_rate = [random_stats['success_rate']] * len(self.episode_data) if self.episode_data else [0]
        
        self.axes[1, 1].plot(self.episode_data, q_success_rate, 'b-', label='Q-Agent', linewidth=2)
        self.axes[1, 1].plot(self.episode_data, random_success_rate, 'r-', label='Random Agent', linewidth=2)
        self.axes[1, 1].legend()
        
        # Plot epsilon decay
        if hasattr(q_agent, 'epsilon'):
            epsilon_data = [q_agent.epsilon] * len(self.episode_data) if self.episode_data else [config.INITIAL_EPSILON]
            self.axes[1, 2].plot(self.episode_data, epsilon_data, 'g-', linewidth=2)
        
        # Update display
        plt.draw()
        plt.pause(0.01)
    
    def plot_final_results(self, q_agent, random_agent, save_path=None):
        """
        Create final comprehensive plots
        
        Args:
            q_agent: Q-learning agent
            random_agent: Random agent
            save_path: Path to save plots (optional)
        """
        # Create a new figure for final results
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('RF Learning System - Final Results', fontsize=16, fontweight='bold')
        
        # Get final statistics
        q_stats = q_agent.get_statistics()
        random_stats = random_agent.get_statistics()
        
        # 1. Performance comparison
        metrics = ['Total Reward', 'Collision Rate', 'Success Rate']
        q_values = [q_stats['total_reward'], q_stats['collision_rate'], q_stats['success_rate']]
        random_values = [random_stats['total_reward'], random_stats['collision_rate'], random_stats['success_rate']]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        axes[0, 0].bar(x - width/2, q_values, width, label='Q-Agent', color='blue', alpha=0.7)
        axes[0, 0].bar(x + width/2, random_values, width, label='Random Agent', color='red', alpha=0.7)
        axes[0, 0].set_xlabel('Metrics')
        axes[0, 0].set_ylabel('Value')
        axes[0, 0].set_title('Performance Comparison')
        axes[0, 0].set_xticks(x)
        axes[0, 0].set_xticklabels(metrics)
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Channel usage comparison
        channels = list(range(config.NUM_CHANNELS))
        q_channel_stats = q_agent.get_channel_usage_stats()
        random_channel_stats = random_agent.get_channel_usage_stats()
        
        q_usage = [q_channel_stats.get(ch, 0) for ch in channels]
        random_usage = [random_channel_stats.get(ch, 0) for ch in channels]
        
        # Use channels as x-axis positions
        x_channels = np.arange(len(channels))
        
        axes[0, 1].bar(x_channels - width/2, q_usage, width, label='Q-Agent', color='blue', alpha=0.7)
        axes[0, 1].bar(x_channels + width/2, random_usage, width, label='Random Agent', color='red', alpha=0.7)
        axes[0, 1].set_xlabel('Channel')
        axes[0, 1].set_ylabel('Usage Count')
        axes[0, 1].set_title('Channel Usage Comparison')
        axes[0, 1].set_xticks(x_channels)
        axes[0, 1].set_xticklabels(channels)
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Learning curve
        if q_agent.reward_history:
            episodes = list(range(1, len(q_agent.reward_history) + 1))
            cumulative_q_reward = np.cumsum(q_agent.reward_history)
            cumulative_random_reward = np.cumsum(random_agent.reward_history)
            
            axes[1, 0].plot(episodes, cumulative_q_reward, 'b-', label='Q-Agent', linewidth=2)
            axes[1, 0].plot(episodes, cumulative_random_reward, 'r-', label='Random Agent', linewidth=2)
            axes[1, 0].set_xlabel('Episode')
            axes[1, 0].set_ylabel('Cumulative Reward')
            axes[1, 0].set_title('Learning Curve')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Collision rate over time
        if q_agent.collision_history:
            episodes = list(range(1, len(q_agent.collision_history) + 1))
            q_collision_rate = np.cumsum(q_agent.collision_history) / np.arange(1, len(q_agent.collision_history) + 1)
            random_collision_rate = np.cumsum(random_agent.collision_history) / np.arange(1, len(random_agent.collision_history) + 1)
            
            axes[1, 1].plot(episodes, q_collision_rate, 'b-', label='Q-Agent', linewidth=2)
            axes[1, 1].plot(episodes, random_collision_rate, 'r-', label='Random Agent', linewidth=2)
            axes[1, 1].set_xlabel('Episode')
            axes[1, 1].set_ylabel('Collision Rate')
            axes[1, 1].set_title('Collision Rate Over Time')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Final results saved to {save_path}")
        
        plt.show()
    
    def create_channel_heatmap(self, q_agent, random_agent, save_path=None):
        """
        Create channel usage heatmap
        
        Args:
            q_agent: Q-learning agent
            random_agent: Random agent
            save_path: Path to save heatmap (optional)
        """
        # Create heatmap data
        channels = list(range(config.NUM_CHANNELS))
        q_channel_stats = q_agent.get_channel_usage_stats()
        random_channel_stats = random_agent.get_channel_usage_stats()
        
        # Normalize usage counts
        max_usage = max(max(q_channel_stats.values(), default=0), max(random_channel_stats.values(), default=0))
        if max_usage == 0:
            max_usage = 1
        
        q_usage_normalized = [q_channel_stats.get(ch, 0) / max_usage for ch in channels]
        random_usage_normalized = [random_channel_stats.get(ch, 0) / max_usage for ch in channels]
        
        # Create heatmap
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        fig.suptitle('Channel Usage Heatmap', fontsize=16, fontweight='bold')
        
        # Q-agent heatmap
        q_data = np.array(q_usage_normalized).reshape(1, -1)
        sns.heatmap(q_data, annot=True, fmt='.2f', cmap='Blues', 
                   xticklabels=channels, yticklabels=['Q-Agent'], ax=ax1)
        ax1.set_title('Q-Agent Channel Usage')
        ax1.set_xlabel('Channel')
        
        # Random agent heatmap
        random_data = np.array(random_usage_normalized).reshape(1, -1)
        sns.heatmap(random_data, annot=True, fmt='.2f', cmap='Reds', 
                   xticklabels=channels, yticklabels=['Random Agent'], ax=ax2)
        ax2.set_title('Random Agent Channel Usage')
        ax2.set_xlabel('Channel')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Channel heatmap saved to {save_path}")
        
        plt.show()
    
    def close(self):
        """Close the visualizer"""
        plt.ioff()
        plt.close('all') 