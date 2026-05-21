# 🛒 ShopEase – E-Commerce Management System

A **production-ready full-stack E-Commerce Management System** built with Flask, Bootstrap, and Microsoft SQL Server.

**Status:** ✅ **FULLY OPERATIONAL** | **Database:** ECommerceDB (SQL Server 2022) | **Version:** 1.0.0

---

## 🎯 Quick Start

```bash
# Activate environment
.\.venv\Scripts\activate

# Run application
python app.py

# Access in browser
http://127.0.0.1:5000

# Test Login
Username: admin
Password: admin123
```

---

## 📚 DOCUMENTATION

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **[ARCHITECTURE.md](./ARCHITECTURE.md)** | Complete technical reference | ⭐⭐⭐ 20 min |
| **[VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md)** | Proof all systems operational | ⭐⭐⭐ 10 min |

---

## 📊 TECH STACK - VERIFIED ✅

| Layer      | Technology                    | Version | Status |
|------------|-------------------------------|---------|--------|
| **Frontend** | HTML5 + Bootstrap + JavaScript | Latest | ✅ |
| **Backend** | Flask | 3.0.3 | ✅ |
| **Database** | SQL Server | 2022 | ✅ Connected |
| **Auth** | Flask-Login + bcrypt | Latest | ✅ |
| **DB Access** | SQLAlchemy + pyodbc | 2.0.31 + 5.3.0 | ✅ |
| **Reports** | SQL Queries | Native | ✅ |
| **Design** | ERD + 3NF Schema | 17 tables | ✅ |

---

## 📁 Project Structure

```
ECommerceProject/
├── 📚 ARCHITECTURE.md                      ← Technical Docs
├── 📚 VERIFICATION_REPORT.md               ← Proof of Functionality
├── README.md                               ← This File
│
├── 🐍 app.py                               # Flask Application
├── ⚙️  config.py                            # Database Config
├── 📦 models.py                            # 17 SQLAlchemy Models
├── 📋 forms.py                             # WTForms Validation
├── 📝 requirements.txt                     # Python Packages
│
├── 🔧 SETUP & MANAGEMENT SCRIPTS
│   ├── init_db.py                    # Initialize Database
│   ├── seed_db.py                    # Seed Sample Data
│   ├── drop_and_recreate_db.py       # Reset Database
│   └── comprehensive_stack_verification.py # Full Stack Check
│
├── routes/                           # 44 Routes Total
│   ├── auth_routes.py               # Login / Register / Logout
│   ├── admin_routes.py              # Admin Management
│   ├── customer_routes.py           # Shopping & Orders
│   └── manager_routes.py            # Sales Reports
│
├── templates/                        # 25+ Pages
│   ├── base.html                    # Master Layout
│   ├── index.html, login.html, register.html, products.html
│   ├── admin/                       # 8+ Admin Templates
│   ├── customer/                    # 9+ Customer Templates
│   └── manager/                     # 2+ Manager Templates
│
└── static/                           # Frontend Assets
    ├── css/style.css                # Custom Styles
    ├── js/main.js                   # JavaScript
    └── images/                      # Images
```

---

## ✨ FEATURES

### ✅ Authentication & Users
- User Registration with Email Validation
- Secure Login (bcrypt + Flask-Login)
- Role-Based Access Control (Admin, Customer, Manager)
- Session Management
- User Profiles

### ✅ Product Catalog
- 8 Sample Products
- 5 Categories & 5 Brands
- Product Search & Filtering
- Stock Tracking
- Product Details Pages

### ✅ Shopping Features
- Add to Cart
- Shopping Cart Management
- Quantity Adjustment
- Checkout Process
- Order Creation

### ✅ Order Management
- Order History
- Order Details
- Order Status Tracking
- Payment Processing

### ✅ Reviews & Ratings
- Product Reviews
- 1-5 Star Ratings
- Review Moderation

### ✅ Admin Dashboard
- Product CRUD
- Category Management
- Brand Management
- User Management
- Order Management
- Payment Tracking
- Discount Management
- Analytics & Reports

### ✅ Security
- CSRF Token Protection
- bcrypt Password Hashing
- Session-Based Authentication
- Role-Based Access Control
- SQL Injection Prevention
- Form Validation

---

## 🗄️ DATABASE

### Connection Details ✅
- **Server:** VICTUS-16
- **Database:** ECommerceDB
- **DBMS:** SQL Server 2022
- **Driver:** ODBC Driver 17
- **Status:** ✅ Connected & Verified

