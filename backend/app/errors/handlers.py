from flask import render_template
from app import db
from app.errors import bp

@bp.app_errorhandler(404)
def not_found_page(error):
    return render_template('errors/404.html')

@bp.app_errorhandler(500)
def server_error_page(error):
    return '500'