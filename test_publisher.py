#!/usr/bin/env python3
"""
Simple Redis Publisher for Testing
==================================

This script sends test messages to Redis channels.
Run this alongside pubsub_demo.py to see real-time messaging.
"""

import redis
import json
import time
import sys
from datetime import datetime

def main():
    # Connect to Redis
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        print("✅ Connected to Redis")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        print("💡 Make sure Redis is running: sudo service redis-server start")
        return
    
    sender_id = "test_publisher"
    
    print(f"""
🚀 REDIS PUBLISHER TEST
======================
This will send test messages every 3 seconds.
Run pubsub_demo.py in another terminal to see real-time messages!

Press Ctrl+C to stop.
""")
    
    counter = 1
    
    try:
        while True:
            # Send different types of messages
            message_data = {
                'sender': sender_id,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            }
            
            if counter % 3 == 1:
                # Chat message
                message_data['message'] = f"Automated test message #{counter}"
                r.publish('chat_room', json.dumps(message_data))
                print(f"📤 Sent chat message #{counter}")
                
            elif counter % 3 == 2:
                # Notification
                message_data['message'] = f"System notification #{counter}"
                r.publish('notifications', json.dumps(message_data))
                print(f"🔔 Sent notification #{counter}")
                
            else:
                # Alert
                message_data['message'] = f"System status update #{counter}"
                r.publish('system_alerts', json.dumps(message_data))
                print(f"🚨 Sent alert #{counter}")
            
            counter += 1
            time.sleep(3)
            
    except KeyboardInterrupt:
        print(f"\n👋 Publisher stopped.")

if __name__ == "__main__":
    main()