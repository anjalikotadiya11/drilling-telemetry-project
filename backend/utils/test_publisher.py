"""
Test Publisher - Simulates drilling data for testing
"""

import time
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streaming.publisher import DataPublisher
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('TestPublisher')

def simulate_drilling_operation():
    """Simulates a realistic drilling operation."""
    publisher = DataPublisher()
    
    logger.info("=" * 60)
    logger.info("🧪 TEST PUBLISHER - Simulating Drilling Operation")
    logger.info("=" * 60)
    logger.info("Press Ctrl+C to stop\n")
    
    depth = 5000.0
    base_temperature = 250.0
    base_pressure = 1500.0
    base_rpm = 120
    
    message_count = 0
    
    try:
        while True:
            message_count += 1
            
            depth += random.uniform(0.5, 2.0)
            temperature = base_temperature + (depth - 5000) * 0.01
            temperature += random.uniform(-10, 10)
            
            if random.random() < 0.05:
                temperature += random.uniform(50, 100)
                logger.info("🔥 Simulating temperature spike!")
            
            pressure = base_pressure + random.uniform(-50, 50)
            
            if random.random() < 0.03:
                pressure += random.uniform(200, 400)
                logger.info("💥 Simulating pressure surge!")
            
            rpm = base_rpm + random.randint(-10, 10)
            
            data = {
                "temperature": round(temperature, 2),
                "pressure": round(pressure, 2),
                "depth": round(depth, 2),
                "rpm": rpm,
                "tool_id": "DRILL_001",
                "operator": "Test_Operator",
                "status": "drilling"
            }
            
            publisher.publish_drilling_data(data)
            
            logger.info(f"📊 Message #{message_count} | "
                  f"Depth: {depth:.1f}ft | "
                  f"Temp: {temperature:.1f}° | "
                  f"Pressure: {pressure:.1f} PSI")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        logger.info(f"\n📊 Total messages sent: {message_count}")
        publisher.close()
        logger.info("✅ Test publisher stopped cleanly")

if __name__ == "__main__":
    simulate_drilling_operation()
