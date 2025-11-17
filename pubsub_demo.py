#!/usr/bin/env python3
"""
Redis vs Memcached Demo with Redis Pub/Sub
==========================================

This demo showcases:
✅ Redis with persistence
❌ Memcached without persistence  
🚀 Redis Pub/Sub for real-time messaging

Run multiple instances to see real-time communication!
"""

import redis
from pymemcache.client import base
import threading
import time
import sys
import json
from datetime import datetime
import signal
import os

class CachePubSubDemo:
    def __init__(self):
        # Redis connections
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.redis_pubsub = self.redis_client.pubsub()
        
        # Memcached connection
        self.memcached_client = base.Client(('localhost', 11211))
        
        # Demo state
        self.running = True
        self.user_id = f"user_{os.getpid()}"  # Unique user ID based on process ID
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print(f"\n👋 {self.user_id} is leaving the chat...")
        self.running = False
        sys.exit(0)
    
    def test_persistence(self):
        """Test Redis vs Memcached persistence"""
        print("🔧 PERSISTENCE TEST")
        print("=" * 50)
        
        # Test data
        test_key = "demo_data"
        redis_value = f"Redis_data_from_{self.user_id}_at_{datetime.now().strftime('%H:%M:%S')}"
        memcached_value = f"Memcached_data_from_{self.user_id}_at_{datetime.now().strftime('%H:%M:%S')}"
        
        # Set values
        self.redis_client.set(test_key, redis_value)
        self.memcached_client.set(test_key, memcached_value)
        
        print(f"✅ Stored in Redis: {self.redis_client.get(test_key)}")
        print(f"✅ Stored in Memcached: {self.memcached_client.get(test_key).decode()}")
        
        print("\n💡 Redis data persists across restarts, Memcached doesn't!")
        print("   Try restarting the services and running the demo again.\n")
    
    def pubsub_listener(self):
        """Listen for messages on Redis Pub/Sub"""
        self.redis_pubsub.subscribe('chat_room', 'notifications', 'system_alerts')
        
        print(f"🎧 {self.user_id} is listening for messages...")
        
        try:
            for message in self.redis_pubsub.listen():
                if not self.running:
                    break
                    
                if message['type'] == 'message':
                    data = json.loads(message['data'])
                    channel = message['channel']
                    
                    # Don't show our own messages
                    if data.get('sender') != self.user_id:
                        timestamp = data.get('timestamp', '')
                        sender = data.get('sender', 'Unknown')
                        content = data.get('message', '')
                        
                        if channel == 'chat_room':
                            print(f"💬 [{timestamp}] {sender}: {content}")
                        elif channel == 'notifications':
                            print(f"🔔 [{timestamp}] NOTIFICATION - {sender}: {content}")
                        elif channel == 'system_alerts':
                            print(f"🚨 [{timestamp}] SYSTEM ALERT - {content}")
        except Exception as e:
            if self.running:  # Only print if we're not shutting down
                print(f"❌ Listener error: {e}")
    
    def send_message(self, channel, message):
        """Send a message to a Redis channel"""
        message_data = {
            'sender': self.user_id,
            'message': message,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        
        try:
            self.redis_client.publish(channel, json.dumps(message_data))
            return True
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return False
    
    def interactive_chat(self):
        """Interactive chat interface"""
        print(f"\n💬 REAL-TIME CHAT DEMO")
        print("=" * 50)
        print(f"🎭 You are: {self.user_id}")
        print("📍 Commands:")
        print("   - Just type to send to chat_room")
        print("   - '/notify <message>' to send notification")
        print("   - '/alert <message>' to send system alert")
        print("   - '/quit' to exit")
        print("   - '/stats' to show cache statistics")
        print("\n🚀 Start another terminal and run this script to see real-time messaging!")
        print("-" * 50)
        
        # Start the listener in a separate thread
        listener_thread = threading.Thread(target=self.pubsub_listener, daemon=True)
        listener_thread.start()
        
        # Send join notification
        self.send_message('system_alerts', f"{self.user_id} joined the chat!")
        
        try:
            while self.running:
                user_input = input().strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == '/quit':
                    break
                elif user_input.lower() == '/stats':
                    self.show_cache_stats()
                elif user_input.startswith('/notify '):
                    message = user_input[8:]  # Remove '/notify '
                    self.send_message('notifications', message)
                elif user_input.startswith('/alert '):
                    message = user_input[7:]  # Remove '/alert '
                    self.send_message('system_alerts', message)
                else:
                    self.send_message('chat_room', user_input)
                    
        except EOFError:
            # Handle Ctrl+D
            pass
        except KeyboardInterrupt:
            # Handle Ctrl+C
            pass
        
        # Send leave notification
        self.send_message('system_alerts', f"{self.user_id} left the chat!")
        self.running = False
    
    def show_cache_stats(self):
        """Show current cache statistics"""
        try:
            # Redis stats
            redis_info = self.redis_client.info()
            redis_keys = len(self.redis_client.keys('*'))
            
            # Memcached stats  
            memcached_stats = self.memcached_client.stats()
            
            print(f"\n📊 CACHE STATISTICS")
            print("-" * 30)
            print(f"🔴 Redis:")
            print(f"   - Connected clients: {redis_info.get('connected_clients', 'N/A')}")
            print(f"   - Total keys: {redis_keys}")
            print(f"   - Memory usage: {redis_info.get('used_memory_human', 'N/A')}")
            print(f"   - Uptime: {redis_info.get('uptime_in_seconds', 0)} seconds")
            
            print(f"\n🟠 Memcached:")
            print(f"   - Current items: {memcached_stats.get(b'curr_items', b'N/A').decode()}")
            print(f"   - Total connections: {memcached_stats.get(b'total_connections', b'N/A').decode()}")
            print(f"   - Memory usage: {memcached_stats.get(b'bytes', b'N/A').decode()} bytes")
            print(f"   - Uptime: {memcached_stats.get(b'uptime', b'N/A').decode()} seconds")
            print("-" * 30)
            
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
    
    def run_demo(self):
        """Run the complete demo"""
        print("🚀 REDIS vs MEMCACHED + PUB/SUB DEMO")
        print("=" * 60)
        
        # Test connections
        try:
            self.redis_client.ping()
            print("✅ Redis connection successful")
        except Exception as e:
            print(f"❌ Redis connection failed: {e}")
            print("💡 Make sure Redis is running: sudo service redis-server start")
            return
        
        try:
            self.memcached_client.set("test", "test")
            print("✅ Memcached connection successful")
        except Exception as e:
            print(f"❌ Memcached connection failed: {e}")
            print("💡 Make sure Memcached is running: sudo service memcached start")
            return
        
        print()
        
        # Test persistence
        self.test_persistence()
        
        # Start interactive chat
        self.interactive_chat()
        
        print(f"\n👋 Thanks for testing the demo, {self.user_id}!")

def main():
    """Main function"""
    demo = CachePubSubDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()