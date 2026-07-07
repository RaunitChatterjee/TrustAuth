from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user,
    logout_user
)

from services.transfer_service import (
    transfer_money,
    execute_transfer
)

from services.otp_service import (
    verify_transfer_otp,
    consume_verified_transfer,
    resend_transfer_otp,
    cancel_pending_transfer,
)

transfer = Blueprint(
    "transfer",
    __name__
)


@transfer.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer_page():

    if request.method == "POST":

        beneficiary = request.form.get("beneficiary")
        amount = request.form.get("amount")
        note = request.form.get("note")

        try:
            amount = float(amount)
        except (ValueError, TypeError):
            flash("Invalid transfer amount.", "danger")
            return redirect(
                url_for("transfer.transfer_page")
            )

        success, message = transfer_money(
            current_user,
            beneficiary,
            amount,
            note
        )

        if success:
            flash(message, "success")
            return redirect(
                url_for("main.dashboard")
            )

        if message == "SESSION_TERMINATED":

            logout_user()

            flash(
                "Your session has been terminated because suspicious activity was detected.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        if message == "OTP_REQUIRED":
            return redirect(
                url_for("transfer.verify_transfer")
            )

        flash(message, "danger")

        return redirect(
            url_for("transfer.transfer_page")
        )

    return render_template("transfer.html")


@transfer.route("/transfer/verify", methods=["GET", "POST"])
@login_required
def verify_transfer():

    if request.method == "POST":

        otp = request.form.get("otp")

        success, message, pending = verify_transfer_otp(
            current_user.id,
            otp
        )

        if not success:

            flash(message, "danger")

            return redirect(
                url_for("transfer.verify_transfer")
            )

        pending = consume_verified_transfer(
            current_user.id
        )

        if pending is None:

            flash(
                "No pending transfer found.",
                "danger"
            )

            return redirect(
                url_for("main.dashboard")
            )

        success, message = execute_transfer(
            current_user,
            pending.beneficiary,
            pending.amount,
            pending.note
        )

        flash(
            message,
            "success" if success else "danger"
        )

        return redirect(
            url_for("main.dashboard")
        )

    return render_template(
        "verify_transfer_otp.html"
    )


# ----------------------------------------------------
# RESEND OTP
# ----------------------------------------------------

@transfer.route("/transfer/resend", methods=["POST"])
@login_required
def resend_transfer():

    success, message = resend_transfer_otp(
        current_user.id
    )

    flash(
        message,
        "success" if success else "danger"
    )

    return redirect(
        url_for("transfer.verify_transfer")
    )


# ----------------------------------------------------
# CANCEL TRANSFER
# ----------------------------------------------------

@transfer.route("/transfer/cancel", methods=["POST"])
@login_required
def cancel_transfer():

    cancel_pending_transfer(
        current_user.id
    )

    flash(
        "Transfer cancelled.",
        "info"
    )

    return redirect(
        url_for("main.dashboard")
    )