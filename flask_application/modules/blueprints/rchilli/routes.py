# -*- coding: utf-8 -*-

"""
    Фйал с роутаами для работы с API Rchilli

"""

from flask import Blueprint, render_template, abort, session
from flask_login import login_required, logout_user
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for, flash, session, send_file
from flask_cors import CORS
from flask import send_from_directory
from jinja2 import TemplateNotFound
import os

rchilli_routes = Blueprint('rchilli_routes', __name__, template_folder='templates')


@rchilli_routes.route('/getRchilliJson', methods=['GET', 'POST'])
@login_required
def get_rchilli_json():
    """
     Получение Json от API Rchilli
    :return:
    """
    return jsonify(current_user.rchilli_data)


@rchilli_routes.route('/getRchilliSkills', methods=['GET', 'POST'])
@login_required
def get_rchilli_skills():
    """
    Get Skills from Rchilli Json
    :return:
    """
    try:
        return jsonify(current_user.rchilli_data['ResumeParserData']['SegregatedSkill'])
    except Exception as e:
        print(e)
        return '404'
