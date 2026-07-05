from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from models.user_session import UserSession
from services.typing_service import save_typing_event
from services.feature_extraction_service import extract_features_for_session

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