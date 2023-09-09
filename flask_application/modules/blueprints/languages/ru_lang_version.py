# -*- coding: utf-8 -*-

"""
    Роуты для страниц на русском языке
"""

from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user

ru_version = Blueprint('ru_version', __name__, template_folder='templates')


@ru_version.route('/ru/auth')
def auth_ru():
    """
    # Новая страница логинки
    :return:
    """
    return render_template('/ru/auth_ru.html', title='Digital Professional Me')


# Основная страница
@ru_version.route('/ru/')
@login_required
def index_ru():
    if session is None:
        logout_user()
        return redirect(".auth_ru")
    return render_template('/ru/index_ru.html', title='Digital Professional Me', userName=current_user.name)


@ru_version.route('/ru/login', methods=['POST', 'GET'])
def login_ru():
    """
    # Авторизация
    :return:
    """
    from ...db_connector import DatabaseConnector

    if current_user.is_authenticated:
        return redirect(url_for('.index_ru'))

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        checkbox = True if request.form.get('check') else False

        user = DatabaseConnector.get_instance().find_record('email', email)
        if user:
            # print(f'User is found. Email={email}.')
            hashed_password = user.password
            if password == hashed_password:
                # print(f'User password is accepted. Email={email}.')
                # checkbox = True if json_data["check"] else False
                session["logged_in"] = True
                login_user(user, remember=checkbox)
                return redirect(url_for(".index_ru"))
            else:
                # print(f'User password is rejected. Email={email}.')
                return redirect(url_for(".auth_ru"))
        else:
            # print(f'User is not found. Email={email}.')
            return redirect(url_for(".auth_ru"))
    else:
        return redirect(url_for(".auth_ru"))


# Деавторизация
@ru_version.route('/ru/logout')
@login_required
def logout_ru():
    logout_user()
    session["logged_in"] = False
    return redirect(url_for(".auth_ru"))


@ru_version.route('/ru/adminUni', methods=['GET', 'POST'])
@login_required
def admin_uni_ru():
    return render_template('/ru/adminuni_ru.html')


# About page
@ru_version.route('/ru/about', methods=['POST', 'GET'])
def about_us_ru():
    return render_template('/ru/aboutus_ru.html', title='About us')
