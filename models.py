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

# Conexão com o banco de dados SQLite
db = create_engine("sqlite:///database.db")

# Cria a base do banco de dados
Base = declarative_base()


# Tabela para os usuários
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


# Tabela para os pedidos
class Order(Base):
    __tablename__ = "orders"

    # STATUS_ORDER = [
    #     ("pending", "Pending"),
    #     ("completed", "Completed"),
    #     ("cancelled", "Cancelled"),
    # ]

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String, default="pending")
    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    price = Column("price", Float, nullable=False)

    def __init__(self, user_id, status="pending", price=0):
        self.status = status
        self.user_id = user_id
        self.price = price


# Tabela para os itens do pedido
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer, nullable=False)
    flavor = Column("flavor", String, nullable=False)
    size = Column("size", String, nullable=False)
    unitary_price = Column("unitary_price", Float, nullable=False)
    order_id = Column("order_id", Integer, ForeignKey("orders.id"), nullable=False)

    def __init__(self, order_id, quantity, flavor, size, unitary_price):
        self.order_id = order_id
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unitary_price = unitary_price


# alembic init alembic
# alterar env.py
# alterar alembic.ini
# alembic revision --autogenerate -m "Initial Migration"
# alembic upgrade head

# se deu erro
# deletar version e .db
# executa novamente alembic revision --autogenerate -m "Initial Migration"

# sempre quando houver alteraçao do banco, é necessario migrar:
# alembic revision --autogenerate -m "remove admin"
# alembic upgrade head
