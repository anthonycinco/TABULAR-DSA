#include "ns3/core-module.h"
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
{
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
};

RFLearningSimulation::RFLearningSimulation ()
  : m_numNodes (5),
    m_simulationTime (100),
    m_channelWidth (20),
    m_frequency (2440),
    m_enableInterference (true)
{
}

void
RFLearningSimulation::Configure (uint32_t numNodes, double simulationTime,
                                 double channelWidth, double frequency, bool enableInterference)
{
  m_numNodes = numNodes;
  m_simulationTime = simulationTime;
  m_channelWidth = channelWidth;
  m_frequency = frequency;
  m_enableInterference = enableInterference;
}

void
RFLearningSimulation::SetupNodes ()
{
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
}

void
RFLearningSimulation::SetupSpectrum ()
{
  // Create spectrum model for 2.4 GHz band
  std::vector<double> frequencies;
  std::vector<double> powers;
  
  // 5 channels in 2.4 GHz band
  for (uint32_t i = 0; i < 5; ++i)
  {
    double freq = 2400 + i * 20; // 20 MHz channels
    frequencies.push_back (freq * 1e6); // Convert to Hz
    powers.push_back (-60); // Default power level
  }
  
  // Create spectrum value
  Ptr<SpectrumValue> spectrumValue = Create<SpectrumValue> (
    Create<SpectrumModel> (frequencies));
  
  for (uint32_t i = 0; i < frequencies.size (); ++i)
  {
    (*spectrumValue)[i] = powers[i];
  }
}

void
RFLearningSimulation::SetupMobility ()
{
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
}

void
RFLearningSimulation::SetupApplications ()
{
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
  {
    UdpEchoClientHelper echoClient (m_interfaces.GetAddress (0), port);
    echoClient.SetAttribute ("MaxPackets", UintegerValue (1000));
    echoClient.SetAttribute ("Interval", TimeValue (Seconds (0.1)));
    echoClient.SetAttribute ("PacketSize", UintegerValue (1024));
    
    ApplicationContainer clientApps = echoClient.Install (m_nodes.Get (i));
    clientApps.Start (Seconds (2.0 + i * 0.5));
    clientApps.Stop (Seconds (m_simulationTime));
  }
}

void
RFLearningSimulation::CollectSpectrumData ()
{
  // Collect spectrum data every 100ms
  for (double t = 0; t < m_simulationTime; t += 0.1)
  {
    Simulator::Schedule (Seconds (t), &RFLearningSimulation::WriteSpectrumData, this);
  }
}

void
RFLearningSimulation::WriteSpectrumData ()
{
  // Simulate spectrum data collection
  std::vector<double> powerLevels;
  
  for (uint32_t ch = 0; ch < 5; ++ch)
  {
    // Simulate realistic power levels with interference
    double basePower = -70; // Base noise floor
    double interference = 0;
    
    if (m_enableInterference)
    {
      // Add random interference
      Ptr<UniformRandomVariable> random = CreateObject<UniformRandomVariable> ();
      if (random->GetValue () < 0.3) // 30% chance of interference
      {
        interference = random->GetValue () * 30; // 0-30 dB interference
      }
    }
    
    double power = basePower + interference;
    powerLevels.push_back (power);
  }
  
  // Write to file
  m_spectrumFile << Simulator::Now ().GetSeconds () << " ";
  for (double power : powerLevels)
  {
    m_spectrumFile << power << " ";
  }
  m_spectrumFile << std::endl;
}

void
RFLearningSimulation::Run ()
{
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
}

int
main (int argc, char *argv[])
{
  CommandLine cmd (__FILE__);
  cmd.Parse (argc, argv);
  
  RFLearningSimulation simulation;
  simulation.Configure (5, 100, 20, 2440, true);
  simulation.Run ();
  
  return 0;
}
