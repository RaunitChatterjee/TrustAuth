from app.extensions import db, bcrypt
from models.user import User


def register_user(username, email, password):
    """
    Register a new user.
    """

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
    db.session.commit()

    return user, None


def authenticate_user(username, password):
    """
    Authenticate a user.
    """

    user = User.query.filter_by(username=username).first()

    if not user:
        return None

    if bcrypt.check_password_hash(user.password_hash, password):
        return user

    return None