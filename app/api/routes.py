from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from models.user_session import UserSession
from models.security_event import SecurityEvent

from services.typing_service import save_typing_event
from services.feature_extraction_service import extract_features_for_session
from services.profile_service import (
    enroll_user,
    get_behavior_profile
)
from services.trust_engine import evaluate_session

api = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


@api.route("/typing", methods=["POST"])
@login_required
def typing_event():

    data = request.get_json()

    required_fields = [
        "field_name",
        "key_pressed",
        "sequence_number",
        "key_down_timestamp",
        "key_up_timestamp",
        "dwell_time"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "message": f"Missing field: {field}"
            }), 400

    success, result = save_typing_event(
        current_user,
        data
    )

    if not success:
        return jsonify({
            "success": False,
            "message": result
        }), 400

    return jsonify({
        "success": True,
        "message": "Typing event saved successfully."
    })


@api.route("/features", methods=["GET"])
@login_required
def behavioral_features():

    session = (
        UserSession.query
        .filter_by(
            user_id=current_user.id,
            status="ACTIVE"
        )
        .order_by(UserSession.login_time.desc())
        .first()
    )

    if not session:
        return jsonify({
            "success": False,
            "message": "No active session found."
        }), 404

    features = extract_features_for_session(session.id)

    return jsonify({
        "success": True,
        "features": features
    })


@api.route("/security-events", methods=["GET"])
@login_required
def security_events():

    events = (
        SecurityEvent.query
        .filter_by(user_id=current_user.id)
        .order_by(SecurityEvent.created_at.desc())
        .all()
    )

    data = []

    for event in events:
        data.append({
            "event_type": event.event_type,
            "severity": event.severity,
            "risk_score": event.risk_score,
            "action_taken": event.action_taken,
            "details": event.details,
            "created_at": event.created_at.strftime("%d %b %Y %H:%M")
        })

    return jsonify({
        "success": True,
        "events": data
    })


@api.route("/profile", methods=["GET"])
@login_required
def behavior_profile():

    session = (
        UserSession.query
        .filter_by(
            user_id=current_user.id,
            status="ACTIVE"
        )
        .order_by(UserSession.login_time.desc())
        .first()
    )

    if not session:
        return jsonify({
            "success": False,
            "message": "No active session found."
        }), 404

    profile = get_behavior_profile(current_user.id)

    if profile is None:

        profile = enroll_user(
            current_user.id,
            session.id
        )

        if profile is None:
            return jsonify({
                "success": False,
                "message": "User is still enrolling. More typing data required."
            }), 400

    return jsonify({
        "success": True,
        "profile": {
            "is_enrolled": profile.is_enrolled,
            "avg_dwell_time": profile.avg_dwell_time,
            "avg_flight_time": profile.avg_flight_time,
            "dwell_variance": profile.dwell_variance,
            "flight_variance": profile.flight_variance,
            "typing_speed": profile.typing_speed,
            "total_keys": profile.total_keys
        }
    })


@api.route("/trust", methods=["GET"])
@login_required
def trust_score():

    session = (
        UserSession.query
        .filter_by(
            user_id=current_user.id,
            status="ACTIVE"
        )
        .order_by(UserSession.login_time.desc())
        .first()
    )

    if not session:
        return jsonify({
            "success": False,
            "message": "No active session found."
        }), 404

    result = evaluate_session(
        current_user.id,
        session.id
    )

    if result is None:
        return jsonify({
            "success": False,
            "message": "Unable to evaluate trust."
        }), 400

    return jsonify({
        "success": True,
        "enrolled": result["enrolled"],
        "similarity": result["similarity"],
        "trust_score": result["trust_score"],
        "risk_level": result["risk_level"],
        "keys_collected": result.get("keys_collected"),
        "keys_required": result.get("keys_required")
    })