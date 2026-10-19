"""Словарь (HashMap) на основе хеш-таблицы с методом цепочек (separate chaining)."""


class _Node:
    """Узел односвязного списка внутри корзины (bucket)."""

    __slots__ = ("key", "value", "next")

    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node


class HashMap:
    INITIAL_CAPACITY = 8
    MAX_LOAD_FACTOR = 0.75

    def __init__(self, capacity=INITIAL_CAPACITY):
        if capacity < 1:
            raise ValueError("capacity должен быть >= 1")
        self._capacity = capacity
        self._buckets = [None] * capacity  # каждая ячейка — голова цепочки
        self._size = 0

    # ---------- внутренние методы ----------

    def _index(self, key):
        """Индекс корзины для ключа. hash() сам бросит TypeError для list/dict."""
        return hash(key) % self._capacity

    def _resize(self, new_capacity):
        """Увеличить таблицу и перераспределить все узлы по новым корзинам."""
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [None] * new_capacity
        for head in old_buckets:
            node = head
            while node is not None:
                nxt = node.next  # запоминаем: ниже node.next будет перезаписан
                idx = self._index(node.key)
                node.next = self._buckets[idx]
                self._buckets[idx] = node
                node = nxt

    def _find_node(self, key):
        node = self._buckets[self._index(key)]
        while node is not None:
            if node.key == key:
                return node
            node = node.next
        return None

    # ---------- основной интерфейс ----------

    def put(self, key, value):
        """Вставить пару или обновить значение, если ключ уже есть."""
        node = self._find_node(key)
        if node is not None:
            node.value = value
            return
        if (self._size + 1) / self._capacity > self.MAX_LOAD_FACTOR:
            self._resize(self._capacity * 2)
        idx = self._index(key)
        self._buckets[idx] = _Node(key, value, self._buckets[idx])  # в начало цепочки
        self._size += 1

    def get(self, key, default=None):
        """Значение по ключу или default, если ключа нет."""
        node = self._find_node(key)
        return default if node is None else node.value

    def remove(self, key):
        """Удалить ключ и вернуть его значение. KeyError, если ключа нет."""
        idx = self._index(key)
        prev, node = None, self._buckets[idx]
        while node is not None:
            if node.key == key:
                if prev is None:
                    self._buckets[idx] = node.next
                else:
                    prev.next = node.next
                self._size -= 1
                return node.value
            prev, node = node, node.next
        raise KeyError(key)

    def contains_key(self, key):
        return self._find_node(key) is not None

    def items(self):
        """Список пар (ключ, значение)."""
        result = []
        for head in self._buckets:
            node = head
            while node is not None:
                result.append((node.key, node.value))
                node = node.next
        return result

    def keys(self):
        return [k for k, _ in self.items()]

    def values(self):
        return [v for _, v in self.items()]

    # ---------- магические методы ----------

    def __getitem__(self, key):
        node = self._find_node(key)
        if node is None:
            raise KeyError(key)
        return node.value

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __contains__(self, key):
        return self.contains_key(key)

    def __len__(self):
        return self._size

    def __iter__(self):
        return iter(self.keys())

    def __repr__(self):
        body = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"HashMap({{{body}}})"
