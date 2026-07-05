from flask import Flask

from app.config import Config
from app.extensions import db, login_manager, bcrypt


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "auth.login"

    from models import (
        User,
        UserSession,
        TypingEvent,
        SecurityEvent,
        BankAccount,
        Transaction
    )

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth.routes import auth
    from app.main import main
    from app.transfer import transfer

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(transfer)

    return app