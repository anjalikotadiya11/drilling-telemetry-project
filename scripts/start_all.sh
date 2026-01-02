#!/bin/bash

# Drilling Telemetry System - Startup Script
# This starts all services in the correct order

echo "=================================================="
echo "🛢️  DRILLING TELEMETRY SYSTEM - STARTUP"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    source venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
fi

# Create logs directory
mkdir -p logs

# Function to start a service
start_service() {
    SERVICE_NAME=$1
    SCRIPT_PATH=$2
    LOG_FILE="logs/${SERVICE_NAME}.log"
    
    echo -e "${YELLOW}Starting ${SERVICE_NAME}...${NC}"
    nohup python $SCRIPT_PATH > $LOG_FILE 2>&1 &
    PID=$!
    echo $PID > "logs/${SERVICE_NAME}.pid"
    sleep 1
    
    if ps -p $PID > /dev/null; then
        echo -e "${GREEN}✅ ${SERVICE_NAME} started (PID: $PID)${NC}"
    else
        echo -e "${RED}❌ ${SERVICE_NAME} failed to start${NC}"
        cat $LOG_FILE
    fi
}

echo ""
echo "📡 Starting services..."
echo ""

# Start services in order
start_service "broker" "backend/streaming/broker.py"
sleep 2

start_service "db_saver" "backend/subscribers/db_saver.py"
sleep 1

start_service "prediction_engine" "backend/subscribers/prediction_engine.py"
sleep 1

start_service "flask_app" "backend/flask_app/app.py"
sleep 2

start_service "test_publisher" "backend/utils/test_publisher.py"

echo ""
echo "=================================================="
echo -e "${GREEN}🎉 ALL SERVICES STARTED${NC}"
echo "=================================================="
echo ""
echo "📊 Dashboard: http://localhost:5000"
echo "💾 Database: drilling_data.db"
echo "📋 Logs: logs/"
echo ""
echo "To stop all services, run: ./scripts/stop_all.sh"
echo "To view logs: tail -f logs/*.log"
echo ""
