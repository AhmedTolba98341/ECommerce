# config.py - Database and App Configuration

SERVER = 'VICTUS-16'
DATABASE = 'ECommerceDB'

# SQL Server Authentication (Windows Trusted Connection)
CONNECTION_STRING = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

# App Config
SECRET_KEY = 'ecommerce-secret-key-2024'
DEBUG = True
