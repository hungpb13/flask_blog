from app import create_app, db
from werkzeug.security import generate_password_hash
from app.models import User

app = create_app()

def create_admin():
    if not User.query.filter_by(name="admin").first():
        admin = User(
            name="admin",
            email="admin@gmail.com",
            password=generate_password_hash("admin"),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created.")
    else:
        print("Admin already exists.")

with app.app_context():
    db.create_all()
    create_admin()

    

if __name__ == "__main__":
    app.run(debug=True)