import redis
from pymemcache.client import base

# --- CONNECT TO REDIS ---
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# --- CONNECT TO MEMCACHED ---
m = base.Client(('localhost', 11211))

print("---- Setting values ----")

# Set values
r.set("username", "kugesan_redis")
m.set("username", "kugesan_memcached")

print("Redis saved:", r.get("username"))
print("Memcached saved:", m.get("username"))

input("\nNow RESTART Redis & Memcached, then press ENTER to continue...")

print("\n---- Checking values after restart ----")
print("Redis value:", r.get("username"))
print("Memcached value:", m.get("username"))
