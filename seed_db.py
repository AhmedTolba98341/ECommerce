#!/usr/bin/env python
# seed_db.py - Seed Database with Sample Data

import os
import sys
os.environ['FLASK_ENV'] = 'production'

from app import create_app, db, bcrypt
from models import User, Admin, Customer, Category, Brand, Product, Discount, PaymentMethod

def seed_database():
    """Seed database with sample data."""
    app = create_app()
    app.config['DEBUG'] = False
    
    with app.app_context():
        print("Seeding database...")
        try:
            # Create admin user
            admin_user = User.query.filter_by(Username='admin').first()
            if not admin_user:
                admin_password_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')
                admin_user = User(
                    Username='admin',
                    Email='admin@shopease.com',
                    Password=admin_password_hash,
                    Role='Admin',
                    IsActive=True
                )
                db.session.add(admin_user)
                db.session.commit()
                
                admin_profile = Admin(UserID=admin_user.UserID, FullName='System Administrator')
                db.session.add(admin_profile)
                db.session.commit()
                print("✓ Admin user created (username: admin, password: admin123)")
            
            # Payment Methods
            if PaymentMethod.query.count() == 0:
                methods = [
                    PaymentMethod(MethodName='Credit Card'),
                    PaymentMethod(MethodName='Cash on Delivery'),
                    PaymentMethod(MethodName='Bank Transfer')
                ]
                db.session.add_all(methods)
                db.session.commit()
                print("✓ Payment methods created")
            
            # Categories
            if Category.query.count() == 0:
                categories = [
                    Category(CategoryName='Electronics', Description='Phones, laptops, gadgets'),
                    Category(CategoryName='Clothing', Description='Apparel for men and women'),
                    Category(CategoryName='Books', Description='Fiction and non-fiction'),
                    Category(CategoryName='Home & Garden', Description='Furniture, decor, tools'),
                    Category(CategoryName='Sports', Description='Equipment and apparel')
                ]
                db.session.add_all(categories)
                db.session.commit()
                print("✓ Categories created")
            
            # Brands
            if Brand.query.count() == 0:
                brands = [
                    Brand(BrandName='Apple', Country='USA'),
                    Brand(BrandName='Samsung', Country='South Korea'),
                    Brand(BrandName='Nike', Country='USA'),
                    Brand(BrandName='Adidas', Country='Germany'),
                    Brand(BrandName='Sony', Country='Japan')
                ]
                db.session.add_all(brands)
                db.session.commit()
                print("✓ Brands created")
            
            # Products
            if Product.query.count() == 0:
                products = [
                    Product(ProductName='iPhone 15', Description='Latest Apple smartphone', 
                           Price=999.99, Stock=50, CategoryID=1, BrandID=1, IsActive=True),
                    Product(ProductName='Samsung Galaxy S24', Description='Flagship Android phone',
                           Price=849.99, Stock=40, CategoryID=1, BrandID=2, IsActive=True),
                    Product(ProductName='Sony WH-1000XM5', Description='Noise-cancelling headphones',
                           Price=349.99, Stock=30, CategoryID=1, BrandID=5, IsActive=True),
                    Product(ProductName='Nike Air Max 270', Description='Comfortable running shoes',
                           Price=129.99, Stock=60, CategoryID=5, BrandID=3, IsActive=True),
                    Product(ProductName='Adidas Ultraboost', Description='Performance running shoe',
                           Price=159.99, Stock=45, CategoryID=5, BrandID=4, IsActive=True),
                    Product(ProductName='Clean Code', Description='Book by Robert C. Martin',
                           Price=34.99, Stock=20, CategoryID=3, BrandID=1, IsActive=True),
                    Product(ProductName='Nike Dri-FIT Tee', Description='Lightweight training shirt',
                           Price=29.99, Stock=80, CategoryID=2, BrandID=3, IsActive=True),
                    Product(ProductName='Samsung 4K Monitor', Description='27-inch UHD display',
                           Price=399.99, Stock=15, CategoryID=1, BrandID=2, IsActive=True)
                ]
                db.session.add_all(products)
                db.session.commit()
                print("✓ Products created")
            
            # Discounts
            if Discount.query.count() == 0:
                discounts = [
                    Discount(DiscountName='Summer Sale', DiscountPercent=10.00, IsActive=True),
                    Discount(DiscountName='Flash Deal', DiscountPercent=20.00, IsActive=True)
                ]
                db.session.add_all(discounts)
                db.session.commit()
                print("✓ Discounts created")
            
            print("\n✓ Database seeded successfully!")
            return True
            
        except Exception as e:
            print(f"✗ Error seeding database: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = seed_database()
    sys.exit(0 if success else 1)
