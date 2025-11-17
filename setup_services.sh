#!/bin/bash
# Setup Script for Redis and Memcached Demo
# =========================================

echo "🚀 Starting Redis and Memcached services..."

# Start Redis
echo "📡 Starting Redis..."
sudo service redis-server start
if [ $? -eq 0 ]; then
    echo "✅ Redis started successfully"
else
    echo "❌ Failed to start Redis"
    echo "💡 Installing Redis..."
    sudo apt update && sudo apt install -y redis-server
    sudo service redis-server start
fi

# Start Memcached  
echo "📡 Starting Memcached..."
sudo service memcached start
if [ $? -eq 0 ]; then
    echo "✅ Memcached started successfully"
else
    echo "❌ Failed to start Memcached"
    echo "💡 Installing Memcached..."
    sudo apt update && sudo apt install -y memcached
    sudo service memcached start
fi

echo ""
echo "🎯 Services Status:"
sudo service redis-server status | grep -E "(Active|loaded)"
sudo service memcached status | grep -E "(Active|loaded)"

echo ""
echo "🚀 Ready to run the demo!"
echo "   Run: python pubsub_demo.py"
echo "   Or:  python test_publisher.py (in another terminal)"