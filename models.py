# models.py - SQLAlchemy Models for ECommerceDB

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# ─────────────────────────────────────────────
# USER (base login entity)
# ─────────────────────────────────────────────
class User(db.Model, UserMixin):
    __tablename__ = 'USER'

    UserID      = db.Column(db.Integer, primary_key=True)
    Username    = db.Column(db.String(50), unique=True, nullable=False)
    Email       = db.Column(db.String(100), unique=True, nullable=False)
    Password    = db.Column(db.String(255), nullable=False)
    Role        = db.Column(db.String(20), nullable=False)   # Admin / Customer / Manager
    CreatedAt   = db.Column(db.DateTime, default=datetime.utcnow)
    IsActive    = db.Column(db.Boolean, default=True)

    # Relationships
    customer    = db.relationship('Customer', backref='user', uselist=False)
    admin       = db.relationship('Admin',    backref='user', uselist=False)
    manager     = db.relationship('Manager', backref='user', uselist=False)

    def get_id(self):
        return str(self.UserID)


# ─────────────────────────────────────────────
# CUSTOMER
# ─────────────────────────────────────────────
class Customer(db.Model):
    __tablename__ = 'CUSTOMER'

    CustomerID  = db.Column(db.Integer, primary_key=True)
    UserID      = db.Column(db.Integer, db.ForeignKey('USER.UserID'), nullable=False)
    FullName    = db.Column(db.String(100), nullable=False)
    Phone       = db.Column(db.String(20))
    Address     = db.Column(db.String(255))

    # Relationships
    cart        = db.relationship('ShoppingCart', backref='customer', uselist=False)
    orders      = db.relationship('Order', backref='customer')
    reviews     = db.relationship('Review', backref='customer')
    payments    = db.relationship('Payment', backref='customer')


# ─────────────────────────────────────────────
# ADMIN
# ─────────────────────────────────────────────
class Admin(db.Model):
    __tablename__ = 'ADMIN'

    AdminID     = db.Column(db.Integer, primary_key=True)
    UserID      = db.Column(db.Integer, db.ForeignKey('USER.UserID'), nullable=False)
    FullName    = db.Column(db.String(100), nullable=False)


# ─────────────────────────────────────────────
# MANAGER
# ─────────────────────────────────────────────
class Manager(db.Model):
    __tablename__ = 'MANAGER'

    ManagerID   = db.Column(db.Integer, primary_key=True)
    UserID      = db.Column(db.Integer, db.ForeignKey('USER.UserID'), nullable=False)
    FullName    = db.Column(db.String(100), nullable=False)


# ─────────────────────────────────────────────
# CATEGORY
# ─────────────────────────────────────────────
class Category(db.Model):
    __tablename__ = 'CATEGORY'

    CategoryID   = db.Column(db.Integer, primary_key=True)
    CategoryName = db.Column(db.String(100), unique=True, nullable=False)
    Description  = db.Column(db.Text)

    products     = db.relationship('Product', backref='category')


# ─────────────────────────────────────────────
# BRAND
# ─────────────────────────────────────────────
class Brand(db.Model):
    __tablename__ = 'BRAND'

    BrandID     = db.Column(db.Integer, primary_key=True)
    BrandName   = db.Column(db.String(100), unique=True, nullable=False)
    Country     = db.Column(db.String(50))

    products    = db.relationship('Product', backref='brand')


# ─────────────────────────────────────────────
# PRODUCT
# ─────────────────────────────────────────────
class Product(db.Model):
    __tablename__ = 'PRODUCT'

    ProductID   = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(150), nullable=False)
    Description = db.Column(db.Text)
    Price       = db.Column(db.Numeric(10, 2), nullable=False)
    Stock       = db.Column(db.Integer, default=0)
    ImageURL    = db.Column(db.String(255))
    CategoryID  = db.Column(db.Integer, db.ForeignKey('CATEGORY.CategoryID'))
    BrandID     = db.Column(db.Integer, db.ForeignKey('BRAND.BrandID'))
    IsActive    = db.Column(db.Boolean, default=True)
    CreatedAt   = db.Column(db.DateTime, default=datetime.utcnow)

    cart_items  = db.relationship('CartItem',   backref='product')
    order_items = db.relationship('OrderItem',  backref='product')
    reviews     = db.relationship('Review',     backref='product')
    discounts   = db.relationship('ProductDiscount', backref='product')


# ─────────────────────────────────────────────
# SHOPPING CART
# ─────────────────────────────────────────────
class ShoppingCart(db.Model):
    __tablename__ = 'SHOPPING_CART'

    CartID      = db.Column(db.Integer, primary_key=True)
    CustomerID  = db.Column(db.Integer, db.ForeignKey('CUSTOMER.CustomerID'), nullable=False)
    CreatedAt   = db.Column(db.DateTime, default=datetime.utcnow)

    items       = db.relationship('CartItem', backref='cart', cascade='all, delete-orphan')


# ─────────────────────────────────────────────
# CART ITEM
# ─────────────────────────────────────────────
class CartItem(db.Model):
    __tablename__ = 'CART_ITEM'

    CartItemID  = db.Column(db.Integer, primary_key=True)
    CartID      = db.Column(db.Integer, db.ForeignKey('SHOPPING_CART.CartID'), nullable=False)
    ProductID   = db.Column(db.Integer, db.ForeignKey('PRODUCT.ProductID'), nullable=False)
    Quantity    = db.Column(db.Integer, default=1)


