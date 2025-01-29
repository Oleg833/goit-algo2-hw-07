import random
import time
from functools import lru_cache
from collections import OrderedDict

class LRUCache:
    """LRU Cache implementation with a fixed size."""
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        """Retrieve an item from cache."""
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        """Insert an item into the cache."""
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def invalidate(self, index):
        """Remove all cache entries affected by an update."""
        keys_to_delete = [key for key in self.cache if key[0] <= index <= key[1]]
        for key in keys_to_delete:
            del self.cache[key]

# Functions without caching
def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

# Functions with LRU cache
cache = LRUCache(1000)

def range_sum_with_cache(array, L, R):
    key = (L, R)
    cached_result = cache.get(key)
    if cached_result is not None:
        return cached_result
    result = sum(array[L:R+1])
    cache.put(key, result)
    return result

def update_with_cache(array, index, value):
    array[index] = value
    cache.invalidate(index)

# Generate test data
N = 100_000
Q = 50_000
array = [random.randint(1, 1000) for _ in range(N)]
queries = []
for _ in range(Q):
    if random.random() < 0.7:  # 70% chance of Range query, 30% Update query
        L = random.randint(0, N - 1)
        R = random.randint(L, N - 1)
        queries.append(('Range', L, R))
    else:
        index = random.randint(0, N - 1)
        value = random.randint(1, 1000)
        queries.append(('Update', index, value))

# Benchmark without caching
start_time = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_no_cache(array, query[1], query[2])
    else:
        update_no_cache(array, query[1], query[2])
time_no_cache = time.time() - start_time

# Benchmark with caching
cache = LRUCache(1000)  # Reset cache
start_time = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_with_cache(array, query[1], query[2])
    else:
        update_with_cache(array, query[1], query[2])
time_with_cache = time.time() - start_time

# Output results
print(f"Час виконання без кешування: {time_no_cache:.2f} секунд")
print(f"Час виконання з LRU-кешем: {time_with_cache:.2f} секунд")
