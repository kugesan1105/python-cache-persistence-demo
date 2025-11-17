#!/bin/bash
# Restart Services Script
# ======================
# Use this to restart Redis and Memcached for persistence testing

echo "🔄 RESTARTING SERVICES FOR PERSISTENCE TEST"
echo "============================================"

echo "📡 Restarting Redis..."
sudo service redis-server restart
if [ $? -eq 0 ]; then
    echo "✅ Redis restarted successfully"
else
    echo "❌ Failed to restart Redis"
fi

echo "📡 Restarting Memcached..."
sudo service memcached restart
if [ $? -eq 0 ]; then
    echo "✅ Memcached restarted successfully"
else
    echo "❌ Failed to restart Memcached"
fi

echo ""
echo "🎯 Services restarted! Now run:"
echo "   python persistence_demo.py"
echo ""
echo "💡 Expected result:"
echo "   ✅ Redis data will survive the restart"
echo "   ❌ Memcached data will be lost"