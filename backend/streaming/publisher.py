"""
Data Publisher - Publishes drilling data to the message broker
"""

import zmq
import json
from datetime import datetime
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Publisher')

class DataPublisher:
    """Publisher that sends drilling data to the broker."""
    
    def __init__(self, broker_address="tcp://localhost:5555"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.connect(broker_address)
        
        logger.info(f"📡 Publisher connected to broker at {broker_address}")
        time.sleep(0.5)  # Prevent slow joiner issue
    
    def publish(self, topic, data_dict):
        """Publish data with a specific topic."""
        message_data = data_dict.copy()
        message_data['timestamp'] = datetime.now().isoformat()
        
        message_json = json.dumps(message_data)
        full_message = f"{topic} {message_json}"
        self.socket.send_string(full_message)
        
        logger.debug(f"📤 Published [{topic}]: {list(data_dict.keys())}")
    
    def publish_drilling_data(self, data_dict):
        """Convenience method for general drilling data."""
        self.publish("drilling_data", data_dict)
    
    def publish_nse_data(self, data_dict):
        """Publish NSE (Near Surface Equipment) data."""
        self.publish("nse", data_dict)
    
    def publish_surface_data(self, data_dict):
        """Publish surface data."""
        self.publish("surface", data_dict)
    
    def close(self):
        """Clean shutdown."""
        self.socket.close()
        self.context.term()
        logger.info("📡 Publisher closed")
