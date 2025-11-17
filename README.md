# Python Cache Persistence + Pub/Sub Demo

This repo demonstrates:
- ✅ **Redis with persistence** - Data survives service restarts
- ❌ **Memcached without persistence** - Data lost on restart  
- 🚀 **Redis Pub/Sub** - Real-time messaging between multiple clients

## 🎯 What You'll See

### Persistence Test
- Redis retains data after service restart
- Memcached loses all data after restart

### Real-Time Messaging
- Multiple terminals can communicate in real-time
- Different message types: chat, notifications, alerts
- Live statistics and monitoring

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
# Setup services automatically
./setup_services.sh

# Run the main demo
python pubsub_demo.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start services manually
sudo service redis-server start
sudo service memcached start

# Run demos
python pubsub_demo.py          # Main interactive demo
python test_publisher.py       # Automated message publisher
python cache_test.py           # Original simple demo
```

## 🎮 Demo Scripts

### 1. `pubsub_demo.py` - Interactive Real-Time Demo
- **Persistence test** - Compare Redis vs Memcached
- **Real-time chat** - Multi-terminal communication
- **Commands**:
  - Type normally to send chat messages
  - `/notify <message>` - Send notification
  - `/alert <message>` - Send system alert
  - `/stats` - Show cache statistics
  - `/quit` - Exit

### 2. `test_publisher.py` - Automated Message Generator
- Sends test messages every 3 seconds
- Different message types (chat, notifications, alerts)
- Perfect for testing while running the main demo

### 3. `cache_test.py` - Original Simple Demo
- Basic persistence comparison
- Manual restart testing

## 🎪 Try This!

1. **Terminal 1**: Run `python pubsub_demo.py`
2. **Terminal 2**: Run `python pubsub_demo.py` 
3. **Terminal 3**: Run `python test_publisher.py`

Watch real-time messages flow between all terminals!

## 🔧 Requirements

- Python 3.7+
- Redis server
- Memcached server
- Linux/Ubuntu environment

The demo will automatically try to start services and install missing packages.
