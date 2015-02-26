import json

from flask import Blueprint, jsonify, request, abort, url_for
from flask.ext.login import login_user

from ..models import User
from ..extensions import login_manager, db


api = Blueprint("api", __name__)
