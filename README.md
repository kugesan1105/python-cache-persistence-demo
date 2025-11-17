# Python Cache Persistence Demo

This repo demonstrates the difference between Redis (with persistence) and Memcached (without persistence).

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Redis and Memcached are running:
```bash
sudo service redis-server start
sudo service memcached start
```
3. Run the demo:
```
python cache_test.py
```
