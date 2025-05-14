import pickle
import hashlib
import threading
import math


def hash_pickle(obj, protocol=pickle.HIGHEST_PROTOCOL):
    data = pickle.dumps(obj, protocol=protocol)
    return hashlib.sha256(data).hexdigest()


# TC01 – Basic Types
def test_TC01_basic_types():
    values = [123, 123.456, "abc", True, False, None]
    for val in values:
        assert hash_pickle(val) == hash_pickle(val)
    print("TC01 passed: Basic Types")


# TC02 – Standard Collections
def test_TC02_standard_collections():
    values = [
        [1, 2, 3],
        (1, 2, 3),
        {1, 2, 3},
        {'a': 1, 'b': 2}
    ]
    for val in values:
        assert hash_pickle(val) == hash_pickle(val)
    print("TC02 passed: Standard Collections")


# TC03 – Nested Collections
def test_TC03_nested_collections():
    val = {'a': [1, {'b': (2, 3)}], 'c': ({1, 2},)}
    assert hash_pickle(val) == hash_pickle(val)
    print("TC03 passed: Nested Collections")


# TC04 – Recursive Structures
def test_TC04_recursive_structures():
    obj = []
    obj.append(obj)
    assert hash_pickle(obj) == hash_pickle(obj)
    print("TC04 passed: Recursive Structures")


# TC05 – Floating Point Arithmetic
def test_TC05_floating_point_arithmetic():
    a = 0.1 + 0.2
    b = 0.3
    assert hash_pickle(a) != hash_pickle(b), "Pickle must reflect floating-point imprecision"
    print("TC05 passed: Floating Point Arithmetic")


# TC06 – NaN and Infinity
def test_TC06_nan_and_infinity():
    inf = float('inf')
    ninf = float('-inf')
    nan1 = float('nan')
    nan2 = float('nan')

    # Positiv och negativ oändlighet ska vara stabilt serialiserade
    assert hash_pickle(inf) == hash_pickle(inf)
    assert hash_pickle(ninf) == hash_pickle(ninf)

    # NaN: kontrollera att picklingen *sker* men undvik att kräva instabilitet
    h1 = hash_pickle(nan1)
    h2 = hash_pickle(nan2)

    assert isinstance(h1, str) and isinstance(h2, str)
    print("TC06 passed: NaN and Infinity (pickle success, hash may or may not match)")



# TC07 – Custom Classes
class Animal:
    def __init__(self, name):
        self.name = name


def test_TC07_custom_classes():
    a = Animal("Tiger")
    assert hash_pickle(a) == hash_pickle(a)
    print("TC07 passed: Custom Classes")


# TC08 – Mutated Custom Object
def test_TC08_mutated_custom_object():
    a = Animal("Tiger")
    h1 = hash_pickle(a)
    a.name = "Lion"
    h2 = hash_pickle(a)
    assert h1 != h2
    print("TC08 passed: Mutated Custom Object")


# TC09 – Binary Data
def test_TC09_binary_data():
    b = bytearray([10, 20, 255, 0])
    assert hash_pickle(b) == hash_pickle(b)
    print("TC09 passed: Binary Data")


# TC10 – Circular ReferencesT
class Node:
    def __init__(self, value):
        self.value = value
        self.ref = None


def test_TC10_circular_references():
    a = Node("A")
    b = Node("B")
    a.ref = b
    b.ref = a
    assert hash_pickle(a) == hash_pickle(a)
    print("TC10 passed: Circular References")


# TC11 – Shared Object References
def test_TC11_shared_object_references():
    shared = [1, 2, 3]
    container = [shared, shared]
    assert hash_pickle(container) == hash_pickle(container)
    print("TC11 passed: Shared Object References")


# TC12 – Serialization in Threads
def test_TC12_serialization_in_threads():
    obj = {'shared': [1, 2, 3]}
    hashes = []

    def worker():
        hashes.append(hash_pickle(obj))

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(h == hashes[0] for h in hashes)
    print("TC12 passed: Serialization in Threads")


# TC13 – Unordered Containers (set/dict)
def test_TC13_unordered_containers():
    d1 = {'a': 1, 'b': 2}
    d2 = {'b': 2, 'a': 1}

    s1 = {1, 2, 3}
    s2 = {3, 2, 1}

    # Kontrollera att serialisering *lyckas*, men inte att hasharna är samma
    assert hash_pickle(d1) != '' and hash_pickle(d2) != ''
    assert hash_pickle(s1) != '' and hash_pickle(s2) != ''

    print("TC13 passed: Unordered Containers (hash not guaranteed to match)")



# TC14 – Protocol Version Differences
def test_TC14_protocol_versions():
    obj = {"x": 1, "y": 2}
    h3 = hash_pickle(obj, protocol=3)
    h5 = hash_pickle(obj, protocol=5)
    assert h3 != h5, "Different protocols should yield different hashes"
    print("TC14 passed: Protocol Version Differences")


# TC15 – Cross-Environment Consistency (manual)
def test_TC15_cross_environment_consistency():
    print("TC15 manual: Run this test on different OS/Python versions and compare hash_pickle results")
    print("Test object:", {"os_independent": True})


# Main runner
def main():
    test_TC01_basic_types()
    test_TC02_standard_collections()
    test_TC03_nested_collections()
    test_TC04_recursive_structures()
    test_TC05_floating_point_arithmetic()
    test_TC06_nan_and_infinity()
    test_TC07_custom_classes()
    test_TC08_mutated_custom_object()
    test_TC09_binary_data()
    test_TC10_circular_references()
    test_TC11_shared_object_references()
    test_TC12_serialization_in_threads()
    test_TC13_unordered_containers()
    test_TC14_protocol_versions()
    test_TC15_cross_environment_consistency()


if __name__ == "__main__":
    main()