### Schema (17 Tables - 3NF Normalized)
```
✓ USER              - User accounts
✓ CUSTOMER          - Customer profiles
✓ ADMIN             - Admin profiles
✓ MANAGER           - Manager profiles
✓ PRODUCT           - Product catalog
✓ CATEGORY          - Categories
✓ BRAND             - Brands
✓ SHOPPING_CART     - Shopping carts
✓ CART_ITEM         - Cart items
✓ ORDER             - Orders
✓ ORDER_ITEM        - Order items
✓ PAYMENT           - Payments
✓ PAYMENT_METHOD    - Payment methods
✓ REVIEW            - Product reviews
✓ DISCOUNT          - Discounts
✓ PRODUCT_DISCOUNT  - Product-Discount junction
✓ REPORT            - Business reports
```

---

## 🚀 RUNNING THE APPLICATION

### Prerequisites
- Python 3.13+
- SQL Server 2022
- ODBC Driver 17
- Virtual Environment

### Setup (One-time)
```bash
# Create virtual environment
python -m venv .venv

# Activate
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Seed sample data
python seed_db.py
```

### Start Application
```bash
# Activate environment
.\.venv\Scripts\activate

# Run Flask
python app.py

# Access
http://127.0.0.1:5000
```

---

## ✅ VERIFICATION

### Run Verification Scripts
```bash
# Complete stack verification
python comprehensive_stack_verification.py
```

### Expected Output ✅
```
✓ Frontend:        HTML + Bootstrap + JavaScript
✓ Backend:         Flask (44 routes)
✓ Database:        SQL Server 2022 (17 tables)
✓ Authentication:  Flask-Login + bcrypt
✓ Database Access: SQLAlchemy ORM + pyodbc
✓ Reports:         SQL queries
✓ Design:          3NF normalized schema
```

---

## 👤 TEST ACCOUNTS

| Username | Password | Role | Email |
|----------|----------|------|-------|
| admin | admin123 | Admin | admin@shopease.com |
| noname | (registered) | Customer | aafmt@gmail.com |

---

## 📊 STATISTICS

```
Code Metrics:
  - Python Modules: 20+
  - HTML Templates: 25+
  - Routes: 44
  - Database Tables: 17
  - ORM Models: 17
  - Forms: 8+
  - Lines of Code: 5,000+

Database:
  - Entities: 17
  - Sample Data: 8 products, 5 categories, 5 brands
  - Normalization: 3NF

Application:
  - Framework: Flask 3.0.3
  - Database: SQL Server 2022
  - Status: ✅ Running
```

---

## 📚 Project Structure Details
    ├── css/style.css
    └── js/main.js
```

---

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- Microsoft SQL Server (with ODBC Driver 17)
- SSMS (to run setup SQL)

### 2. Database Setup

1. Open SSMS and create the database:
   ```sql
   CREATE DATABASE ECommerceDB;
   ```
2. Create all 17 tables (schema must already exist as per project spec).
3. Run the seed data:
   ```
   Open seed_data.sql in SSMS and execute against ECommerceDB
   ```

### 3. Configure Connection

Edit `config.py` and set your SQL Server name:
```python
SERVER   = 'YOUR_SERVER_NAME'   # e.g. DESKTOP-ABC\SQLEXPRESS
DATABASE = 'ECommerceDB'
```

For **SQL Server Authentication** (username/password), change to:
```python
CONNECTION_STRING = (
    f"mssql+pyodbc://sa:yourpassword@{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)
```

### 4. Install Dependencies

```bash
cd ECommerceProject
pip install -r requirements.txt
```

### 5. Create Admin Account

```bash
python create_admin.py
```

Follow the prompts to set username / email / password.

### 6. Run the App

```bash
python app.py
```

Visit: **http://127.0.0.1:5000**

---

## Role Features

### Admin
- Dashboard with KPIs (revenue, orders, customers)
- Add / Edit / Deactivate products
- Manage categories and brands
- View & toggle users; add managers
- Verify or reject payments
- Moderate reviews (approve/reject)
- Change order statuses
- Manage discounts
- Full reports dashboard

### Customer
- Register & login
- Browse / search / filter products
- Shopping cart (add, update, remove)
- Checkout with payment method selection
- Order history & order detail
- Payment history
- Submit & view reviews

### Manager
- Analytics dashboard (revenue, orders, top products)
- Sales reports by category and status

---

## Validation

- Frontend: HTML5 required / type / min attributes
- Backend: WTForms validators (DataRequired, Email, Length, NumberRange, EqualTo)
- CSRF protection on all forms via Flask-WTF

## Security

- Passwords hashed with bcrypt
- Role-based decorators on every protected route
- Parameterized queries via SQLAlchemy ORM
- CSRF tokens on all POST forms

---

## Default Admin Login

If you ran `seed_data.sql`, a test admin exists:

| Field    | Value             |
|----------|-------------------|
| Username | admin             |
| Password | admin123          |

> **Change this password immediately in production.**
