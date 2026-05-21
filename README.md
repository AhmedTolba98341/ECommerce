# ShopEase 🛒

A full-stack **E-Commerce Management System** built with Flask, Bootstrap 5, and Microsoft SQL Server.  
Supports three user roles — **Admin**, **Manager**, and **Customer** — each with their own dedicated dashboard and feature set.

---

## ✨ Features

### 🔐 Authentication & Access Control
- Secure registration & login with **bcrypt** password hashing
- Role-based access control (Admin / Manager / Customer)
- Session management via **Flask-Login**
- CSRF protection on all forms

### 🛍️ Customer
- Browse, search, and filter products by category or brand
- Shopping cart — add, update, remove items
- Checkout with shipping address & payment method selection
- Order history & detailed order tracking
- Payment history
- Submit and view approved product reviews

### 🖥️ Admin
- Dashboard KPIs — total revenue, orders, customers
- Full **CRUD** for products, categories, and brands
- User management — activate / deactivate accounts, promote to manager
- Payment verification (Approve / Reject)
- Review moderation (Approve / Reject)
- Order status management
- Discount creation and assignment to products
- Business reports

### 📊 Manager
- Analytics dashboard — revenue, order stats, top-selling products
- Sales reports by category and status

---

## 🗄️ Database Schema — 17 Tables (3NF)

```
USER · CUSTOMER · ADMIN · MANAGER
PRODUCT · CATEGORY · BRAND
SHOPPING_CART · CART_ITEM
ORDER · ORDER_ITEM
PAYMENT · PAYMENT_METHOD
REVIEW
DISCOUNT · PRODUCT_DISCOUNT
REPORT
```

---

## 🛠️ Tech Stack

| Layer       | Technology                              |
|-------------|------------------------------------------|
| Backend     | Python 3.13 · Flask 3.0                 |
| Database    | Microsoft SQL Server 2022 · SQLAlchemy  |
| Auth        | Flask-Login · Flask-Bcrypt              |
| Forms       | Flask-WTF · WTForms                     |
| Frontend    | Jinja2 · Bootstrap 5 · Vanilla JS       |
| DB Driver   | pyodbc + ODBC Driver 17                 |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Microsoft SQL Server (Express is fine)
- [ODBC Driver 17 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/shopease.git
cd shopease
```

### 2. Create & activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

```bash
cp config.example.py config.py
```

Open `config.py` and set your SQL Server name:

```python
SERVER   = 'YOUR_SERVER_NAME'   # e.g. localhost or DESKTOP-XYZ\SQLEXPRESS
DATABASE = 'ECommerceDB'
```

For **SQL Server Authentication** instead of Windows Auth, uncomment Option B in `config.example.py`.

### 5. Set up the database

```bash
# Create tables
python init_db.py

# Seed sample data (8 products, 5 categories, 5 brands)
python seed_db.py
```

Or run the seed SQL directly in SSMS:

```sql
-- In SSMS, open seed_data.sql and run against ECommerceDB
```

### 6. Create an admin account

```bash
python create_admin.py
```

### 7. Run the app

```bash
python app.py
```

Visit: **http://127.0.0.1:5000**

---

## 👤 Default Test Accounts

| Role     | Username | Password |
|----------|----------|----------|
| Admin    | admin    | admin123 |


---

## 📁 Project Structure

```
shopease/
├── app.py                  # Application factory & public routes
├── config.py               # DB connection & secret key (not committed)
├── config.example.py       # Safe template — copy to config.py
├── models.py               # 17 SQLAlchemy models
├── forms.py                # WTForms validation
├── requirements.txt
│
├── routes/
│   ├── auth_routes.py      # /login  /register  /logout
│   ├── admin_routes.py     # /admin/...
│   ├── customer_routes.py  # /customer/...
│   └── manager_routes.py   # /manager/...
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── product_detail.html
│   ├── login.html
│   ├── register.html
│   ├── admin/
│   ├── customer/
│   └── manager/
│
├── static/
│   ├── css/style.css
│   └── js/main.js
│
├── init_db.py              # Create all tables
├── seed_db.py              # Insert sample data
├── seed_data.sql           # Raw SQL seed
├── create_admin.py         # Interactive admin account creator
└── drop_and_recreate_db.py # Hard reset (dev only)
```

---

## 🔒 Security Notes

- Passwords are hashed with **bcrypt** — plain-text passwords are never stored.
- All forms use **CSRF tokens** via Flask-WTF.
- Database queries go through **SQLAlchemy ORM** — no raw string interpolation.
- Role-based decorators protect every sensitive route.
- `config.py` (with real credentials) is excluded from version control via `.gitignore`.

---

## 📄 License

This project is for educational purposes.
