"""
Message Broker - Central Hub for Data Distribution
Forwards messages from publishers to all subscribers using ZeroMQ proxy.
"""

import zmq
import sys
import signal
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('Broker')

class StreamingBroker:
    """ZeroMQ pub-sub proxy for message distribution."""
    
    def __init__(self, frontend_port=5555, backend_port=5556):
        self.frontend_port = frontend_port
        self.backend_port = backend_port
        self.context = zmq.Context()
        self.running = False
        
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully."""
        logger.info("Shutdown signal received")
        self.running = False
    
    def start(self):
        """Start the broker and begin forwarding messages."""
        logger.info("=" * 50)
        logger.info("🚀 STREAMING BROKER STARTING")
        logger.info("=" * 50)
        
        # FRONTEND: Receives messages from publishers
        frontend = self.context.socket(zmq.SUB)
        frontend.bind(f"tcp://*:{self.frontend_port}")
        frontend.subscribe("")  # Subscribe to ALL messages
        logger.info(f"📥 Frontend listening on port {self.frontend_port}")
        
        # BACKEND: Sends messages to subscribers
        backend = self.context.socket(zmq.PUB)
        backend.bind(f"tcp://*:{self.backend_port}")
        logger.info(f"📤 Backend publishing on port {self.backend_port}")
        
        logger.info("✅ Broker is running! Press Ctrl+C to stop.\n")
        self.running = True
        
        try:
            zmq.proxy(frontend, backend)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logger.error(f"Broker error: {e}")
        finally:
            logger.info("🧹 Cleaning up...")
            frontend.close()
            backend.close()
            self.context.term()
            logger.info("✅ Broker stopped cleanly")

def main():
    """Run the broker as a standalone service."""
    broker = StreamingBroker(
        frontend_port=5555,
        backend_port=5556
    )
    broker.start()

if __name__ == "__main__":
    main()
