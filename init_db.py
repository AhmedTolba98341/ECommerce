#!/usr/bin/env python
# init_db.py - Initialize Database Tables

import os
import sys

# Disable Flask debug mode before importing
os.environ['FLASK_ENV'] = 'production'

from app import create_app, db

def init_database():
    """Create all database tables from models."""
    app = create_app()
    app.config['DEBUG'] = False
    
    with app.app_context():
        print("Creating database tables...")
        try:
            db.create_all()
            print("✓ Database tables created successfully!")
            return True
        except Exception as e:
            print(f"✗ Error creating tables: {e}")
            return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
