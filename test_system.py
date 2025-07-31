#!/usr/bin/env python3
"""
Test script for Simplified RF Learning System
Tests simulation and NS3 integration without hardware dependencies
"""

import sys
import os
import time
import numpy as np
import logging
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
from q_learning_agent import TabularQAgent
from random_agent import RandomAgent
from ns3_integration import NS3SpectrumProvider

def test_agents():
    """Test Q-learning and random agents"""
    print("Testing agents...")
    
    # Create agents
    q_agent = TabularQAgent()
    random_agent = RandomAgent()
    
    # Test with simulated data
    test_power_levels = [-65, -45, -70, -50, -68]
    
    # Test observation and action
    q_action = q_agent.observe_and_act(test_power_levels)
    random_action = random_agent.observe_and_act(test_power_levels)
    
    print(f"Q-Agent action: {q_action}")
    print(f"Random Agent action: {random_action}")
    
    # Test learning
    q_reward = 1.0
    q_collision = False
    random_reward = -1.0
    random_collision = True
    
    q_agent.learn(test_power_levels, q_reward, q_collision)
    random_agent.learn(test_power_levels, random_reward, random_collision)
    
    # Test statistics
    q_stats = q_agent.get_statistics()
    random_stats = random_agent.get_statistics()
    
    print(f"Q-Agent stats: {q_stats}")
    print(f"Random Agent stats: {random_stats}")
    
    print("Agent tests passed!")
    return True

def test_ns3_integration():
    """Test NS3 integration"""
    print("Testing NS3 integration...")
    
    try:
        # Create NS3 spectrum provider
        provider = NS3SpectrumProvider(use_ns3=True)
        
        # Test getting power levels
        power_levels = provider.get_power_levels()
        
        if power_levels and len(power_levels) == config.NUM_CHANNELS:
            print(f"NS3 power levels: {power_levels}")
            print("NS3 integration test passed!")
            return True
        else:
            print("NS3 integration test failed - invalid power levels")
            return False
            
    except Exception as e:
        print(f"NS3 integration test failed: {e}")
        print("This is expected if NS3 is not installed")
        return False

def test_simulation():
    """Test simulation mode"""
    print("Testing simulation mode...")
    
    try:
        # Create NS3 spectrum provider with fallback
        provider = NS3SpectrumProvider(use_ns3=False)
        
        # Test getting power levels
        power_levels = provider.get_power_levels()
        
        if power_levels and len(power_levels) == config.NUM_CHANNELS:
            print(f"Simulated power levels: {power_levels}")
            print("Simulation test passed!")
            return True
        else:
            print("Simulation test failed - invalid power levels")
            return False
            
    except Exception as e:
        print(f"Simulation test failed: {e}")
        return False

def test_configuration():
    """Test configuration parameters"""
    print("Testing configuration...")
    
    required_params = [
        'NUM_CHANNELS', 'SENSING_INTERVAL', 'POWER_THRESHOLD',
        'LEARNING_RATE', 'DISCOUNT_FACTOR', 'SUCCESS_REWARD',
        'COLLISION_PENALTY', 'DEFER_REWARD'
    ]
    
    for param in required_params:
        if not hasattr(config, param):
            print(f"Configuration test failed - missing {param}")
            return False
    
    print("Configuration test passed!")
    return True

def run_quick_simulation():
    """Run a quick simulation to test the system"""
    print("Running quick simulation...")
    
    try:
        from main_system import RFLearningSystem
        
        # Create system with simulation
        system = RFLearningSystem(use_ns3=False, load_q_table=False)
        
        # Run for a few episodes
        system.run(max_episodes=10, max_time=5)
        
        print("Quick simulation completed successfully!")
        return True
        
    except Exception as e:
        print(f"Quick simulation failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("Simplified RF Learning System - Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now()}")
    print()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    tests = [
        ("Configuration", test_configuration),
        ("Agents", test_agents),
        ("Simulation", test_simulation),
        ("NS3 Integration", test_ns3_integration),
        ("Quick Simulation", run_quick_simulation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} test PASSED")
            else:
                print(f"✗ {test_name} test FAILED")
        except Exception as e:
            print(f"✗ {test_name} test FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("All tests passed! System is ready for use.")
        print("\nTo run the system:")
        print("  python main_system.py                    # Basic simulation")
        print("  python main_system.py --ns3              # NS3 simulation")
        print("  python main_system.py --episodes 100     # Run 100 episodes")
        print("  python main_system.py --time 60          # Run for 60 seconds")
    else:
        print("Some tests failed. Please check the output above.")
        print("The system may still work for basic simulation mode.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 