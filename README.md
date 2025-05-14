# pickle_testing
# Pickle Hash Tests

This project provides a suite of test cases to verify the behavior of `pickle` serialization in Python using SHA-256 hashes for consistency checks.

## Features

- Tests for basic types, standard and nested collections
- Handles circular and recursive references
- Custom class serialization and mutation detection
- Thread-safe hashing
- Floating-point quirks (NaN, inf)
- Cross-protocol and environment consistency checks

## Usage

Run all tests:

```bash
python pickle_testing.py
