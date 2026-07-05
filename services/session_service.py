from datetime import datetime, timedelta

from app.extensions import db
from models.user_session import UserSession


SESSION_TIMEOUT_MINUTES = 10


def get_active_session(user_id):
    """
    Return the latest active session for a user.
    """

    return (
        UserSession.query
        .filter_by(
            user_id=user_id,
            status="ACTIVE"
        )
        .order_by(UserSession.login_time.desc())
        .first()
    )


def update_last_activity(session):
    """
    Update the last activity timestamp.
    The caller is responsible for committing.
    """

    session.last_activity = datetime.utcnow()


def end_session(session):
    """
    End a session.
    """

    session.status = "ENDED"
    session.logout_time = datetime.utcnow()

    db.session.commit()


def session_expired(session):
    """
    Check whether the session has timed out.
    """

    timeout = timedelta(
        minutes=SESSION_TIMEOUT_MINUTES
    )

    return (
        datetime.utcnow() -
        session.last_activity
    ) > timeout