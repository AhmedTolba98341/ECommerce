"""
create_admin.py
---------------
Run this ONCE to create the first Admin account in the database.
Usage:  python create_admin.py

It will prompt for username / email / password and insert the
hashed password into the USER + ADMIN tables.
"""

from app import create_app
from models import db, User, Admin
from flask_bcrypt import Bcrypt

app    = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    print("=== Create Admin Account ===")
    username = input("Username : ").strip()
    email    = input("Email    : ").strip()
    password = input("Password : ").strip()

    if User.query.filter_by(Username=username).first():
        print("ERROR: username already exists.")
    else:
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        user   = User(Username=username, Email=email, Password=hashed, Role='Admin')
        db.session.add(user)
        db.session.flush()
        admin  = Admin(UserID=user.UserID, FullName=username)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin '{username}' created successfully.")
