from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Boolean,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType

# databse connection
db = create_engine("sqlite:///database.db")

# Base class for declarative models
Base = declarative_base()


# Create the User model
class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)
    active = Column("active", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

class Order(Base):
    __tablename__ = "orders"

    STATUS_ORDER = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    status = Column("status", ChoiceType(STATUS_ORDER), default="pending")
    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    price = Column("price", Float, nullable=False)

    def __init__(self, status, user, price):
        self.status = status
        self.user = user
        self.price = price

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer, nullable=False)
    flavor = Column("flavor", String, nullable=False)
    size = Column("size", String, nullable=False)
    unitary_price = Column("unitary_price", Float, nullable=False)
    order_id = Column("order_id", Integer, ForeignKey("orders.id"), nullable=False)

    def __init__(self, order_id, product_name, quantity):
        self.order_id = order_id
        self.product_name = product_name
        self.quantity = quantity