#!/bin/bash

# Drilling Telemetry System - Stop Script

echo "=================================================="
echo "🛑 STOPPING ALL SERVICES"
echo "=================================================="
echo ""

# Function to stop a service
stop_service() {
    SERVICE_NAME=$1
    PID_FILE="logs/${SERVICE_NAME}.pid"
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null; then
            echo "Stopping ${SERVICE_NAME} (PID: $PID)..."
            kill $PID
            sleep 1
            
            if ps -p $PID > /dev/null; then
                echo "Force killing ${SERVICE_NAME}..."
                kill -9 $PID
            fi
            
            echo "✅ ${SERVICE_NAME} stopped"
        else
            echo "⚠️  ${SERVICE_NAME} not running"
        fi
        rm $PID_FILE
    else
        echo "⚠️  No PID file found for ${SERVICE_NAME}"
    fi
}

# Stop services
stop_service "test_publisher"
stop_service "flask_app"
stop_service "prediction_engine"
stop_service "db_saver"
stop_service "broker"

echo ""
echo "✅ All services stopped"
echo ""
