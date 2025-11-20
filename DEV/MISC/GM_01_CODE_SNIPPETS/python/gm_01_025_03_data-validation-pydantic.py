# PATTERN: Data Validation (Pydantic)

from pydantic import BaseModel

class UserProfile(BaseModel):
    user_id: int
    username: str
    email: str | None = None
    is_active: bool = True

user = UserProfile(user_id=123, username="john_doe")
print(user.model_dump_json(indent=2))

# PATTERN: Data Validation (Pydantic)

from pydantic import BaseModel, Field

class Product(BaseModel):
    product_id: str = Field(min_length=5, max_length=10)
    name: str = Field(..., min_length=3)
    price: float = Field(gt=0, le=1000)
    quantity: int = Field(ge=0)

try:
    product = Product(product_id="P12345", name="Laptop", price=999.99, quantity=10)
    print(product.model_dump_json(indent=2))
except Exception as e:
    print(e)

# PATTERN: Data Validation (Pydantic)

from pydantic import BaseModel, ValidationError

class SensorData(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float
    timestamp: int

data = {
    "sensor_id": "S001",
    "temperature": 25.5,
    "humidity": 60.2,
    "timestamp": 1678886400
}

try:
    sensor_reading = SensorData.model_validate(data)
    print(sensor_reading.model_dump_json(indent=2))
except ValidationError as e:
    print(e.json(indent=2))

# PATTERN: Data Validation (Pydantic)

from pydantic import BaseModel

class Order(BaseModel):
    order_id: str
    customer_id: int
    total_amount: float
    status: str = "pending"

order_instance = Order(order_id="ORD-001", customer_id=456, total_amount=120.50)

# Dump to a dictionary
order_dict = order_instance.model_dump()
print(f"Full dictionary: {order_dict}")

# Dump excluding unset fields (status was set by default, so it's included)
order_dict_exclude_unset = order_instance.model_dump(exclude_unset=True)
print(f"Exclude unset: {order_dict_exclude_unset}")

# PATTERN: Data Validation (Pydantic)

from pydantic import BaseModel, ValidationError, field_validator

class UserRegistration(BaseModel):
    username: str
    password: str
    email: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()

try:
    user = UserRegistration(username="TestUser123", password="SecurePassword", email="test@example.com")
    print(user.model_dump_json(indent=2))

    UserRegistration(username="Invalid User!", password="P", email="a@b.com")
except ValidationError as e:
    print(e.json(indent=2))

# PATTERN: Data Validation (Pydantic)

from pydantic import BaseModel, Field, ValidationError

class APIResponse(BaseModel):
    data_id: str = Field(alias="id")
    message: str

    class Config:
        populate_by_name = True # Allow using 'id' instead of 'data_id' for input
        extra = 'forbid' # Forbid any extra fields not defined in the model

try:
    # Using alias 'id' for input
    response = APIResponse(id="abc-123", message="Success")
    print(response.model_dump_json(indent=2))

    # Attempting to pass an extra field
    APIResponse(id="def-456", message="Error", extra_field="oops")
except ValidationError as e:
    print(e.json(indent=2))