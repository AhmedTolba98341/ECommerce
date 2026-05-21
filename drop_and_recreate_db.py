#!/usr/bin/env python
# drop_and_recreate_db.py - Drop all tables and recreate

import os
os.environ['FLASK_ENV'] = 'production'

from app import create_app, db

def drop_and_recreate():
    app = create_app()
    app.config['DEBUG'] = False
    
    try:
        with app.app_context():
            print("Dropping all tables...")
            db.drop_all()
            print("✓ All tables dropped")
            
            print("\nCreating tables with correct schema...")
            db.create_all()
            print("✓ All tables created successfully!")
            
            # Verify
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"\nCreated {len(tables)} tables:")
            for table in sorted(tables):
                print(f"  - {table}")
            
            return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import sys
    success = drop_and_recreate()
    sys.exit(0 if success else 1)
