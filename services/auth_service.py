from random import randint

from app.extensions import db, bcrypt
from models.user import User
from models.bank_account import BankAccount


def generate_account_number():
    return str(randint(100000000000, 999999999999))


def register_user(username, email, password):

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return None, "Username or email already exists."

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.flush()

    account = BankAccount(
        user_id=user.id,
        account_number=generate_account_number(),
        account_type="Savings",
        balance=100000.00,
        currency="INR"
    )

    db.session.add(account)
    db.session.commit()

    return user, None


def authenticate_user(username, password):

    user = User.query.filter_by(username=username).first()

    if not user:
        return None

    if bcrypt.check_password_hash(user.password_hash, password):
        return user

    return None