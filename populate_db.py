from app import create_app, db
from app.models import User, Contact
import random
import string

app = create_app()

with app.app_context():
    db.create_all()

    for _ in range(10):
        user = User(
            name="".join(random.choices(string.ascii_uppercase, k=5)),
            phone_number="".join(random.choices(string.digits, k=10)),
            email="".join(random.choices(string.ascii_lowercase, k=5)) + "@example.com",
        )
        user.set_password("password")
        db.session.add(user)

        for _ in range(5):
            contact = Contact(
                name="".join(random.choices(string.ascii_uppercase, k=5)),
                phone_number="".join(random.choices(string.digits, k=10)),
                owner=user,
            )
            db.session.add(contact)

    db.session.commit()
