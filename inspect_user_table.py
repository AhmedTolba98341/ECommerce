#!/usr/bin/env python
# inspect_user_table.py - Inspect USER table columns

import os
os.environ['FLASK_ENV'] = 'production'

from app import create_app
from sqlalchemy import inspect

def inspect_user_table():
    app = create_app()
    app.config['DEBUG'] = False
    
    try:
        with app.app_context():
            from models import db
            
            inspector = inspect(db.engine)
            
            # Get columns of USER table
            columns = inspector.get_columns('USER')
            
            print("Columns in USER table:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
            
            print("\nPrimary key:")
            pk = inspector.get_pk_constraint('USER')
            print(f"  {pk}")
            
            return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import sys
    success = inspect_user_table()
    sys.exit(0 if success else 1)
