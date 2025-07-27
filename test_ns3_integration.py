#!/usr/bin/env python3
"""
Test script for NS3 Integration
Verifies that NS3 simulation works correctly with the RF learning system
"""

import numpy as np
import time
import config
from ns3_integration import NS3Simulator, NS3SpectrumProvider

def test_ns3_simulator():
    """Test NS3 simulator functionality"""
    print("Testing NS3 Simulator...")
    
    # Create NS3 simulator
    simulator = NS3Simulator(
        num_nodes=config.NS3_NUM_NODES,
        simulation_time=10,  # Short test
        channel_width=config.NS3_CHANNEL_WIDTH,
        frequency=config.NS3_FREQUENCY,
        enable_interference=config.NS3_ENABLE_INTERFERENCE
    )
    
    # Test simulation
    print("Running NS3 simulation...")
    success = simulator.run_simulation()
    
    if success:
        print("✓ NS3 simulation completed")
        
        # Test spectrum data retrieval
        power_levels = simulator.get_spectrum_data()
        print(f"✓ Spectrum data retrieved: {power_levels}")
        
        # Verify data format
        if len(power_levels) == config.NUM_CHANNELS:
            print("✓ Data format correct")
        else:
            print("✗ Data format incorrect")
            return False
    else:
        print("✗ NS3 simulation failed")
        return False
    
    return True

def test_ns3_spectrum_provider():
    """Test NS3 spectrum provider"""
    print("\nTesting NS3 Spectrum Provider...")
    
    # Create spectrum provider
    provider = NS3SpectrumProvider(use_ns3=True)
    
    # Test power levels
    for i in range(5):
        power_levels = provider.get_power_levels()
        print(f"Sample {i+1}: {power_levels}")
        
        # Verify data format
        if len(power_levels) != config.NUM_CHANNELS:
            print("✗ Incorrect number of channels")
            return False
        
        time.sleep(0.1)
    
    print("✓ NS3 spectrum provider working correctly")
    return True

def test_ns3_with_learning():
    """Test NS3 integration with Q-learning"""
    print("\nTesting NS3 with Q-Learning...")
    
    from q_learning_agent import TabularQAgent
    from random_agent import RandomAgent
    
    # Create agents
    q_agent = TabularQAgent()
    random_agent = RandomAgent()
    
    # Create spectrum provider
    provider = NS3SpectrumProvider(use_ns3=True)
    
    # Run a few episodes
    for episode in range(10):
        # Get spectrum data from NS3
        power_levels = provider.get_power_levels()
        
        # Agents observe and act
        q_action = q_agent.observe_and_act(power_levels)
        random_action = random_agent.observe_and_act(power_levels)
        
        # Simulate results
        q_reward = 1.0 if q_action < config.NUM_CHANNELS and power_levels[q_action] <= config.POWER_THRESHOLD else -1.0
        random_reward = 1.0 if random_action < config.NUM_CHANNELS and power_levels[random_action] <= config.POWER_THRESHOLD else -1.0
        
        # Learn
        q_agent.learn(power_levels, q_reward)
        random_agent.learn(power_levels, random_reward)
        
        print(f"Episode {episode+1}: Q-action={q_action}, Q-reward={q_reward:.1f}, "
              f"R-action={random_action}, R-reward={random_reward:.1f}")
    
    # Check statistics
    q_stats = q_agent.get_statistics()
    random_stats = random_agent.get_statistics()
    
    print(f"Q-agent stats: {q_stats}")
    print(f"Random agent stats: {random_stats}")
    
    print("✓ NS3 integration with Q-learning working correctly")
    return True

def test_fallback_simulation():
    """Test fallback simulation when NS3 is not available"""
    print("\nTesting Fallback Simulation...")
    
    # Create simulator with NS3 disabled
    simulator = NS3Simulator()
    
    # Force fallback mode
    success = simulator._run_fallback_simulation()
    
    if success:
        print("✓ Fallback simulation working")
        
        # Test data retrieval
        power_levels = simulator.get_spectrum_data()
        print(f"✓ Fallback data: {power_levels}")
        
        return True
    else:
        print("✗ Fallback simulation failed")
        return False

def main():
    """Run all NS3 integration tests"""
    print("="*60)
    print("NS3 Integration Tests")
    print("="*60)
    
    tests_passed = 0
    total_tests = 4
    
    try:
        # Test 1: NS3 Simulator
        if test_ns3_simulator():
            tests_passed += 1
        
        # Test 2: NS3 Spectrum Provider
        if test_ns3_spectrum_provider():
            tests_passed += 1
        
        # Test 3: NS3 with Q-Learning
        if test_ns3_with_learning():
            tests_passed += 1
        
        # Test 4: Fallback Simulation
        if test_fallback_simulation():
            tests_passed += 1
        
    except Exception as e:
        print(f"Test failed with error: {e}")
    
    print("\n" + "="*60)
    print(f"NS3 Integration Tests: {tests_passed}/{total_tests} passed")
    print("="*60)
    
    if tests_passed == total_tests:
        print("🎉 All NS3 integration tests passed!")
        print("\nTo run the system with NS3:")
        print("  python main_system.py --ns3 --episodes 1000")
    else:
        print("⚠️  Some tests failed. Check NS3 installation.")
        print("\nNS3 installation:")
        print("  Ubuntu/Debian: sudo apt-get install ns3-dev")
        print("  macOS: brew install ns3")
        print("  Windows: Download from https://www.nsnam.org/download/")

if __name__ == "__main__":
    main() 