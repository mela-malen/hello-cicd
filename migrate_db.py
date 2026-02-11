#!/usr/bin/env python3
"""Database migration script to add newsletter columns to subscribers table."""
import os
import sys

def run_migration():
    """Run database migration."""
    from app import create_app
    from app.data.models import db
    from sqlalchemy import text

    app = create_app()
    with app.app_context():
        # Check if columns exist
        result = db.session.execute(text("""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'subscribers'
            ORDER BY ORDINAL_POSITION
        """))
        columns = [row[0] for row in result]
        
        print('Current columns in subscribers table:')
        for col in columns:
            print(f'  - {col}')
        
        # Add missing columns
        for col in ['nl_kost', 'nl_mindset', 'nl_kunskap', 'nl_veckans_pass', 'nl_jaine']:
            if col not in columns:
                print(f'Adding column: {col}...')
                try:
                    db.session.execute(text(f'ALTER TABLE subscribers ADD {col} BIT NOT NULL DEFAULT 0'))
                    db.session.commit()
                    print(f'  ✓ Added {col}')
                except Exception as e:
                    db.session.rollback()
                    print(f'  ✗ Failed to add {col}: {e}')
            else:
                print(f'  ✓ {col} already exists')
        
        print('\nMigration complete!')

if __name__ == "__main__":
    run_migration()
