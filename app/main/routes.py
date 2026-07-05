from flask import Blueprint, render_template
from flask_login import login_required, current_user

from services.dashboard_service import get_dashboard_data

main = Blueprint("main", __name__)


@main.route("/dashboard")
@login_required
def dashboard():

    dashboard_data = get_dashboard_data(current_user)

    return render_template(
        "dashboard.html",
        account=dashboard_data["account"],
        transactions=dashboard_data["transactions"]
    )


@main.route("/security")
@login_required
def security():
    return render_template("security.html")


@main.route("/accounts")
@login_required
def accounts():
    return "<h1>Accounts Page (Coming Soon)</h1>"


@main.route("/transactions")
@login_required
def transactions():
    return "<h1>Transactions Page (Coming Soon)</h1>"