from email.policy import default
from sqlalchemy.sql import func
import sqlalchemy
from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    String,
    Table,
    DateTime,
    Boolean,
)

from core.database import schema

metadata = sqlalchemy.MetaData(schema=schema)

User = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("first_name", String(255), nullable=True),
    Column("last_name", String(255), nullable=True),
    Column("contact", String(127), nullable=True, default=None),
    Column("email", String(255), unique=True, nullable=True),
    Column("username", String(255), unique=True, nullable=True),
    Column("active", Boolean, nullable=True, default=False),
    Column("password", String(255), nullable=True),
    Column("company_name", String(255), nullable=True, default=None),
    Column("address", String(511), nullable=True, default=None),
    Column("city", String(127), nullable=True, default=None),
    Column("country", String(127), nullable=True, default=None),
    Column("postal_code", String(255), nullable=True, default=None),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)

#Product Category table
ProductCategory = Table(
    "product_category",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("name", String(255), nullable=False, unique=True),
    Column("description", String(255), nullable=True),
    Column(
        "created_by",
        Integer,
        ForeignKey("user.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "updated_by",
        Integer,
        ForeignKey("user.id", ondelete="RESTRICT"),
        nullable=True,
    ),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)


# Product table
Product = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("category_id", Integer, ForeignKey("product_category.id", ondelete="RESTRICT"), nullable=False),
    Column("name", String(255), nullable=False, unique=True),
    Column("uom", String(255), nullable=True),
    Column("description", String(255), nullable=True),
    Column("price", Float, nullable=True, default=None),
    Column(
        "created_by",
        Integer,
        ForeignKey("user.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "updated_by",
        Integer,
        ForeignKey("user.id", ondelete="RESTRICT"),
        nullable=True,
    ),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)

# Inventory table
Inventory = Table(
    "inventory",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("product_id", Integer, ForeignKey("product.id", ondelete="RESTRICT"), nullable=False),
    Column("quantity", Float, nullable=False),
    Column("threshold", Integer, nullable=True, default=None),
    Column(
        "created_by",
        Integer,
        ForeignKey("user.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "updated_by",
        Integer,
        ForeignKey("user.id", ondelete="RESTRICT"),
        nullable=True,
    ),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)

# Sales table
SaleOrder = Table(
    "sale_order",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("name", String(255), nullable=False, unique=True),
    Column("description", String(255), nullable=True),
    Column("date", DateTime),
    Column("customer_id", Integer, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False),
    Column("product_id", Integer, ForeignKey("product.id", ondelete="RESTRICT"), nullable=False),
    Column("quantity", Float, nullable=False),
    Column("price", Float, nullable=False),
    Column("total", Float, nullable=False),
    Column(
        "created_by",
        Integer,
        ForeignKey("user.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "updated_by",
        Integer,
        ForeignKey("user.id", ondelete="RESTRICT"),
        nullable=True,
    ),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)
