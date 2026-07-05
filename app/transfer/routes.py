from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user

from services.transfer_service import transfer_money

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
            return redirect(url_for("transfer.transfer_page"))

        success, message = transfer_money(
            current_user,
            beneficiary,
            amount,
            note
        )

        if success:
            flash(message, "success")
            return redirect(url_for("main.dashboard"))

        flash(message, "danger")
        return redirect(url_for("transfer.transfer_page"))

    return render_template("transfer.html")