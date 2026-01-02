# 🛢️ Drilling Telemetry System

Real-time oil drilling telemetry, analytics, and prediction platform with streaming infrastructure and live web visualization.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Features

- **Real-time Data Streaming** - ZeroMQ pub/sub architecture for low-latency data distribution
- **Live Web Dashboard** - Flask + Plotly.js for interactive, real-time visualization
- **Database Persistence** - SQLite storage with WAL mode for concurrent access
- **Prediction Engine** - Real-time anomaly detection and alerting
- **Offline Capable** - Designed for remote drilling sites without internet
- **Production Ready** - Error handling, logging, health monitoring

## 📁 Project Structure

```
drilling-telemetry-project/
├── backend/
│   ├── streaming/              # Task 1 & 2: Streaming infrastructure
│   │   ├── broker.py           # Central message broker
│   │   ├── publisher.py        # Data publisher class
│   │   └── subscriber.py       # Base subscriber class
│   ├── subscribers/            # Data consumers
│   │   ├── db_saver.py         # SQLite persistence
│   │   ├── console_logger.py   # Terminal logger
│   │   └── prediction_engine.py # Anomaly detection
│   ├── flask_app/              # Task 3: Web UI
│   │   ├── app.py              # Flask server
│   │   ├── websocket_bridge.py # ZMQ to WebSocket bridge
│   │   └── routes.py           # API endpoints
│   └── utils/
│       ├── monitor.py          # System health check
│       └── test_publisher.py   # Data simulator
├── frontend/                   # Web UI
│   ├── templates/
│   │   └── dashboard.html      # Main dashboard
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── public/
├── tests/                      # Unit tests
├── docs/                       # Documentation
├── scripts/                    # Utility scripts
│   ├── start_all.sh            # Start all services
│   └── deploy.sh               # Deployment script
├── requirements.txt            # Python dependencies
├── .gitignore
├── README.md
└── LICENSE
```

## 🏗️ Architecture

```
┌─────────────────┐
│  PySide6 App    │ (Data Source)
│  + Publisher    │
└────────┬────────┘
         │ ZMQ (Port 5555)
         ▼
┌─────────────────┐
│ Message Broker  │ (Distribution Hub)
└────────┬────────┘
         │ ZMQ (Port 5556)
    ┌────┴────┬──────────┬─────────┐
    │         │          │         │
    ▼         ▼          ▼         ▼
┌────────┐ ┌─────┐  ┌────────┐ ┌──────┐
│ Flask  │ │ DB  │  │Predict │ │Logger│
│   UI   │ │Saver│  │Engine  │ │      │
└───┬────┘ └─────┘  └────────┘ └──────┘
    │
    │ WebSocket
    ▼
┌─────────────────┐
│   Web Browser   │ (Operators)
│  Live Dashboard │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd drilling-telemetry-project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the System

**Option 1: Manual Start (for development)**

Open 5 separate terminals:

```bash
# Terminal 1: Message Broker
python backend/streaming/broker.py

# Terminal 2: Database Saver
python backend/subscribers/db_saver.py

# Terminal 3: Prediction Engine
python backend/subscribers/prediction_engine.py

# Terminal 4: Flask Web UI
python backend/flask_app/app.py

# Terminal 5: Test Data Publisher (for testing)
python backend/utils/test_publisher.py
```

**Option 2: Automated Start (production)**

```bash
# Start all services
./scripts/start_all.sh
```

Then open your browser to: `http://localhost:5000`

## 📊 Dashboard Features

### Live View
- Real-time charts updating every second
- Temperature, Pressure, Depth, RPM monitoring
- Zoom and pan retention during updates
- Current metrics with trend indicators

### Analytics View
- Historical trend analysis
- Correlation charts
- Performance metrics
- Downtime analysis

### Alerts View
- Active alerts and warnings
- Alert history
- Threshold configuration

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# Broker Configuration
BROKER_FRONTEND_PORT=5555
BROKER_BACKEND_PORT=5556

# Flask Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False

# Database
DATABASE_PATH=drilling_data.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Custom Topics

Modify `backend/streaming/publisher.py` to add custom topics:

```python
publisher.publish("custom_topic", {
    "your": "data"
})
```

## 🧪 Testing

### Run All Tests
```bash
pytest tests/
```

### Run Specific Tests
```bash
pytest tests/test_streaming.py
pytest tests/test_subscribers.py
```

### System Health Check
```bash
python backend/utils/monitor.py
```

## 📈 Performance

- **Latency**: <5ms (same machine), <20ms (local network)
- **Throughput**: 1000+ messages/second
- **Concurrent Subscribers**: Unlimited
- **Database Writes**: 500+ records/second
- **Memory Usage**: ~50MB per component

## 🔐 Security Considerations

- Use firewall rules to restrict broker ports
- Implement authentication for Flask UI (production)
- Use HTTPS in production
- Validate all incoming data
- Rate limit WebSocket connections

## 📝 Development

### Adding a New Subscriber

```python
from backend.streaming.subscriber import DataSubscriber

class MyCustomSubscriber(DataSubscriber):
    def __init__(self):
        super().__init__(topics=["drilling_data"])
    
    def on_message(self, topic, data):
        # Your logic here
        print(f"Received: {data}")

# Run it
subscriber = MyCustomSubscriber()
subscriber.start()
```

### Adding a New Dashboard View

1. Create HTML template in `frontend/templates/`
2. Add route in `backend/flask_app/routes.py`
3. Add navigation link in dashboard

## 🐛 Troubleshooting

### "Address already in use"
- Change ports in `.env` file
- Kill existing Python processes: `pkill -f python`

### "Can't connect to broker"
- Ensure broker is running first
- Check firewall settings
- Verify port numbers match

### "No data in charts"
- Check WebSocket connection in browser console
- Verify test publisher is running
- Check Flask logs for errors

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guide](docs/CONTRIBUTING.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## Libraries/framework

- ZeroMQ for high-performance messaging
- Plotly.js for interactive charts
- Flask for web framework

---

**Status**: ✅ Production Ready | 🚀 Active Development | 📊 Real-time Data
