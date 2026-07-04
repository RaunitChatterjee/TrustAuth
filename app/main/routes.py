from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint("main", __name__)


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@main.route("/transfer")
@login_required
def transfer():
    return render_template("transfer.html")


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