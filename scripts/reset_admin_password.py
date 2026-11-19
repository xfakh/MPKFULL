#!/usr/bin/env python3
"""
Reset password akun admin.

Gunakan dari root project:
    python scripts/reset_admin_password.py
    python scripts/reset_admin_password.py admin
    python scripts/reset_admin_password.py admin "password-baru"
"""

import getpass
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Admin
from werkzeug.security import generate_password_hash


def reset_admin_password(username, new_password):
    with app.app_context():
        db.create_all()

        admin = Admin.query.filter_by(username=username).first()
        if not admin:
            print(f"❌ Akun admin '{username}' tidak ditemukan.")
            return False

        admin.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()
        print(f"✅ Password akun '{username}' berhasil direset.")
        return True


def main():
    username = sys.argv[1] if len(sys.argv) > 1 else 'admin'

    if len(sys.argv) > 2:
        new_password = sys.argv[2]
    else:
        new_password = getpass.getpass(f"Password baru untuk '{username}': ")
        confirmation = getpass.getpass("Ulangi password baru: ")
        if new_password != confirmation:
            print("❌ Password tidak sama.")
            return 1

    if not new_password:
        print("❌ Password tidak boleh kosong.")
        return 1

    return 0 if reset_admin_password(username, new_password) else 1


if __name__ == '__main__':
    sys.exit(main())
