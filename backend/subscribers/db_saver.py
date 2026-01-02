"""
Database Saver - Saves all drilling data to SQLite
"""

import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streaming.subscriber import DataSubscriber
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('DatabaseSaver')

class DatabaseSaver(DataSubscriber):
    """Listens to drilling data and saves it to SQLite."""
    
    def __init__(self, db_path="drilling_data.db"):
        super().__init__(topics=["drilling_data", "nse", "surface"])
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.setup_database()
        self.save_count = 0
        logger.info(f"💾 Database connected: {db_path}")
    
    def setup_database(self):
        """Create tables if they don't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS drilling_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                topic TEXT,
                temperature REAL,
                pressure REAL,
                depth REAL,
                rpm INTEGER,
                raw_data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
        logger.info("📊 Database table ready")
    
    def on_message(self, topic, data):
        """Save incoming data to database."""
        try:
            self.cursor.execute("""
                INSERT INTO drilling_data 
                (timestamp, topic, temperature, pressure, depth, rpm, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('timestamp'),
                topic,
                data.get('temperature'),
                data.get('pressure'),
                data.get('depth'),
                data.get('rpm'),
                json.dumps(data)
            ))
            self.conn.commit()
            self.save_count += 1
            logger.info(f"💾 Saved [{topic}] to database (Total: {self.save_count})")
        except Exception as e:
            logger.error(f"❌ Database error: {e}")
    
    def stop(self):
        """Close database connection."""
        logger.info(f"📊 Total records saved: {self.save_count}")
        self.conn.close()
        super().stop()

def main():
    saver = DatabaseSaver()
    saver.start()

if __name__ == "__main__":
    main()
