"""
Base Subscriber Class - Template for all data consumers
"""

import zmq
import json
from abc import ABC, abstractmethod
import signal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Subscriber')

class DataSubscriber(ABC):
    """Base class for all subscribers."""
    
    def __init__(self, broker_address="tcp://localhost:5556", topics=None):
        self.broker_address = broker_address
        self.topics = topics or [""]
        self.running = False
        
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(broker_address)
        
        for topic in self.topics:
            self.socket.subscribe(topic)
            if topic == "":
                logger.info(f"📻 Subscribed to: ALL TOPICS")
            else:
                logger.info(f"📻 Subscribed to: '{topic}'")
        
        logger.info(f"👂 Subscriber connected to {broker_address}")
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully."""
        logger.info("Stopping subscriber...")
        self.stop()
    
    def start(self):
        """Start listening for messages."""
        self.running = True
        logger.info("✅ Subscriber started! Press Ctrl+C to stop.\n")
        
        try:
            while self.running:
                message = self.socket.recv_string()
                
                try:
                    topic, data_json = message.split(" ", 1)
                    data = json.loads(data_json)
                    self.on_message(topic, data)
                except Exception as e:
                    logger.error(f"❌ Error parsing message: {e}")
                    continue
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
    
    def stop(self):
        """Clean shutdown."""
        self.running = False
        self.socket.close()
        self.context.term()
        logger.info("✅ Subscriber stopped")
    
    @abstractmethod
    def on_message(self, topic, data):
        """Override this method to handle incoming messages."""
        pass
