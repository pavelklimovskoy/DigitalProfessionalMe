# -*- coding: utf-8 -*-

"""
    Фйал с роутами общими для всех языков

"""

import os

from flask import (Blueprint, current_app, redirect, render_template, request,
                   send_from_directory, session, url_for)
from flask_login import current_user, login_required, logout_user
from werkzeug.utils import secure_filename

core_route = Blueprint('core_routes', __name__, template_folder='templates')


@core_route.route('/favicon.ico')
def favicon():
    """
    Возврат фавикона
    :return:
    """
    return send_from_directory(os.path.join(core_route.root_path, 'static/image'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@core_route.route('/detect_lang')
def select_language():
    """
    Выбора языка страницы для выдачи пользователю
    :return:
    """
    if "ru" in request.accept_languages:
        return redirect(url_for('ru_version.auth_ru'))
    else:
        return redirect(url_for('en_version.auth_en'))


# @core_route.app_errorhandler(404)
# def page_not_found(error):
#     """
#     Обработка кода ошибки 404
#     :param error:
#     :return:
#     """
#     if "ru" in request.accept_languages:
#         return render_template('/ru/401_ru.html')
#     else:
#         return render_template('/en/notfound_en.html')
#

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


@core_route.route('/upload_avatar', methods=['GET', 'POST'])
@login_required
def upload_avatar():
    from ...analytics import Analytics
    from ...db_connector import DatabaseConnector
    """
    Загрузка аватара на сервер
    :return:
    """
    avatar = request.files['avatar']
    avatar_name = avatar.filename
    image_id = Analytics().summary_image_count()

    if request.method == 'POST':
        if avatar is not None:
            if avatar_name[-3:] in ['jpg', 'png']:
                file_name = f'{avatar_name[:-4]}-id-{image_id}.{avatar_name[-3:]}'

                avatar.save(os.path.join(current_app.config['UPLOAD_IMAGE_FOLDER'], file_name))

                Analytics.get_instance().increment_image_count()
                DatabaseConnector.get_instance().update_record('id', current_user.id, 'avatar', file_name)

    return redirect(url_for('ru_version.index_ru'))


@core_route.route('/getAvatar', methods=['GET', 'POST'])
@login_required
def get_avatar():
    """
    Получение аватара пользователя
    :return:
    """
    return current_user.avatar


@core_route.route('/')
@login_required
def index():
    """
    Основная страница
    :return:
    """
    if session is None:
        logout_user()
        return redirect(url_for('select_language'))

    return render_template('/ru/index_ru.html', title='Digital Professional Me', userName=current_user.name)


@core_route.route('/uploader', methods=['GET', 'POST'])
@login_required
def upload_file():
    from ...analytics import Analytics
    from ...db_connector import DatabaseConnector
    from ...rchilli import RchilliConnector
    from ...service import ServiceContainer
    """
    Uploading CV in storage
    :return:
    """
    if request.method == 'POST':
        try:
            cv_link = request.form['link']
            file_name = ''
            if cv_link != '':
                try:
                    file_name = f'hhCv_{Analytics.get_instance().summary_cv_count()}.pdf'
                    ServiceContainer.get_instance().save_pdf(cv_link, file_name)

                    Analytics.get_instance().increment_cv_count()
                except Exception as e:
                    print(e)
            else:
                file = request.files['file']
                file_name = secure_filename(file.filename)

                # Локально сохраняем копию CV
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file_name))

                Analytics.get_instance().increment_cv_count()

            cur_user = DatabaseConnector.get_instance().find_record('id', current_user.id)

            if cur_user is not None:
                
                rchilli_data = RchilliConnector.get_instance().rchilli_parse(file_name)
                json_data, skills_array = ServiceContainer.get_instance().json_convert(rchilli_data)
                timeline_events = ServiceContainer.get_instance().timeline_parse(rchilli_data)

                DatabaseConnector.get_instance().update_record('id', current_user.id, 'language',
                                                               rchilli_data['ResumeParserData']['ResumeLanguage'][
                                                                   'LanguageCode'])
                DatabaseConnector.get_instance().update_record('id', current_user.id, 'jsondata', json_data)
                DatabaseConnector.get_instance().update_record('id', current_user.id, 'rchillidata', rchilli_data)
                DatabaseConnector.get_instance().update_record('id', current_user.id, 'timelineEvents', timeline_events)
                return '200'
        except Exception as e:
            print(e)

    return redirect(url_for('ru_version.index_ru'))


@core_route.route('/handleRecommendationClick', methods=['GET', 'POST'])
@login_required
def handle_recommendation_click():
    from ...db_connector import DatabaseConnector
    DatabaseConnector.get_instance().update_recommendation_clicks(current_user.id)
    return '200'
