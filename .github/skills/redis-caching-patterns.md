---
name: redis-caching-patterns
description: Redis caching strategies for performance optimization in microservices
technologies: [Python, Redis, Caching]
repositories: [ticketremaster-b, source-repo-code]
---

# Redis Caching Patterns

## When to Use

Use this skill when implementing caching strategies to improve performance and reduce database load in Python microservices.

## Prerequisites

- Basic Redis knowledge
- Understanding of caching concepts
- Familiarity with Python Redis clients

## Step-by-Step Instructions

### 1. Cache Configuration

```python
# shared/cache.py
import redis
import json
from typing import Any, Optional
from datetime import timedelta

class CacheManager:
    def __init__(self, redis_url: str = "redis://redis:6379/0"):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.default_ttl = 300  # 5 minutes
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            value = self.redis.get(key)
            return json.loads(value) if value else None
        except (redis.RedisError, json.JSONDecodeError) as e:
            print(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache with optional TTL."""
        try:
            serialized = json.dumps(value)
            ttl = ttl or self.default_ttl
            return self.redis.setex(key, ttl, serialized)
        except (redis.RedisError, TypeError) as e:
            print(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            return bool(self.redis.delete(key))
        except redis.RedisError as e:
            print(f"Cache delete error: {e}")
            return False
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern."""
        try:
            keys = self.redis.keys(pattern)
            if keys:
                return self.redis.delete(*keys)
            return 0
        except redis.RedisError as e:
            print(f"Cache invalidation error: {e}")
            return 0

# Usage in services
cache = CacheManager()
```

### 2. Cache-Aside Pattern (Lazy Loading)

```python
# services/event-service/routes.py
from flask import Blueprint, jsonify
from models import Event
from shared.cache import cache

bp = Blueprint("events", __name__)

@bp.get("/events/<event_id>")
def get_event(event_id):
    # 1. Check cache first
    cache_key = f"event:{event_id}"
    event_data = cache.get(cache_key)
    
    if event_data:
        return jsonify({"data": event_data, "source": "cache"}), 200
    
    # 2. Cache miss - query database
    event = Event.query.get(event_id)
    if not event:
        return jsonify({
            "error": {
                "code": "EVENT_NOT_FOUND",
                "message": "Event not found."
            }
        }), 404
    
    # 3. Populate cache for future requests
    event_data = event.to_dict()
    cache.set(cache_key, event_data, ttl=300)  # 5 minutes
    
    return jsonify({"data": event_data, "source": "db"}), 200
```

### 3. Write-Through Pattern

```python
# services/seat-inventory-service/routes.py
from flask import Blueprint, jsonify, request
from models import SeatInventory
from shared.cache import cache

bp = Blueprint("inventory", __name__)

@bp.patch("/seats/<inventory_id>/status")
def update_seat_status(inventory_id):
    data = request.get_json()
    new_status = data.get("status")
    
    # 1. Update database
    inventory = SeatInventory.query.get(inventory_id)
    if not inventory:
        return jsonify({"error": {"code": "SEAT_NOT_FOUND"}}), 404
    
    inventory.status = new_status
    db.session.commit()
    
    # 2. Update cache with same data
    cache_key = f"seat:{inventory_id}"
    cache.set(cache_key, inventory.to_dict(), ttl=300)
    
    # 3. Invalidate related caches
    cache.invalidate_pattern(f"event:{inventory.eventId}:seats:*")
    
    return jsonify({"data": inventory.to_dict()}), 200
```

### 4. Cache Invalidation Strategies

```python
# shared/cache_utils.py
from shared.cache import cache

class CacheInvalidator:
    @staticmethod
    def invalidate_event_seats(event_id: str):
        """Invalidate all seat cache for an event."""
        cache.invalidate_pattern(f"seat:*:event:{event_id}")
        cache.invalidate_pattern(f"event:{event_id}:*")
    
    @staticmethod
    def invalidate_user_tickets(user_id: str):
        """Invalidate all ticket cache for a user."""
        cache.invalidate_pattern(f"ticket:*:owner:{user_id}")
        cache.invalidate_pattern(f"user:{user_id}:tickets")
    
    @staticmethod
    def invalidate_venue_seats(venue_id: str):
        """Invalidate all seat cache for a venue."""
        cache.invalidate_pattern(f"seat:*:venue:{venue_id}")
        cache.invalidate_pattern(f"venue:{venue_id}:*")

# Usage in services
@bp.post("/events/<event_id>/populate-seats")
def populate_seats(event_id):
    # ... create seat inventory records ...
    
    # Invalidate all related caches
    CacheInvalidator.invalidate_event_seats(event_id)
    
    return jsonify({"message": "Seats populated"}), 201
```

