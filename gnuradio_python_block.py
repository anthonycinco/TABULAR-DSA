#!/usr/bin/env python3
"""
GNU Radio Python Block for RF Learning System
This block can be integrated into GNU Radio flowgraphs to export spectrum data
"""

import numpy as np
import struct
import time
import json
import os
from gnuradio import gr

class SpectrumExporter(gr.sync_block):
    """
    GNU Radio block that exports spectrum data for the RF learning system
    
    This block takes FFT power data and exports it in a format that can be
    read by the Python Q-learning system.
    """
    
    def __init__(self, num_channels=5, export_interval=0.1, output_file="spectrum_data.json"):
        """
        Initialize the spectrum exporter
        
        Args:
            num_channels: Number of channels to monitor
            export_interval: Time interval between exports (seconds)
            output_file: File to export data to
        """
        gr.sync_block.__init__(
            self,
            name="Spectrum Exporter",
            in_sig=[np.float32],  # FFT power data
            out_sig=[]  # No output
        )
        
        self.num_channels = num_channels
        self.export_interval = export_interval
        self.output_file = output_file
        
        # Timing
        self.last_export_time = 0
        
        # Data buffer
        self.fft_size = 1024  # Default FFT size
        self.data_buffer = []
        
        print(f"Spectrum Exporter initialized: {num_channels} channels, {export_interval}s interval")
    
    def work(self, input_items, output_items):
        """
        Process input data and export spectrum information
        
        Args:
            input_items: Input FFT power data
            output_items: Not used (no output)
        
        Returns:
            Number of items consumed
        """
        # Get input data
        fft_data = input_items[0]
        num_items = len(fft_data)
        
        # Add to buffer
        self.data_buffer.extend(fft_data)
        
        # Check if we have enough data for a complete FFT
        if len(self.data_buffer) >= self.fft_size:
            # Extract complete FFT
            fft_complete = self.data_buffer[:self.fft_size]
            self.data_buffer = self.data_buffer[self.fft_size:]
            
            # Check if it's time to export
            current_time = time.time()
            if current_time - self.last_export_time >= self.export_interval:
                self._export_spectrum_data(fft_complete)
                self.last_export_time = current_time
        
        return num_items
    
    def _export_spectrum_data(self, fft_data):
        """
        Export spectrum data to file
        
        Args:
            fft_data: Complete FFT power data
        """
        try:
            # Calculate power levels for each channel
            # Assuming FFT data is centered around 2.44 GHz
            # Divide spectrum into num_channels bands
            
            channel_bandwidth = len(fft_data) // self.num_channels
            power_levels = []
            
            for i in range(self.num_channels):
                start_idx = i * channel_bandwidth
                end_idx = start_idx + channel_bandwidth
                
                # Calculate average power for this channel
                channel_power = np.mean(fft_data[start_idx:end_idx])
                
                # Convert to dB
                if channel_power > 0:
                    power_db = 10 * np.log10(channel_power)
                else:
                    power_db = -100  # Very low power
                
                power_levels.append(power_db)
            
            # Create export data
            export_data = {
                'timestamp': time.time(),
                'power_levels': power_levels,
                'num_channels': self.num_channels,
                'fft_size': len(fft_data)
            }
            
            # Write to file (atomic write)
            temp_file = self.output_file + '.tmp'
            with open(temp_file, 'w') as f:
                json.dump(export_data, f)
            
            # Atomic move
            os.replace(temp_file, self.output_file)
            
            print(f"Exported spectrum data: {power_levels}")
            
        except Exception as e:
            print(f"Error exporting spectrum data: {e}")

# Alternative: Simple file sink for binary data
class SpectrumFileSink(gr.sync_block):
    """
    Simple file sink for spectrum data
    """
    
    def __init__(self, filename="spectrum_data.bin"):
        gr.sync_block.__init__(
            self,
            name="Spectrum File Sink",
            in_sig=[np.float32],
            out_sig=[]
        )
        
        self.filename = filename
        self.file_handle = None
        self._open_file()
    
    def _open_file(self):
        """Open output file"""
        try:
            self.file_handle = open(self.filename, 'wb')
            print(f"Opened spectrum file: {self.filename}")
        except Exception as e:
            print(f"Error opening file {self.filename}: {e}")
    
    def work(self, input_items, output_items):
        """Write data to file"""
        if self.file_handle is None:
            return 0
        
        try:
            # Write data as binary
            data = input_items[0].tobytes()
            self.file_handle.write(data)
            self.file_handle.flush()
            
            return len(input_items[0])
        except Exception as e:
            print(f"Error writing to file: {e}")
            return 0
    
    def stop(self):
        """Close file when block stops"""
        if self.file_handle:
            self.file_handle.close()
            print(f"Closed spectrum file: {self.filename}")

# Example usage in GNU Radio flowgraph:
"""
To use this in GNU Radio:

1. Add a Python Block to your flowgraph
2. Set the code to:
   import gnuradio_python_block
   self.spectrum_exporter = gnuradio_python_block.SpectrumExporter(
       num_channels=5,
       export_interval=0.1,
       output_file="spectrum_data.json"
   )
   return self.spectrum_exporter

3. Connect FFT power output to this block

4. The block will export spectrum data every 100ms to spectrum_data.json
"""

if __name__ == "__main__":
    # Test the exporter
    print("Testing Spectrum Exporter...")
    
    # Create test FFT data
    test_fft = np.random.random(1024) * 100
    
    # Create exporter
    exporter = SpectrumExporter(num_channels=5, export_interval=0.1)
    
    # Test export
    exporter._export_spectrum_data(test_fft)
    
    print("Test completed!") 