from flask import Blueprint

bp = Blueprint('errors', __name__, url_prefix="/error")

from app.errors import handlers

