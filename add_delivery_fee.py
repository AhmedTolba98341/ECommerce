#!/usr/bin/env python
"""
Add DeliveryFee column to ORDER table
"""
import pyodbc

# Connection string using Windows authentication
CONNECTION_STRING = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=VICTUS-16;"
    "Database=ECommerceDB;"
    "Trusted_Connection=yes;"
)

def add_delivery_fee_column():
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'ORDER' AND COLUMN_NAME = 'DeliveryFee'
        """)
        
        if cursor.fetchone():
            print("✓ DeliveryFee column already exists")
        else:
            # Add the column
            cursor.execute("""
                ALTER TABLE [ORDER] 
                ADD DeliveryFee NUMERIC(10, 2) DEFAULT 5.00
            """)
            conn.commit()
            print("✓ DeliveryFee column added successfully")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == '__main__':
    add_delivery_fee_column()
