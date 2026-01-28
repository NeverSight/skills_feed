---
name: Python Fundamentals
description: Master Python syntax, data types, control flow, functions, OOP, and standard library
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 01-python-fundamentals
bond_type: PRIMARY_BOND

# Skill Configuration
retry_strategy: exponential_backoff
observability:
  logging: true
  metrics: skill_completion_rate
---

# Python Fundamentals

## Overview

This skill covers the foundational elements of Python programming including syntax, data types, control structures, functions, object-oriented programming, and the standard library.

## Learning Objectives

- Write clean, Pythonic code following PEP 8 guidelines
- Master all Python data structures (lists, tuples, dicts, sets)
- Understand and implement object-oriented programming concepts
- Navigate and utilize the Python standard library effectively
- Manage virtual environments and packages with pip/venv

## Core Topics

### 1. Python Syntax & Data Types
- Variables and naming conventions
- Numeric types (int, float, complex)
- Strings and string methods
- Boolean logic and None
- Type hints (PEP 484)
- F-strings and formatting

**Code Example:**
```python
# Type hints and f-strings
def greet_user(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old!"

# Using the function
message = greet_user("Alice", 30)
print(message)  # Hello Alice, you are 30 years old!
```

### 2. Control Flow & Functions
- Conditional statements (if/elif/else)
- Loops (for, while)
- List/dict/set comprehensions
- Function parameters and arguments
- Lambda functions
- Decorators basics

**Code Example:**
```python
# List comprehension with conditional
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_squares = [x**2 for x in numbers if x % 2 == 0]
print(even_squares)  # [4, 16, 36, 64, 100]

# Decorator example
def timing_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    import time
    time.sleep(1)
    return "Done!"
```

### 3. Object-Oriented Programming
- Classes and instances
- Inheritance and composition
- Polymorphism and duck typing
- Encapsulation (public/private)
- Magic methods (__init__, __str__, __repr__, etc.)
- Abstract base classes

**Code Example:**
```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, brand: str, model: str):
        self.brand = brand
        self.model = model

    @abstractmethod
    def start_engine(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self.brand} {self.model}"

class Car(Vehicle):
    def __init__(self, brand: str, model: str, doors: int):
        super().__init__(brand, model)
        self.doors = doors

    def start_engine(self) -> str:
        return f"{self} engine started with {self.doors} doors"

# Usage
car = Car("Toyota", "Camry", 4)
print(car.start_engine())  # Toyota Camry engine started with 4 doors
```

### 4. Standard Library
- File operations (open, read, write)
- Path handling with pathlib
- datetime for date/time operations
- collections (Counter, defaultdict, namedtuple)
- itertools and functools
- json and csv modules

**Code Example:**
```python
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
import json

# Path operations
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

config_file = data_dir / "config.json"
config = {"app_name": "MyApp", "version": "1.0.0"}

# Write JSON
with open(config_file, "w") as f:
    json.dump(config, f, indent=2)

# Read JSON
with open(config_file, "r") as f:
    loaded_config = json.load(f)

# Date operations
today = datetime.now()
next_week = today + timedelta(days=7)
formatted = today.strftime("%Y-%m-%d %H:%M:%S")

# Counter for frequency analysis
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
word_count = Counter(words)
print(word_count.most_common(2))  # [('apple', 3), ('banana', 2)]
```

## Hands-On Practice

### Project 1: File Management Tool
Build a command-line tool that organizes files by extension.

**Requirements:**
- Accept directory path as input
- Scan for files recursively
- Group files by extension
- Move files to organized folders
- Generate summary report

**Key Skills:** pathlib, file I/O, os module

### Project 2: Contact Manager (OOP)
Create a contact management system using object-oriented principles.

**Requirements:**
- Contact class with name, email, phone
- ContactBook class to manage contacts
- CRUD operations (Create, Read, Update, Delete)
- Search and filter functionality
- Persist data to JSON file

**Key Skills:** OOP, JSON serialization, data structures

### Project 3: Text Analyzer
Analyze text files for statistics and patterns.

**Requirements:**
- Word frequency analysis
- Character count (with/without spaces)
- Average word length
- Most common words (exclude stop words)
- Export results to CSV

**Key Skills:** String manipulation, collections.Counter, CSV

## Assessment Criteria

- [ ] Write PEP 8 compliant Python code
- [ ] Use appropriate data structures for different scenarios
- [ ] Implement classes with proper OOP principles
- [ ] Utilize standard library modules effectively
- [ ] Manage virtual environments and dependencies
- [ ] Handle exceptions properly
- [ ] Write clear docstrings and comments

## Resources

### Official Documentation
- [Python.org](https://python.org) - Official Python documentation
- [PEP 8](https://pep8.org) - Python style guide
- [Python Tutorial](https://docs.python.org/3/tutorial/) - Official tutorial

### Learning Platforms
- [Real Python](https://realpython.com) - Comprehensive tutorials
- [Python for Everybody](https://py4e.com) - Free course
- [Automate the Boring Stuff](https://automatetheboringstuff.com) - Practical Python

### Tools
- [VS Code](https://code.visualstudio.com) - Recommended editor
- [PyCharm](https://jetbrains.com/pycharm/) - Professional IDE
- [pylint](https://pylint.org) - Code linter
- [black](https://black.readthedocs.io) - Code formatter

## Next Steps

After mastering Python fundamentals, proceed to:
- **Django Framework** - Build web applications
- **Pandas Data Analysis** - Work with data
- **Pytest Testing** - Write comprehensive tests
- **Asyncio Programming** - Asynchronous Python