# ─────────────────────────────────────────────
# ORDER
# ─────────────────────────────────────────────
class Order(db.Model):
    __tablename__ = 'ORDER'

    OrderID         = db.Column(db.Integer, primary_key=True)
    CustomerID      = db.Column(db.Integer, db.ForeignKey('CUSTOMER.CustomerID'), nullable=False)
    OrderDate       = db.Column(db.DateTime, default=datetime.utcnow)
    TotalAmount     = db.Column(db.Numeric(10, 2))
    DeliveryFee     = db.Column(db.Numeric(10, 2), default=5.00)  # Default delivery fee
    Status          = db.Column(db.String(50), default='Pending')   # Pending/Processing/Shipped/Delivered/Cancelled
    ShippingAddress = db.Column(db.String(255))

    order_items     = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')
    payment         = db.relationship('Payment',   backref='order', uselist=False)


# ─────────────────────────────────────────────
# ORDER ITEM
# ─────────────────────────────────────────────
class OrderItem(db.Model):
    __tablename__ = 'ORDER_ITEM'

    OrderItemID = db.Column(db.Integer, primary_key=True)
    OrderID     = db.Column(db.Integer, db.ForeignKey('ORDER.OrderID'), nullable=False)
    ProductID   = db.Column(db.Integer, db.ForeignKey('PRODUCT.ProductID'), nullable=False)
    Quantity    = db.Column(db.Integer, nullable=False)
    UnitPrice   = db.Column(db.Numeric(10, 2), nullable=False)


# ─────────────────────────────────────────────
# PAYMENT METHOD
# ─────────────────────────────────────────────
class PaymentMethod(db.Model):
    __tablename__ = 'PAYMENT_METHOD'

    MethodID    = db.Column(db.Integer, primary_key=True)
    MethodName  = db.Column(db.String(50), nullable=False)   # Credit Card / Cash / Bank Transfer

    payments    = db.relationship('Payment', backref='method')


# ─────────────────────────────────────────────
# PAYMENT
# ─────────────────────────────────────────────
class Payment(db.Model):
    __tablename__ = 'PAYMENT'

    PaymentID   = db.Column(db.Integer, primary_key=True)
    OrderID     = db.Column(db.Integer, db.ForeignKey('ORDER.OrderID'), nullable=False)
    CustomerID  = db.Column(db.Integer, db.ForeignKey('CUSTOMER.CustomerID'), nullable=False)
    MethodID    = db.Column(db.Integer, db.ForeignKey('PAYMENT_METHOD.MethodID'))
    Amount      = db.Column(db.Numeric(10, 2), nullable=False)
    Status      = db.Column(db.String(30), default='Pending')   # Pending / Verified / Rejected
    PaymentDate = db.Column(db.DateTime, default=datetime.utcnow)


# ─────────────────────────────────────────────
# REVIEW
# ─────────────────────────────────────────────
class Review(db.Model):
    __tablename__ = 'REVIEW'

    ReviewID    = db.Column(db.Integer, primary_key=True)
    ProductID   = db.Column(db.Integer, db.ForeignKey('PRODUCT.ProductID'), nullable=False)
    CustomerID  = db.Column(db.Integer, db.ForeignKey('CUSTOMER.CustomerID'), nullable=False)
    Rating      = db.Column(db.Integer, nullable=False)   # 1–5
    Comment     = db.Column(db.Text)
    Status      = db.Column(db.String(20), default='Pending')   # Pending / Approved / Rejected
    CreatedAt   = db.Column(db.DateTime, default=datetime.utcnow)


# ─────────────────────────────────────────────
# DISCOUNT
# ─────────────────────────────────────────────
class Discount(db.Model):
    __tablename__ = 'DISCOUNT'

    DiscountID      = db.Column(db.Integer, primary_key=True)
    DiscountName    = db.Column(db.String(100), nullable=False)
    DiscountPercent = db.Column(db.Numeric(5, 2), nullable=False)
    StartDate       = db.Column(db.DateTime)
    EndDate         = db.Column(db.DateTime)
    IsActive        = db.Column(db.Boolean, default=True)

    products        = db.relationship('ProductDiscount', backref='discount')


# ─────────────────────────────────────────────
# PRODUCT DISCOUNT (junction)
# ─────────────────────────────────────────────
class ProductDiscount(db.Model):
    __tablename__ = 'PRODUCT_DISCOUNT'

    ID          = db.Column(db.Integer, primary_key=True)
    ProductID   = db.Column(db.Integer, db.ForeignKey('PRODUCT.ProductID'), nullable=False)
    DiscountID  = db.Column(db.Integer, db.ForeignKey('DISCOUNT.DiscountID'), nullable=False)


# ─────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────
class Report(db.Model):
    __tablename__ = 'REPORT'

    ReportID    = db.Column(db.Integer, primary_key=True)
    ReportType  = db.Column(db.String(100), nullable=False)
    GeneratedBy = db.Column(db.Integer, db.ForeignKey('USER.UserID'))
    GeneratedAt = db.Column(db.DateTime, default=datetime.utcnow)
    Data        = db.Column(db.Text)
