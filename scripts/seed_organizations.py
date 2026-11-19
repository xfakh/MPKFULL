#!/usr/bin/env python3
"""
Script untuk menambahkan organisasi contoh ke database
Gunakan dari root project: python scripts/seed_organizations.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Organization
from werkzeug.security import generate_password_hash

def seed_organizations():
    """Menambahkan organisasi contoh ke database"""
    
    organizations = [
        {
            'name': 'OSIM',
            'username': 'osim',
            'email': 'osim@masassalafiyyah.sch.id',
            'password': 'osim123'
        },
        {
            'name': 'GPS',
            'username': 'gps',
            'email': 'gps@masassalafiyyah.sch.id',
            'password': 'gps123'
        },
        {
            'name': 'Jurnalistik',
            'username': 'jurnalistik',
            'email': 'jurnalistik@masassalafiyyah.sch.id',
            'password': 'jurnalistik123'
        },
        {
            'name': 'ARSC',
            'username': 'arsc',
            'email': 'arsc@masassalafiyyah.sch.id',
            'password': 'arsc123'
        }
    ]
    
    with app.app_context():
        db.create_all()
        print("🚀 Memulai seeding organisasi...\n")
        
        for org_data in organizations:
            # Check if organization already exists
            existing = Organization.query.filter_by(username=org_data['username']).first()
            
            if existing:
                print(f"⚠️  Organisasi '{org_data['name']}' sudah ada, skip...")
                continue
            
            # Create new organization
            org = Organization(
                name=org_data['name'],
                username=org_data['username'],
                email=org_data['email'],
                password=generate_password_hash(org_data['password'], method='pbkdf2:sha256')
            )
            
            db.session.add(org)
            print(f"✅ Organisasi '{org_data['name']}' berhasil dibuat")
            print(f"   Username: {org_data['username']}")
            print(f"   Password: {org_data['password']}")
            print()
        
        db.session.commit()
        print("✨ Seeding selesai!\n")
        
        # Show summary
        total_orgs = Organization.query.count()
        print(f"📊 Total organisasi di database: {total_orgs}")
        print("\n" + "="*50)
        print("KREDENSIAL LOGIN ORGANISASI")
        print("="*50)
        
        all_orgs = Organization.query.all()
        for org in all_orgs:
            print(f"\n🏢 {org.name}")
            print(f"   URL: http://127.0.0.1:5000/org/login")
            print(f"   Username: {org.username}")
            # Password tidak ditampilkan karena sudah di-hash
            # User harus ingat password yang digunakan saat seeding

if __name__ == '__main__':
    seed_organizations()
