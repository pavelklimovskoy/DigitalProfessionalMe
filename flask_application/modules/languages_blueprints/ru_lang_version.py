# -*- coding: utf-8 -*-


from flask import Blueprint, render_template, abort, session
from flask_login import login_required, logout_user
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from ..json_convert import json_convert, color_calc, timeline_parse
from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for, flash, session, send_file
from flask_cors import CORS
from flask import send_from_directory
from jinja2 import TemplateNotFound
from ..mongodb import *


ru_version = Blueprint('ru_version', __name__, template_folder='templates')


# Новая страница логинки
@ru_version.route('/ru/auth')
def auth_ru():
    return render_template('/ru/auth_ru.html', title='Digital Professional Me')

# Основная страница
@ru_version.route('/ru/')
@login_required
def index_ru():
    if session is None:
        logout_user()
        return redirect(".auth_ru")
    return render_template('/ru/index_ru.html', title='Digital Professional Me', userName=current_user.name)


# Авторизация
@ru_version.route('/ru/login', methods=['POST', 'GET'])
def login_ru():
    if current_user.is_authenticated:
        return redirect(url_for('.index_ru'))

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        checkbox = True if request.form.get('check') else False

        user = find_record('email', email)
        if user:
            print(f'User is found. Email={email}.')
            hashed_password = user.password
            if password == hashed_password:
                print(f'User password is accepted. Email={email}.')
                # checkbox = True if json_data["check"] else False
                session["logged_in"] = True
                login_user(user, remember=checkbox)
                return redirect(url_for(".index_ru"))
            else:
                print(f'User password is rejected. Email={email}.')
                return redirect(url_for(".auth_ru"))
        else:
            print(f'User is not found. Email={email}.')
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