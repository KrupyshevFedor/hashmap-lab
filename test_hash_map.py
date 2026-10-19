import unittest
from hash_map import HashMap


class BadHash:
    """Ключ с одинаковым хешем у всех экземпляров — принудительные коллизии."""

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return 42

    def __eq__(self, other):
        return isinstance(other, BadHash) and self.name == other.name


class TestHashMap(unittest.TestCase):
    def test_put_get_update(self):
        m = HashMap()
        m.put("a", 1)
        m.put("a", 2)  # обновление
        self.assertEqual(m.get("a"), 2)
        self.assertEqual(len(m), 1)

    def test_get_default(self):
        m = HashMap()
        self.assertIsNone(m.get("x"))
        self.assertEqual(m.get("x", 0), 0)

    def test_remove(self):
        m = HashMap()
        m.put("a", 1)
        self.assertEqual(m.remove("a"), 1)
        self.assertFalse(m.contains_key("a"))
        self.assertEqual(len(m), 0)
        with self.assertRaises(KeyError):
            m.remove("a")

    def test_contains_key(self):
        m = HashMap()
        m["k"] = None  # значение None — ключ всё равно есть
        self.assertTrue(m.contains_key("k"))
        self.assertIn("k", m)
        self.assertNotIn("z", m)

    def test_keys_values_items(self):
        m = HashMap()
        for i in range(5):
            m[i] = i * i
        self.assertEqual(sorted(m.keys()), [0, 1, 2, 3, 4])
        self.assertEqual(sorted(m.values()), [0, 1, 4, 9, 16])
        self.assertEqual(sorted(m.items()), [(i, i * i) for i in range(5)])

    def test_dunder_methods(self):
        m = HashMap()
        m["x"] = 10
        self.assertEqual(m["x"], 10)
        del m["x"]
        with self.assertRaises(KeyError):
            m["x"]
        with self.assertRaises(KeyError):
            del m["x"]

    def test_string_keys(self):
        m = HashMap()
        m["apple"], m["banana"] = 1, 2
        self.assertEqual((m["apple"], m["banana"]), (1, 2))

    def test_number_keys(self):
        m = HashMap()
        m[1], m[2.5], m[-7] = "int", "float", "neg"
        self.assertEqual((m[1], m[2.5], m[-7]), ("int", "float", "neg"))
        # 1 == 1.0 и hash равны — как в обычном dict, это один и тот же ключ
        m[1.0] = "same"
        self.assertEqual(m[1], "same")
        self.assertEqual(len(m), 3)

    def test_tuple_keys(self):
        m = HashMap()
        m[(1, 2)] = "a"
        m[(2, 1)] = "b"
        m[("x", (3, 4))] = "nested"
        self.assertEqual(m[(1, 2)], "a")
        self.assertEqual(m[(2, 1)], "b")
        self.assertEqual(m[("x", (3, 4))], "nested")

    def test_mixed_keys(self):
        m = HashMap()
        m["1"], m[1], m[(1,)] = "str", "int", "tuple"
        self.assertEqual((m["1"], m[1], m[(1,)]), ("str", "int", "tuple"))

    def test_unhashable_key(self):
        m = HashMap()
        with self.assertRaises(TypeError):
            m[[1, 2]] = "list"

    def test_collisions(self):
        m = HashMap()
        keys = [BadHash(str(i)) for i in range(20)]  # все в одной корзине
        for i, k in enumerate(keys):
            m[k] = i
        self.assertEqual(len(m), 20)
        for i, k in enumerate(keys):
            self.assertEqual(m[k], i)
        # удаление из середины, головы и хвоста цепочки
        for idx in (10, 0, 19):
            del m[keys[idx]]
            self.assertNotIn(keys[idx], m)
        self.assertEqual(len(m), 17)

    def test_resize_keeps_data(self):
        m = HashMap(capacity=2)
        for i in range(1000):
            m[i] = str(i)
        self.assertEqual(len(m), 1000)
        self.assertTrue(all(m[i] == str(i) for i in range(1000)))

    def test_compare_with_dict(self):
        import random
        random.seed(1)
        m, d = HashMap(), {}
        for _ in range(5000):
            k = random.randint(0, 200)
            op = random.choice("pgr")
            if op == "p":
                m[k] = d[k] = random.random()
            elif op == "g":
                self.assertEqual(m.get(k), d.get(k))
            elif k in d:
                self.assertEqual(m.remove(k), d.pop(k))
        self.assertEqual(sorted(m.items()), sorted(d.items()))


if __name__ == "__main__":
    unittest.main()
