# -*- coding: utf-8 -*-

"""
    Роуты для страниц на английском языке

"""


from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

en_version = Blueprint("en_version", __name__, template_folder="templates")


# Новая страница логинки
@en_version.route("/en/auth")
def auth_en():
    return render_template("/en/auth_en.html", title="Digital Professional Me")


# Основная страница
# @app.route('/me')
@en_version.route("/en/")
@login_required
def index_en():
    if session is None:
        logout_user()
        return redirect(url_for(".auth_en"))
    return render_template(
        "/en/index_en.html", title="Digital Professional Me", userName=current_user.name
    )


# About page
@en_version.route("/en/about", methods=["POST", "GET"])
def about_us_en():
    return render_template("/en/aboutus_en.html", title="About us")


@en_version.route("/en/register", methods=["GET", "POST"])
def register_en():
    """
    Registration
    :return:
    """
    from ...db_connector import DatabaseConnector

    if current_user.is_authenticated:
        return redirect(url_for(".index_en"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        user = DatabaseConnector.get_instance().find_record("email", email)

        if user:
            return redirect(url_for("auth_en"))
        else:
            if password2 == password:
                # hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
                hashed_password = password
                new_user = DatabaseConnector.get_instance().create_record(
                    name, email, hashed_password
                )
                login_user(new_user, remember=True)
                session["logged_in"] = True

                return redirect(url_for(".index_en"))
            else:
                return redirect(url_for(".auth_en"))
    else:
        return redirect(url_for(".auth_en"))


@en_version.route("/en/adminUni", methods=["GET", "POST"])
@login_required
def admin_uni_en():
    return render_template("/en/adminuni_en.html")


# Авторизация
@en_version.route("/en/login", methods=["POST", "GET"])
def login_en():
    from ...db_connector import DatabaseConnector

    if current_user.is_authenticated:
        return redirect(url_for(".index_en"))

    if request.method == "POST":
        # json_data = request.get_json()
        # email = json_data["email"]
        # password = json_data["password"]
        email = request.form.get("email")
        password = request.form.get("password")
        checkbox = True if request.form.get("check") else False

        user = DatabaseConnector.get_instance().find_record("email", email)
        if user:
            # print(f'User is found. Email={email}.')
            hashed_password = user.password
            if password == hashed_password:
                # print(f'User password is accepted. Email={email}.')
                # checkbox = True if json_data["check"] else False
                session["logged_in"] = True
                login_user(user, remember=checkbox)
                return redirect(url_for(".index_en"))
            else:
                # print(f'User password is rejected. Email={email}.')
                return redirect(url_for(".auth_en"))
        else:
            # print(f'User is not found. Email={email}.')
            return redirect(url_for(".auth_en"))
    else:
        return redirect(url_for(".auth_en"))


# Деавторизация
@en_version.route("/en/logout")
@login_required
def logout_en():
    logout_user()
    session["logged_in"] = False
    return redirect(url_for(".auth_en"))
