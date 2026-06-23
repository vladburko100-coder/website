from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    username: str = Column(String, nullable=False)
    password: str = Column(String, nullable=False)

    cart = relationship("Cart", back_populates="user", uselist=False)


class Product(Base):
    __tablename__ = "products"
    id: int = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    about = Column(String)
    price = Column(Integer)
    image = Column(String, nullable=True)


class Cart(Base):
    __tablename__ = "cart"
    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


class CartItem(Base):
    __tablename__ = "cart_items"
    id: int = Column(Integer, primary_key=True, index=True)
    cart_id: int = Column(Integer, ForeignKey("cart.id"))
    product_id: int = Column(Integer, ForeignKey("products.id"))
    quantity: int = Column(Integer, default=1)
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")