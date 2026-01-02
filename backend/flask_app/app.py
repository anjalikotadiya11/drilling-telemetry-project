"""
Flask Application - Web UI for Drilling Telemetry System
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streaming.subscriber import DataSubscriber
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('FlaskApp')

app = Flask(__name__, 
            template_folder='../../frontend/templates',
            static_folder='../../frontend/static')
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

class WebSocketBridge(DataSubscriber):
    """Subscribes to ZMQ and forwards to WebSocket clients."""
    
    def __init__(self):
        super().__init__(topics=["drilling_data"])
        logger.info("🌐 WebSocket Bridge initialized")
    
    def on_message(self, topic, data):
        """Forward ZMQ message to all WebSocket clients."""
        socketio.emit('drilling_update', {
            'topic': topic,
            'temperature': data.get('temperature'),
            'pressure': data.get('pressure'),
            'depth': data.get('depth'),
            'rpm': data.get('rpm'),
            'timestamp': data.get('timestamp'),
            'status': data.get('status', 'drilling')
        })

# Initialize bridge
bridge = WebSocketBridge()

@app.route('/')
def dashboard():
    """Serve the main dashboard page."""
    logger.info("Dashboard accessed")
    return render_template('dashboard.html')

@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'ok', 'service': 'drilling-telemetry'}

@socketio.on('connect')
def handle_connect():
    """Handle new WebSocket connection."""
    logger.info(f"Client connected")
    emit('status', {'message': 'Connected to drilling telemetry system'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection."""
    logger.info("Client disconnected")

def start_zmq_subscriber():
    """Start ZMQ subscriber in background thread."""
    logger.info("Starting ZMQ subscriber thread...")
    bridge.start()

if __name__ == '__main__':
    # Start ZMQ subscriber in background
    zmq_thread = threading.Thread(target=start_zmq_subscriber, daemon=True)
    zmq_thread.start()
    
    logger.info("=" * 60)
    logger.info("🚀 FLASK WEB UI STARTING")
    logger.info("=" * 60)
    logger.info("Dashboard: http://localhost:5000")
    logger.info("Health Check: http://localhost:5000/health")
    logger.info("=" * 60)
    
    # Start Flask-SocketIO server
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
