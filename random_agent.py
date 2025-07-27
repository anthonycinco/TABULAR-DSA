#!/usr/bin/env python3
"""
Random Agent for RF Channel Selection
Baseline agent that selects channels randomly for comparison with Q-learning
"""

import numpy as np
from collections import defaultdict
import config
import logging

class RandomAgent:
    """
    Random agent for RF channel selection
    
    This agent selects channels randomly to provide a baseline for comparison
    with the Q-learning agent. It has the same interface as the Q-learning agent
    but doesn't learn from experience.
    """
    
    def __init__(self, power_threshold=config.POWER_THRESHOLD):
        """
        Initialize the random agent
        
        Args:
            power_threshold: Threshold for determining busy/idle channels
        """
        self.power_threshold = power_threshold
        
        # Statistics
        self.total_reward = 0
        self.collision_count = 0
        self.success_count = 0
        self.defer_count = 0
        self.episode_count = 0
        
        # History for analysis
        self.action_history = []
        self.reward_history = []
        self.state_history = []
        self.collision_history = []
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def _power_to_state(self, power_levels):
        """
        Convert power levels to binary occupancy state
        
        Args:
            power_levels: List of 5 power levels in dB
            
        Returns:
            Tuple of 5 binary values (0=idle, 1=busy)
        """
        if len(power_levels) != config.NUM_CHANNELS:
            raise ValueError(f"Expected {config.NUM_CHANNELS} power levels, got {len(power_levels)}")
        
        # Convert power levels to binary occupancy
        # Power > threshold = busy (1), Power <= threshold = idle (0)
        state = tuple(1 if power > self.power_threshold else 0 for power in power_levels)
        return state
    
    def _get_available_actions(self, state):
        """
        Get available actions for a given state
        
        Args:
            state: Current state tuple
            
        Returns:
            List of available actions (channels that are idle + defer option)
        """
        available_actions = []
        
        # Add idle channels as available actions
        for channel in range(config.NUM_CHANNELS):
            if state[channel] == 0:  # Channel is idle
                available_actions.append(channel)
        
        # Always add defer action
        available_actions.append(config.NUM_CHANNELS)  # Defer action
        
        return available_actions
    
    def _random_action(self, state):
        """
        Select action randomly from available actions
        
        Args:
            state: Current state tuple
            
        Returns:
            Selected action (0-4 for channels, 5 for defer)
        """
        available_actions = self._get_available_actions(state)
        
        if not available_actions:
            # If no actions available, defer
            return config.NUM_CHANNELS
        
        # Random selection
        return np.random.choice(available_actions)
    
    def observe_and_act(self, power_levels):
        """
        Observe current power levels and select an action
        
        Args:
            power_levels: List of 5 power levels in dB
            
        Returns:
            Selected action (0-4 for channels, 5 for defer)
        """
        # Convert power levels to state
        state = self._power_to_state(power_levels)
        
        # Select action randomly
        action = self._random_action(state)
        
        # Store for statistics
        self.current_state = state
        self.current_action = action
        
        return action
    
    def learn(self, power_levels, reward, collision_occurred=False):
        """
        Update statistics (no learning for random agent)
        
        Args:
            power_levels: Power levels after action
            reward: Received reward
            collision_occurred: Whether a collision occurred
        """
        # Update statistics
        self.total_reward += reward
        self.episode_count += 1
        
        if collision_occurred:
            self.collision_count += 1
        elif self.current_action < config.NUM_CHANNELS:
            self.success_count += 1
        else:
            self.defer_count += 1
        
        # Store history
        self.action_history.append(self.current_action)
        self.reward_history.append(reward)
        self.state_history.append(self.current_state)
        self.collision_history.append(collision_occurred)
        
        # Log progress
        if self.episode_count % 100 == 0:
            self.logger.info(f"Random Agent Episode {self.episode_count}: "
                           f"Total Reward={self.total_reward:.2f}, "
                           f"Collision Rate={self.collision_count/self.episode_count:.3f}")
    
    def get_statistics(self):
        """
        Get current statistics
        
        Returns:
            Dictionary with statistics
        """
        if self.episode_count == 0:
            return {
                'total_reward': 0,
                'collision_rate': 0,
                'success_rate': 0,
                'defer_rate': 0,
                'episode_count': 0
            }
        
        return {
            'total_reward': self.total_reward,
            'collision_rate': self.collision_count / self.episode_count,
            'success_rate': self.success_count / self.episode_count,
            'defer_rate': self.defer_count / self.episode_count,
            'episode_count': self.episode_count
        }
    
    def get_channel_usage_stats(self):
        """
        Get channel usage statistics
        
        Returns:
            Dictionary with channel usage counts
        """
        channel_counts = defaultdict(int)
        for action in self.action_history:
            if action < config.NUM_CHANNELS:
                channel_counts[action] += 1
        
        return dict(channel_counts)
    
    def reset(self):
        """Reset agent statistics"""
        self.total_reward = 0
        self.collision_count = 0
        self.success_count = 0
        self.defer_count = 0
        self.episode_count = 0
        self.action_history = []
        self.reward_history = []
        self.state_history = []
        self.collision_history = [] 