from flask import Flask

from app.config import Config

from app.extensions import db, login_manager, bcrypt

from models.behavior_profile import BehaviorProfile

from datetime import timezone

from zoneinfo import ZoneInfo

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    @app.template_filter("localtime")

    def localtime_filter(dt):

        """

        Convert UTC datetime stored in the database to IST for display.

        """

        if dt is None:

            return ""

        if dt.tzinfo is None:

            dt = dt.replace(tzinfo=timezone.utc)

        return (

            dt.astimezone(ZoneInfo("Asia/Kolkata"))

            .strftime("%d %b %Y, %I:%M %p")

        )

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

    from app.api import api

    app.register_blueprint(auth)

    app.register_blueprint(main)

    app.register_blueprint(transfer)

    app.register_blueprint(api)

    return app