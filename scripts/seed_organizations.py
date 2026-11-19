#!/usr/bin/env python3
"""
Script untuk menambahkan organisasi awal ke database.

Gunakan dari root project: python scripts/seed_organizations.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import (
    app,
    db,
    Organization,
    DEFAULT_ORGANIZATIONS,
    create_default_organizations,
)


def seed_organizations():
    """Menambahkan organisasi default yang belum terdaftar ke database."""

    with app.app_context():
        db.create_all()
        print("🚀 Memulai seeding organisasi...\n")

        created = create_default_organizations(force=True)
        created_usernames = {org['username'] for org in created}

        for data in DEFAULT_ORGANIZATIONS:
            if data['username'] in created_usernames:
                print(f"✅ Organisasi '{data['name']}' berhasil dibuat")
                print(f"   Username: {data['username']}")
                print(f"   Password: {data['password']}")
            else:
                print(f"⚠️  Organisasi '{data['name']}' sudah ada, skip...")
            print()

        print("✨ Seeding selesai!\n")

        total_orgs = Organization.query.count()
        print(f"📊 Total organisasi di database: {total_orgs}")
        print("\n" + "=" * 50)
        print("KREDENSIAL LOGIN ORGANISASI")
        print("=" * 50)

        default_by_username = {data['username']: data for data in DEFAULT_ORGANIZATIONS}
        for org in Organization.query.order_by(Organization.id).all():
            print(f"\n🏢 {org.name}")
            print("   URL: http://127.0.0.1:5000/login")
            print(f"   Username: {org.username}")
            if org.username in default_by_username:
                print(f"   Password: {default_by_username[org.username]['password']}")
            else:
                print("   Password: diatur saat pembuatan akun")


if __name__ == '__main__':
    seed_organizations()
