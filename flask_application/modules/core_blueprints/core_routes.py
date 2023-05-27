# -*- coding: utf-8 -*-

"""
    Фйал с роутами общими для всех языков

"""

from flask import Blueprint, render_template, abort, session
from flask_login import login_required, logout_user
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from ..json_convert import json_convert, color_calc, timeline_parse
from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for, flash, session, send_file
from flask_cors import CORS
from flask import send_from_directory
from jinja2 import TemplateNotFound
from ..mongodb import *
import os


core_route = Blueprint('core_routes', __name__, template_folder='templates')

@core_route.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(core_route.root_path, 'static/image'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@core_route.app_errorhandler(404)
def page_not_found(error):
    """
    Обработка кода ошибки 404
    :param error:
    :return:
    """
    if "ru" in request.accept_languages:
        return render_template('/ru/notfound_ru.html')
    else:
        return render_template('/en/401_en.html')


@core_route.app_errorhandler(401)
def unauthorized_error(error):
    """
    Обработка кода ошибки 401
    :param error:
    :return:
    """
    if "ru" in request.accept_languages:
        return render_template('/ru/notfound_ru.html')
    else:
        return render_template('/en/401_en.html')