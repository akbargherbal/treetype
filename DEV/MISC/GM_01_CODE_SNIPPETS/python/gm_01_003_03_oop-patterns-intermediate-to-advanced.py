# PATTERN: OOP Patterns (Intermediate to Advanced)

class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

# PATTERN: OOP Patterns (Intermediate to Advanced)

class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class DiscountedProduct(Product):
    def __init__(self, name: str, price: float, discount_percentage: float):
        super().__init__(name, price)
        self.discount_percentage = discount_percentage
        self.discounted_price = price * (1 - discount_percentage / 100)

# PATTERN: OOP Patterns (Intermediate to Advanced)

class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} (Price: ${self.price:.2f})"

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price:.2f})"

# PATTERN: OOP Patterns (Intermediate to Advanced)

class Product:
    def __init__(self, product_id: int, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.product_id == other.product_id

    def __hash__(self):
        return hash(self.product_id)

# PATTERN: OOP Patterns (Intermediate to Advanced)

class FileManager:
    def __init__(self, filename: str, mode: str):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

# PATTERN: OOP Patterns (Intermediate to Advanced)

class Multiplier:
    def __init__(self, factor: int):
        self.factor = factor

    def __call__(self, number: int):
        return number * self.factor

# PATTERN: OOP Patterns (Intermediate to Advanced)

class Playlist:
    def __init__(self, name: str):
        self.name = name
        self._songs = []

    def add_song(self, song_title: str):
        self._songs.append(song_title)

    def __getitem__(self, index: int):
        return self._songs[index]

    def __setitem__(self, index: int, value: str):
        self._songs[index] = value

# PATTERN: OOP Patterns (Intermediate to Advanced)

class ShoppingCart:
    def __init__(self):
        self._items = []

    def add_item(self, item_name: str):
        self._items.append(item_name)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

# PATTERN: OOP Patterns (Intermediate to Advanced)

from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class Car(Vehicle):
    def start(self):
        return "Car engine started."

    def stop(self):
        return "Car engine stopped."

# PATTERN: OOP Patterns (Intermediate to Advanced)

class Flyer:
    def fly(self):
        return "Flying high!"

class Swimmer:
    def swim(self):
        return "Swimming gracefully."

class Duck(Flyer, Swimmer):
    def quack(self):
        return "Quack!"

# PATTERN: OOP Patterns (Intermediate to Advanced)

from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    pages: int
    isbn: str = ""

# PATTERN: OOP Patterns (Intermediate to Advanced)

from dataclasses import dataclass

@dataclass
class Order:
    item_name: str
    quantity: int
    unit_price: float
    total_price: float = 0.0

    def __post_init__(self):
        self.total_price = self.quantity * self.unit_price

# PATTERN: OOP Patterns (Intermediate to Advanced)

from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

p1 = Point(10, 20)
p2 = Point(x=30, y=40)

# PATTERN: OOP Patterns (Intermediate to Advanced)

class ConfigurationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.settings = {}
        return cls._instance

    def set_setting(self, key, value):
        self.settings[key] = value

    def get_setting(self, key):
        return self.settings.get(key)

# PATTERN: OOP Patterns (Intermediate to Advanced)

class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class AnimalFactory:
    def create_animal(self, animal_type: str):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError("Unknown animal type")