### 5. Distributed Locking with Redis

```python
# shared/locks.py
import redis
import uuid
from typing import Optional
from datetime import timedelta

class DistributedLock:
    def __init__(self, redis_url: str = "redis://redis:6379/0"):
        self.redis = redis.from_url(redis_url, decode_responses=True)
    
    def acquire_lock(self, lock_name: str, timeout: int = 10) -> Optional[str]:
        """Acquire a distributed lock."""
        identifier = str(uuid.uuid4())
        lock_key = f"lock:{lock_name}"
        
        # Try to set the lock with NX (only if not exists)
        if self.redis.set(lock_key, identifier, nx=True, ex=timeout):
            return identifier
        return None
    
    def release_lock(self, lock_name: str, identifier: str) -> bool:
        """Release a distributed lock."""
        lock_key = f"lock:{lock_name}"
        
        # Use Lua script to ensure we only delete our own lock
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        
        return bool(self.redis.eval(lua_script, 1, lock_key, identifier))
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# Usage with context manager
from contextlib import contextmanager

@contextmanager
def seat_lock(inventory_id: str, timeout: int = 5):
    lock_manager = DistributedLock()
    lock_id = lock_manager.acquire_lock(f"seat:{inventory_id}", timeout)
    
    if not lock_id:
        raise Exception(f"Could not acquire lock for seat {inventory_id}")
    
    try:
        yield
    finally:
        lock_manager.release_lock(f"seat:{inventory_id}", lock_id)

# Usage in service
@bp.post("/seats/<inventory_id>/hold")
def hold_seat(inventory_id):
    try:
        with seat_lock(inventory_id, timeout=5):
            # Critical section - only one request can execute this at a time
            inventory = SeatInventory.query.get(inventory_id)
            if inventory.status != "available":
                return jsonify({"error": {"code": "SEAT_UNAVAILABLE"}}), 409
            
            inventory.status = "held"
            db.session.commit()
            
            return jsonify({"data": inventory.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": {"code": "LOCK_FAILED", "message": str(e)}}), 409
```

### 6. Rate Limiting with Redis

```python
# shared/rate_limiter.py
import redis
from typing import Tuple

class RateLimiter:
    def __init__(self, redis_url: str = "redis://redis:6379/0"):
        self.redis = redis.from_url(redis_url, decode_responses=True)
    
    def is_rate_limited(self, key: str, max_requests: int = 100, window: int = 60) -> Tuple[bool, int]:
        """
        Check if a key is rate limited.
        Returns (is_limited, remaining_requests)
        """
        current_time = int(time.time())
        window_key = f"rate:{key}:{current_time // window}"
        
        # Increment counter
        current = self.redis.incr(window_key)
        
        # Set expiry on first request
        if current == 1:
            self.redis.expire(window_key, window)
        
        remaining = max(0, max_requests - current)
        is_limited = current > max_requests
        
        return is_limited, remaining

# Usage in Flask middleware
from flask import request, jsonify
from shared.rate_limiter import RateLimiter

rate_limiter = RateLimiter()

@app.before_request
def check_rate_limit():
    # Rate limit by IP address
    client_ip = request.remote_addr
    is_limited, remaining = rate_limiter.is_rate_limited(client_ip, max_requests=100, window=60)
    
    if is_limited:
        return jsonify({
            "error": {
                "code": "RATE_LIMIT_EXCEEDED",
                "message": "Too many requests. Please try again later."
            }
        }), 429
    
    # Add rate limit headers
    response = jsonify({})
    response.headers['X-RateLimit-Limit'] = 100
    response.headers['X-RateLimit-Remaining'] = remaining
    
    return response
```

## Common Pitfalls

1. **Cache stampede** - Use distributed locks for popular keys
2. **Stale cache** - Always invalidate cache on writes
3. **Memory leaks** - Set appropriate TTLs for all cache entries
4. **Not handling cache failures** - Gracefully degrade when Redis is down
5. **Over-caching** - Don't cache everything; focus on hot data

## References

- [Redis Documentation](https://redis.io/documentation)
- [Cache-Aside Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)
- [Redis Best Practices](https://redis.io/docs/manual/)
