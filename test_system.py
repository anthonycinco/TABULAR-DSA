#!/usr/bin/env python3
"""
Test script for RF Learning System
Verifies that all components work correctly
"""

import numpy as np
import time
import config
from q_learning_agent import TabularQAgent
from random_agent import RandomAgent

def test_agents():
    """Test Q-learning and Random agents"""
    print("Testing agents...")
    
    # Create agents
    q_agent = TabularQAgent()
    random_agent = RandomAgent()
    
    # Test power level conversion
    power_levels = [-65, -45, -70, -50, -75]  # Mix of busy and idle channels
    print(f"Power levels: {power_levels}")
    
    # Test state conversion
    q_state = q_agent._power_to_state(power_levels)
    random_state = random_agent._power_to_state(power_levels)
    print(f"State (Q-agent): {q_state}")
    print(f"State (Random agent): {random_state}")
    
    # Test action selection
    q_action = q_agent.observe_and_act(power_levels)
    random_action = random_agent.observe_and_act(power_levels)
    print(f"Q-agent action: {q_action}")
    print(f"Random agent action: {q_action}")
    
    # Test learning
    q_agent.learn(power_levels, 1.0, False)  # Success
    random_agent.learn(power_levels, -1.0, True)  # Collision
    
    # Test statistics
    q_stats = q_agent.get_statistics()
    random_stats = random_agent.get_statistics()
    print(f"Q-agent stats: {q_stats}")
    print(f"Random agent stats: {random_stats}")
    
    print("Agent tests passed!\n")

def test_learning():
    """Test learning process"""
    print("Testing learning process...")
    
    q_agent = TabularQAgent()
    
    # Run some episodes
    for episode in range(100):
        # Simulate power levels
        power_levels = np.random.normal(-60, 10, config.NUM_CHANNELS)
        
        # Agent observes and acts
        action = q_agent.observe_and_act(power_levels)
        
        # Simulate result
        if action < config.NUM_CHANNELS:
            # Check if channel is busy
            is_busy = power_levels[action] > config.POWER_THRESHOLD
            reward = config.COLLISION_PENALTY if is_busy else config.SUCCESS_REWARD
            collision = is_busy
        else:
            reward = config.DEFER_REWARD
            collision = False
        
        # Learn
        q_agent.learn(power_levels, reward, collision)
    
    # Check final statistics
    stats = q_agent.get_statistics()
    print(f"After 100 episodes:")
    print(f"  Total reward: {stats['total_reward']:.2f}")
    print(f"  Collision rate: {stats['collision_rate']:.3f}")
    print(f"  Success rate: {stats['success_rate']:.3f}")
    print(f"  Epsilon: {q_agent.epsilon:.3f}")
    
    print("Learning test passed!\n")

def test_simulation():
    """Test simulation mode"""
    print("Testing simulation mode...")
    
    from main_system import RFLearningSystem
    
    # Create system in simulation mode
    system = RFLearningSystem(simulate=True)
    
    # Run a few episodes
    for i in range(10):
        result = system._run_episode()
        print(f"Episode {i+1}: Q-reward={result['q_reward']:.2f}, R-reward={result['random_reward']:.2f}")
    
    print("Simulation test passed!\n")

def main():
    """Run all tests"""
    print("="*50)
    print("RF Learning System Tests")
    print("="*50)
    
    try:
        test_agents()
        test_learning()
        test_simulation()
        
        print("All tests passed! ✅")
        print("\nTo run the full system:")
        print("  python main_system.py --simulate --episodes 1000")
        print("\nTo create GNU Radio flowgraph:")
        print("  python main_system.py --create-flowgraph")
        
    except Exception as e:
        print(f"Test failed: {e}")
        raise

if __name__ == "__main__":
    main() 