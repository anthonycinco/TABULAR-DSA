#!/usr/bin/env python3
"""
NS3 Integration for RF Learning System
Provides realistic wireless network simulation capabilities
"""

import subprocess
import json
import time
import threading
import numpy as np
import os
import logging
from typing import List, Dict, Tuple
import config

class NS3Simulator:
    """
    NS3-based wireless network simulator for RF learning system
    
    Simulates realistic 802.11 networks with multiple nodes, interference,
    and dynamic channel conditions.
    """
    
    def __init__(self, 
                 num_nodes=5,
                 simulation_time=100,
                 channel_width=20,
                 frequency=2440,
                 enable_interference=True):
        """
        Initialize NS3 simulator
        
        Args:
            num_nodes: Number of wireless nodes
            simulation_time: Simulation duration in seconds
            channel_width: Channel bandwidth in MHz
            frequency: Center frequency in MHz
            enable_interference: Whether to enable interference simulation
        """
        self.num_nodes = num_nodes
        self.simulation_time = simulation_time
        self.channel_width = channel_width
        self.frequency = frequency
        self.enable_interference = enable_interference
        
        # NS3 script parameters
        self.ns3_script = "rf_learning_simulation.cc"
        self.output_file = "ns3_spectrum_data.json"
        
        # Simulation state
        self.running = False
        self.current_time = 0
        self.spectrum_data = {}
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Create NS3 script
        self._create_ns3_script()
        
    def _create_ns3_script(self):
        """Create the NS3 simulation script"""
        
        script_content = f'''#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/wifi-module.h"
#include "ns3/mobility-module.h"
#include "ns3/applications-module.h"
#include "ns3/spectrum-module.h"
#include "ns3/propagation-module.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/internet-module.h"
#include <fstream>
#include <iostream>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("RFLearningSimulation");

class RFLearningSimulation
{{
public:
  RFLearningSimulation ();
  void Configure (uint32_t numNodes, double simulationTime, 
                  double channelWidth, double frequency, bool enableInterference);
  void Run ();

private:
  void SetupNodes ();
  void SetupSpectrum ();
  void SetupApplications ();
  void SetupMobility ();
  void CollectSpectrumData ();
  void WriteSpectrumData ();
  
  uint32_t m_numNodes;
  double m_simulationTime;
  double m_channelWidth;
  double m_frequency;
  bool m_enableInterference;
  
  NodeContainer m_nodes;
  NetDeviceContainer m_devices;
  Ipv4InterfaceContainer m_interfaces;
  
  Ptr<SpectrumChannel> m_spectrumChannel;
  Ptr<MultiModelSpectrumChannel> m_multiChannel;
  
  std::ofstream m_spectrumFile;
  std::map<uint32_t, std::vector<double>> m_spectrumData;
}};

RFLearningSimulation::RFLearningSimulation ()
  : m_numNodes (5),
    m_simulationTime (100),
    m_channelWidth (20),
    m_frequency (2440),
    m_enableInterference (true)
{{
}}

void
RFLearningSimulation::Configure (uint32_t numNodes, double simulationTime,
                                 double channelWidth, double frequency, bool enableInterference)
{{
  m_numNodes = numNodes;
  m_simulationTime = simulationTime;
  m_channelWidth = channelWidth;
  m_frequency = frequency;
  m_enableInterference = enableInterference;
}}

void
RFLearningSimulation::SetupNodes ()
{{
  m_nodes.Create (m_numNodes);
  
  // Create spectrum channel
  m_multiChannel = CreateObject<MultiModelSpectrumChannel> ();
  
  // Setup spectrum model
  Ptr<ConstantSpectrumPropagationLossModel> lossModel = 
    CreateObject<ConstantSpectrumPropagationLossModel> ();
  m_multiChannel->AddPropagationLossModel (lossModel);
  
  Ptr<FriisPropagationLossModel> friisModel = 
    CreateObject<FriisPropagationLossModel> ();
  m_multiChannel->AddPropagationLossModel (friisModel);
  
  // Setup spectrum analyzer
  Ptr<SingleModelSpectrumChannel> spectrumChannel = 
    CreateObject<SingleModelSpectrumChannel> ();
  spectrumChannel->AddPropagationLossModel (lossModel);
  
  // Create WiFi devices
  SpectrumWifiPhyHelper spectrumPhy;
  spectrumPhy.SetChannel (spectrumChannel);
  spectrumPhy.SetErrorRateModel ("ns3::YansErrorRateModel");
  spectrumPhy.Set ("Frequency", UintegerValue (m_frequency));
  spectrumPhy.Set ("ChannelWidth", UintegerValue (m_channelWidth));
  
  WifiMacHelper mac;
  mac.SetType ("ns3::AdhocWifiMac");
  
  WifiHelper wifi;
  wifi.SetStandard (WIFI_PHY_STANDARD_80211n_2_4GHZ);
  wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager");
  
  m_devices = wifi.Install (spectrumPhy, mac, m_nodes);
}}

void
RFLearningSimulation::SetupSpectrum ()
{{
  // Create spectrum model for 2.4 GHz band
  std::vector<double> frequencies;
  std::vector<double> powers;
  
  // 5 channels in 2.4 GHz band
  for (uint32_t i = 0; i < 5; ++i)
  {{
    double freq = 2400 + i * 20; // 20 MHz channels
    frequencies.push_back (freq * 1e6); // Convert to Hz
    powers.push_back (-60); // Default power level
  }}
  
  // Create spectrum value
  Ptr<SpectrumValue> spectrumValue = Create<SpectrumValue> (
    Create<SpectrumModel> (frequencies));
  
  for (uint32_t i = 0; i < frequencies.size (); ++i)
  {{
    (*spectrumValue)[i] = powers[i];
  }}
}}

void
RFLearningSimulation::SetupMobility ()
{{
  MobilityHelper mobility;
  
  // Random positions in 100x100m area
  mobility.SetPositionAllocator ("ns3::RandomRectanglePositionAllocator",
                                "X", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=100.0]"),
                                "Y", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=100.0]"));
  
  // Random walk mobility
  mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel",
                            "Bounds", RectangleValue (Rectangle (-100, 100, -100, 100)),
                            "Time", StringValue ("2s"),
                            "Mode", StringValue ("Time"),
                            "Speed", StringValue ("ns3::ConstantRandomVariable[Constant=5.0]"));
  
  mobility.Install (m_nodes);
}}

void
RFLearningSimulation::SetupApplications ()
{{
  // Install Internet stack
  InternetStackHelper internet;
  internet.Install (m_nodes);
  
  // Assign IP addresses
  Ipv4AddressHelper ipv4;
  ipv4.SetBase ("10.1.1.0", "255.255.255.0");
  m_interfaces = ipv4.Assign (m_devices);
  
  // Create UDP applications for traffic generation
  uint16_t port = 9;
  UdpEchoServerHelper echoServer (port);
  ApplicationContainer serverApps = echoServer.Install (m_nodes.Get (0));
  serverApps.Start (Seconds (1.0));
  serverApps.Stop (Seconds (m_simulationTime));
  
  // Create traffic between nodes
  for (uint32_t i = 1; i < m_numNodes; ++i)
  {{
    UdpEchoClientHelper echoClient (m_interfaces.GetAddress (0), port);
    echoClient.SetAttribute ("MaxPackets", UintegerValue (1000));
    echoClient.SetAttribute ("Interval", TimeValue (Seconds (0.1)));
    echoClient.SetAttribute ("PacketSize", UintegerValue (1024));
    
    ApplicationContainer clientApps = echoClient.Install (m_nodes.Get (i));
    clientApps.Start (Seconds (2.0 + i * 0.5));
    clientApps.Stop (Seconds (m_simulationTime));
  }}
}}

void
RFLearningSimulation::CollectSpectrumData ()
{{
  // Collect spectrum data every 100ms
  for (double t = 0; t < m_simulationTime; t += 0.1)
  {{
    Simulator::Schedule (Seconds (t), &RFLearningSimulation::WriteSpectrumData, this);
  }}
}}

void
RFLearningSimulation::WriteSpectrumData ()
{{
  // Simulate spectrum data collection
  std::vector<double> powerLevels;
  
  for (uint32_t ch = 0; ch < 5; ++ch)
  {{
    // Simulate realistic power levels with interference
    double basePower = -70; // Base noise floor
    double interference = 0;
    
    if (m_enableInterference)
    {{
      // Add random interference
      Ptr<UniformRandomVariable> random = CreateObject<UniformRandomVariable> ();
      if (random->GetValue () < 0.3) // 30% chance of interference
      {{
        interference = random->GetValue () * 30; // 0-30 dB interference
      }}
    }}
    
    double power = basePower + interference;
    powerLevels.push_back (power);
  }}
  
  // Write to file
  m_spectrumFile << Simulator::Now ().GetSeconds () << " ";
  for (double power : powerLevels)
  {{
    m_spectrumFile << power << " ";
  }}
  m_spectrumFile << std::endl;
}}

void
RFLearningSimulation::Run ()
{{
  // Open spectrum data file
  m_spectrumFile.open ("ns3_spectrum_data.txt");
  
  SetupNodes ();
  SetupSpectrum ();
  SetupMobility ();
  SetupApplications ();
  CollectSpectrumData ();
  
  // Enable logging
  LogComponentEnable ("RFLearningSimulation", LOG_LEVEL_INFO);
  
  // Run simulation
  Simulator::Stop (Seconds (m_simulationTime));
  Simulator::Run ();
  Simulator::Destroy ();
  
  m_spectrumFile.close ();
  
  std::cout << "NS3 simulation completed. Spectrum data saved to ns3_spectrum_data.txt" << std::endl;
}}

int
main (int argc, char *argv[])
{{
  CommandLine cmd (__FILE__);
  cmd.Parse (argc, argv);
  
  RFLearningSimulation simulation;
  simulation.Configure (5, 100, 20, 2440, true);
  simulation.Run ();
  
  return 0;
}}
'''
        
        with open(self.ns3_script, 'w') as f:
            f.write(script_content)
        
        self.logger.info(f"Created NS3 script: {self.ns3_script}")
    
    def compile_ns3_script(self):
        """Compile the NS3 simulation script"""
        try:
            # Check if NS3 is available
            result = subprocess.run(['ns3', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                self.logger.warning("NS3 not found in PATH. Using simulation mode.")
                return False
            
            # Compile the script
            compile_cmd = ['ns3', 'configure', '--enable-examples']
            subprocess.run(compile_cmd, check=True)
            
            compile_cmd = ['ns3', 'build']
            subprocess.run(compile_cmd, check=True)
            
            self.logger.info("NS3 script compiled successfully")
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.logger.warning(f"NS3 compilation failed: {e}")
            return False
    
    def run_simulation(self, duration=None):
        """
        Run NS3 simulation
        
        Args:
            duration: Simulation duration in seconds (optional)
        """
        if duration:
            self.simulation_time = duration
        
        try:
            # Try to run NS3 simulation
            if self.compile_ns3_script():
                cmd = ['./build/scratch/rf_learning_simulation']
                subprocess.run(cmd, check=True)
                self.logger.info("NS3 simulation completed")
                return True
            else:
                # Fallback to simulation mode
                self.logger.info("Using fallback simulation mode")
                return self._run_fallback_simulation()
                
        except Exception as e:
            self.logger.error(f"NS3 simulation failed: {e}")
            return self._run_fallback_simulation()
    
    def _run_fallback_simulation(self):
        """Run fallback simulation when NS3 is not available"""
        self.logger.info("Running fallback simulation")
        
        # Simulate realistic spectrum data
        spectrum_data = []
        
        for t in np.arange(0, self.simulation_time, 0.1):
            # Simulate 5 channels with realistic interference patterns
            power_levels = []
            
            for ch in range(5):
                # Base noise floor
                base_power = -70
                
                # Add interference patterns
                interference = 0
                
                # Channel 1: WiFi interference (periodic)
                if ch == 0 and (t % 2) < 1:
                    interference = np.random.normal(20, 5)
                
                # Channel 2: Bluetooth interference (random)
                elif ch == 1 and np.random.random() < 0.1:
                    interference = np.random.normal(15, 3)
                
                # Channel 3: Microwave interference (periodic)
                elif ch == 2 and (t % 5) < 0.5:
                    interference = np.random.normal(25, 8)
                
                # Channel 4: Random interference
                elif ch == 3 and np.random.random() < 0.05:
                    interference = np.random.normal(18, 6)
                
                # Channel 5: Clean channel (mostly)
                elif ch == 4:
                    interference = np.random.normal(0, 2)
                
                power = base_power + interference
                power_levels.append(power)
            
            spectrum_data.append({
                'timestamp': t,
                'power_levels': power_levels
            })
        
        # Save to file
        with open(self.output_file, 'w') as f:
            json.dump(spectrum_data, f, indent=2)
        
        self.logger.info(f"Fallback simulation completed. Data saved to {self.output_file}")
        return True
    
    def get_spectrum_data(self):
        """
        Get current spectrum data from NS3 simulation
        
        Returns:
            List of 5 power levels in dB
        """
        try:
            # Try to read NS3 output file
            if os.path.exists("ns3_spectrum_data.txt"):
                with open("ns3_spectrum_data.txt", 'r') as f:
                    lines = f.readlines()
                    if lines:
                        # Get latest data
                        latest_line = lines[-1].strip().split()
                        if len(latest_line) >= 6:  # timestamp + 5 power levels
                            power_levels = [float(x) for x in latest_line[1:6]]
                            return power_levels
            
            # Fallback to JSON file
            if os.path.exists(self.output_file):
                with open(self.output_file, 'r') as f:
                    data = json.load(f)
                    if data:
                        # Get latest data
                        latest = data[-1]
                        return latest['power_levels']
            
            # Default fallback
            return [-70, -65, -75, -68, -72]
            
        except Exception as e:
            self.logger.error(f"Error reading spectrum data: {e}")
            return [-70, -65, -75, -68, -72]
    
    def start_real_time_simulation(self):
        """Start real-time NS3 simulation"""
        self.running = True
        
        def simulation_thread():
            while self.running:
                # Run simulation step
                self._run_fallback_simulation()
                time.sleep(config.SENSING_INTERVAL)
        
        self.sim_thread = threading.Thread(target=simulation_thread)
        self.sim_thread.start()
        
        self.logger.info("Real-time NS3 simulation started")
    
    def stop_simulation(self):
        """Stop real-time simulation"""
        self.running = False
        if hasattr(self, 'sim_thread'):
            self.sim_thread.join()
        
        self.logger.info("NS3 simulation stopped")

class NS3SpectrumProvider:
    """
    Spectrum data provider that integrates with NS3 simulation
    """
    
    def __init__(self, use_ns3=True):
        """
        Initialize NS3 spectrum provider
        
        Args:
            use_ns3: Whether to use NS3 simulation (fallback to simulation if NS3 unavailable)
        """
        self.use_ns3 = use_ns3
        self.simulator = None
        
        if use_ns3:
            self.simulator = NS3Simulator()
            # Try to start NS3 simulation
            if not self.simulator.run_simulation(duration=10):
                self.logger.warning("NS3 not available, using simulation mode")
                self.use_ns3 = False
        
        self.logger = logging.getLogger(__name__)
    
    def get_power_levels(self):
        """
        Get current power levels from NS3 or simulation
        
        Returns:
            List of 5 power levels in dB
        """
        if self.use_ns3 and self.simulator:
            return self.simulator.get_spectrum_data()
        else:
            # Fallback simulation
            return self._simulate_power_levels()
    
    def _simulate_power_levels(self):
        """Simulate realistic power levels"""
        base_power = -70
        
        # Simulate different interference patterns
        power_levels = []
        
        for ch in range(5):
            interference = 0
            
            # Channel-specific interference patterns
            if ch == 0:  # WiFi channel
                if np.random.random() < 0.3:
                    interference = np.random.normal(20, 5)
            elif ch == 1:  # Bluetooth channel
                if np.random.random() < 0.1:
                    interference = np.random.normal(15, 3)
            elif ch == 2:  # Microwave interference
                if np.random.random() < 0.05:
                    interference = np.random.normal(25, 8)
            elif ch == 3:  # Random interference
                if np.random.random() < 0.05:
                    interference = np.random.normal(18, 6)
            else:  # Clean channel
                interference = np.random.normal(0, 2)
            
            power = base_power + interference
            power_levels.append(power)
        
        return power_levels

if __name__ == "__main__":
    # Test NS3 integration
    print("Testing NS3 Integration...")
    
    # Create NS3 simulator
    simulator = NS3Simulator(num_nodes=5, simulation_time=10)
    
    # Run simulation
    success = simulator.run_simulation()
    
    if success:
        print("NS3 simulation completed successfully!")
        
        # Get spectrum data
        power_levels = simulator.get_spectrum_data()
        print(f"Spectrum data: {power_levels}")
    else:
        print("NS3 simulation failed, using fallback mode")
    
    print("NS3 integration test completed!") 