# PATTERN: Database Patterns (SQLAlchemy Basics)

from sqlalchemy import create_engine

# Create an in-memory SQLite database engine
engine = create_engine("sqlite:///:memory:")

# For a file-based SQLite database:
# engine = create_engine("sqlite:///my_database.db")

# For PostgreSQL:
# engine = create_engine("postgresql://user:password@host:port/database")

# PATTERN: Database Patterns (SQLAlchemy Basics)

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Define the declarative base
Base = declarative_base()

# Define a simple User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

# PATTERN: Database Patterns (SQLAlchemy Basics)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Assume engine is already created
engine = create_engine("sqlite:///:memory:")

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Use the session in a context manager for automatic closing
with Session() as session:
    # Perform database operations within this block
    pass

# PATTERN: Database Patterns (SQLAlchemy Basics)

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session() as session:
    session.add(Product(name="Laptop"))
    session.add(Product(name="Mouse"))
    session.commit()

    # Query for a product with a specific name
    laptop = session.query(Product).filter(Product.name == "Laptop").first()
    # print(laptop.name)

# PATTERN: Database Patterns (SQLAlchemy Basics)

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session() as session:
    # Create a new object
    new_customer = Customer(name="Alice Smith")

    # Add the object to the session
    session.add(new_customer)
    session.commit() # Commit to save to the database

    # print(f"Added customer with ID: {new_customer.id}")

# PATTERN: Database Patterns (SQLAlchemy Basics)

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True) # Unique constraint to trigger error

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session() as session:
    try:
        session.add(Item(name="Pen"))
        session.commit() # Successful commit

        session.add(Item(name="Pen")) # This will cause a unique constraint error
        session.commit() # This commit will fail
    except Exception:
        session.rollback() # Rollback changes if an error occurs
        # print("Transaction failed and rolled back.")
    # finally:
        # Optional cleanup or verification