from app import app, db, create_default_admin, create_default_organizations, db_path

with app.app_context():
    db.create_all()
    create_default_admin()
    created_organizations = create_default_organizations()
    print(f"Database ready at: {db_path}")
    if created_organizations:
        names = ', '.join(org['name'] for org in created_organizations)
        print(f"Default organizations created: {names}")
