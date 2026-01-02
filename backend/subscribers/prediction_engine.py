"""
Prediction Engine - Analyzes data and detects anomalies
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streaming.subscriber import DataSubscriber
from collections import deque
import statistics
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('PredictionEngine')

class PredictionEngine(DataSubscriber):
    """Monitors drilling data and predicts potential issues."""
    
    def __init__(self, window_size=10):
        super().__init__(topics=["drilling_data"])
        
        self.temperature_window = deque(maxlen=window_size)
        self.pressure_window = deque(maxlen=window_size)
        self.depth_window = deque(maxlen=window_size)
        
        self.alert_count = 0
        logger.info(f"🔮 Prediction engine initialized (window size: {window_size})")
    
    def on_message(self, topic, data):
        """Analyze incoming data."""
        if 'temperature' in data:
            self.temperature_window.append(data['temperature'])
        if 'pressure' in data:
            self.pressure_window.append(data['pressure'])
        if 'depth' in data:
            self.depth_window.append(data['depth'])
        
        self.check_temperature_anomaly()
        self.check_pressure_anomaly()
    
    def check_temperature_anomaly(self):
        """Check if temperature is unusual."""
        if len(self.temperature_window) < 5:
            return
        
        avg_temp = statistics.mean(self.temperature_window)
        latest_temp = self.temperature_window[-1]
        
        if latest_temp > avg_temp * 1.2:
            self.alert_count += 1
            logger.warning(f"⚠️  ALERT #{self.alert_count}: Temperature spike!")
            logger.warning(f"   Average: {avg_temp:.1f}°, Current: {latest_temp:.1f}°")
    
    def check_pressure_anomaly(self):
        """Check if pressure is unusual."""
        if len(self.pressure_window) < 5:
            return
        
        avg_pressure = statistics.mean(self.pressure_window)
        latest_pressure = self.pressure_window[-1]
        
        if latest_pressure > avg_pressure * 1.15:
            self.alert_count += 1
            logger.warning(f"⚠️  ALERT #{self.alert_count}: Pressure increase!")
            logger.warning(f"   Average: {avg_pressure:.1f} PSI, Current: {latest_pressure:.1f} PSI")

def main():
    engine = PredictionEngine()
    engine.start()

if __name__ == "__main__":
    main()
