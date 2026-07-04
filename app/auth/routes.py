from flask import Blueprint, render_template, request, redirect, url_for, flash

from services.auth_service import register_user, authenticate_user

auth = Blueprint("auth", __name__)


@auth.route("/")
def home():
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        user, error = register_user(username, email, password)

        if error:
            flash(error, "danger")
            return redirect(url_for("auth.register"))

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = authenticate_user(username, password)

        if not user:
            flash("Invalid username or password.", "danger")
            return redirect(url_for("auth.login"))

        return redirect(url_for("auth.dashboard"))

    return render_template("login.html")


@auth.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")