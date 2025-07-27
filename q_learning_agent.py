#!/usr/bin/env python3
"""
Q-Learning Agent for RF Channel Selection
Implements tabular Q-learning to learn optimal channel selection strategies
"""

import numpy as np
import pickle
import json
from collections import defaultdict
import config
import logging

class TabularQAgent:
    """
    Tabular Q-Learning agent for RF channel selection
    
    The agent observes the power levels of 5 channels and learns to select
    the best channel to avoid collisions and maximize successful transmissions.
    """
    
    def __init__(self, 
                 learning_rate=config.LEARNING_RATE,
                 discount_factor=config.DISCOUNT_FACTOR,
                 epsilon=config.INITIAL_EPSILON,
                 epsilon_decay=config.EPSILON_DECAY,
                 min_epsilon=config.MIN_EPSILON,
                 power_threshold=config.POWER_THRESHOLD):
        """
        Initialize the Q-learning agent
        
        Args:
            learning_rate: Learning rate for Q-value updates
            discount_factor: Discount factor for future rewards
            epsilon: Initial exploration rate
            epsilon_decay: Rate at which epsilon decays
            min_epsilon: Minimum exploration rate
            power_threshold: Threshold for determining busy/idle channels
        """
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.power_threshold = power_threshold
        
        # Q-table: state -> action -> Q-value
        # State is a tuple of 5 binary values (busy/idle for each channel)
        # Actions are 0-4 (channel selection) or 5 (defer)
        self.q_table = defaultdict(lambda: defaultdict(float))
        
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
    
    def _epsilon_greedy_action(self, state):
        """
        Select action using epsilon-greedy policy
        
        Args:
            state: Current state tuple
            
        Returns:
            Selected action (0-4 for channels, 5 for defer)
        """
        available_actions = self._get_available_actions(state)
        
        if not available_actions:
            # If no actions available, defer
            return config.NUM_CHANNELS
        
        # Epsilon-greedy selection
        if np.random.random() < self.epsilon:
            # Exploration: random action
            return np.random.choice(available_actions)
        else:
            # Exploitation: best action
            q_values = [self.q_table[state][action] for action in available_actions]
            best_action_idx = np.argmax(q_values)
            return available_actions[best_action_idx]
    
    def _calculate_reward(self, action, state, next_state):
        """
        Calculate reward based on action and state transition
        
        Args:
            action: Selected action
            state: Current state
            next_state: Next state (after action)
            
        Returns:
            Reward value
        """
        if action == config.NUM_CHANNELS:
            # Defer action
            return config.DEFER_REWARD
        
        # Check if selected channel is busy in current state
        if state[action] == 1:
            # Collision: selected a busy channel
            return config.COLLISION_PENALTY
        else:
            # Success: selected an idle channel
            return config.SUCCESS_REWARD
    
    def _update_q_value(self, state, action, reward, next_state):
        """
        Update Q-value using Bellman equation
        
        Args:
            state: Current state
            action: Selected action
            reward: Received reward
            next_state: Next state
        """
        # Get available actions for next state
        next_available_actions = self._get_available_actions(next_state)
        
        if next_available_actions:
            # Max Q-value for next state
            next_q_values = [self.q_table[next_state][action] for action in next_available_actions]
            max_next_q = max(next_q_values)
        else:
            max_next_q = 0
        
        # Current Q-value
        current_q = self.q_table[state][action]
        
        # Bellman equation update
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q
    
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
        
        # Select action using epsilon-greedy policy
        action = self._epsilon_greedy_action(state)
        
        # Store for learning
        self.current_state = state
        self.current_action = action
        
        return action
    
    def learn(self, power_levels, reward, collision_occurred=False):
        """
        Learn from the experience
        
        Args:
            power_levels: Power levels after action
            reward: Received reward
            collision_occurred: Whether a collision occurred
        """
        # Convert power levels to next state
        next_state = self._power_to_state(power_levels)
        
        # Update Q-value
        self._update_q_value(self.current_state, self.current_action, reward, next_state)
        
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
        
        # Decay epsilon
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
        
        # Log learning progress
        if self.episode_count % 100 == 0:
            self.logger.info(f"Episode {self.episode_count}: "
                           f"Total Reward={self.total_reward:.2f}, "
                           f"Collision Rate={self.collision_count/self.episode_count:.3f}, "
                           f"Epsilon={self.epsilon:.3f}")
    
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
                'epsilon': self.epsilon,
                'episode_count': 0
            }
        
        return {
            'total_reward': self.total_reward,
            'collision_rate': self.collision_count / self.episode_count,
            'success_rate': self.success_count / self.episode_count,
            'defer_rate': self.defer_count / self.episode_count,
            'epsilon': self.epsilon,
            'episode_count': self.episode_count
        }
    
    def save_q_table(self, filename=config.Q_TABLE_FILE):
        """
        Save Q-table to file
        
        Args:
            filename: File to save Q-table
        """
        # Convert defaultdict to regular dict for serialization
        q_table_dict = {}
        for state in self.q_table:
            q_table_dict[str(state)] = dict(self.q_table[state])
        
        with open(filename, 'wb') as f:
            pickle.dump(q_table_dict, f)
        
        self.logger.info(f"Q-table saved to {filename}")
    
    def load_q_table(self, filename=config.Q_TABLE_FILE):
        """
        Load Q-table from file
        
        Args:
            filename: File to load Q-table from
        """
        try:
            with open(filename, 'rb') as f:
                q_table_dict = pickle.load(f)
            
            # Convert back to defaultdict
            self.q_table.clear()
            for state_str, action_dict in q_table_dict.items():
                state = eval(state_str)  # Convert string back to tuple
                for action, q_value in action_dict.items():
                    self.q_table[state][int(action)] = q_value
            
            self.logger.info(f"Q-table loaded from {filename}")
        except FileNotFoundError:
            self.logger.warning(f"Q-table file {filename} not found, starting with empty table")
    
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
        """Reset agent statistics (keep Q-table)"""
        self.total_reward = 0
        self.collision_count = 0
        self.success_count = 0
        self.defer_count = 0
        self.episode_count = 0
        self.action_history = []
        self.reward_history = []
        self.state_history = []
        self.collision_history = []
        self.epsilon = config.INITIAL_EPSILON 