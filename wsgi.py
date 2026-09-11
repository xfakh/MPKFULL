from app import app, db, create_default_admin, db_path

with app.app_context():
    db.create_all()
    create_default_admin()
    print(f"Database ready at: {db_path}")
