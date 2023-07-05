# -*- coding: utf-8 -*-

"""
    Фйал с роутаами для работы с API Rchilli

"""


import os

from flask import (
    Blueprint,
    Flask,
    abort,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    session,
    url_for,
)
from flask_cors import CORS
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from jinja2 import TemplateNotFound

rchilli_routes = Blueprint("rchilli_routes", __name__, template_folder="templates")


@rchilli_routes.route("/getRchilliJson", methods=["GET", "POST"])
@login_required
def get_rchilli_json():
    """
     Получение Json от API Rchilli
    :return:
    """
    return jsonify(current_user.rchilli_data)


@rchilli_routes.route("/getRchilliSkills", methods=["GET", "POST"])
@login_required
def get_rchilli_skills():
    """
    Get Skills from Rchilli Json
    :return:
    """
    try:
        return jsonify(current_user.rchilli_data["ResumeParserData"]["SegregatedSkill"])
    except Exception as e:
        print(e)
        return "404"
