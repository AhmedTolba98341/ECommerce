#!/usr/bin/env python
# test_db_connection.py - Test SQL Server Connection

import os
os.environ['FLASK_ENV'] = 'production'

from app import create_app
from config import CONNECTION_STRING

def test_connection():
    app = create_app()
    app.config['DEBUG'] = False
    
    print(f"Connection String: {CONNECTION_STRING}")
    print()
    
    try:
        with app.app_context():
            # Try to get database engine info
            from models import db
            
            # Test basic connection
            print("Testing connection...")
            connection = db.engine.connect()
            print("✓ Successfully connected to database!")
            
            # Get list of tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\nTables in database:")
            if tables:
                for table in tables:
                    print(f"  - {table}")
            else:
                print("  (No tables found)")
            
            connection.close()
            return True
            
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import sys
    success = test_connection()
    sys.exit(0 if success else 1)
