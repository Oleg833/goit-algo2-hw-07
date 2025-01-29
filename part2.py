import timeit
import functools
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate


@functools.lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)



class SplayTreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root

            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._rotate_left(root.left)

            return root if root.left is None else self._rotate_right(root)

        else:
            if root.right is None:
                return root

            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._rotate_right(root.right)

            return root if root.right is None else self._rotate_left(root)

    def _rotate_left(self, node):
        temp = node.right
        node.right = temp.left
        temp.left = node
        return temp

    def _rotate_right(self, node):
        temp = node.left
        node.left = temp.right
        temp.right = node
        return temp

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayTreeNode(key, value)
            return

        self.root = self._splay(self.root, key)

        if self.root.key == key:
            return

        new_node = SplayTreeNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node

    def search(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None


def fibonacci_splay(n, tree):
    if n < 2:
        return n

    cached_value = tree.search(n)
    if cached_value is not None:
        return cached_value

    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


n_values = list(range(0, 951, 50))
lru_times = []
splay_times = []


for n in n_values:
    # LRU Cache
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=10) / 10
    lru_times.append(lru_time)

    # Splay Tree
    splay_tree = SplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, splay_tree), number=10) / 10
    splay_times.append(splay_time)


plt.figure(figsize=(10, 6))
plt.plot(n_values, lru_times, marker="o", label="LRU Cache")
plt.plot(n_values, splay_times, marker="s", label="Splay Tree")
plt.xlabel("n (номер числа Фібоначчі)")
plt.ylabel("Середній час виконання (секунди)")
plt.title("Порівняння часу виконання LRU Cache та Splay Tree")
plt.legend()
plt.grid()
plt.show()


formatted_table = tabulate(
    [
        [n, f"{lru:.8f}", f"{splay:.8f}"]
        for n, lru, splay in zip(n_values, lru_times, splay_times)
    ],
    headers=["n", "LRU Cache Time (s)", "Splay Tree Time (s)"],
    tablefmt="pretty",
)
print(formatted_table)
