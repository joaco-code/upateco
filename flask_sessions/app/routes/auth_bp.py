from flask import Blueprint

from ..controllers.auth_controller import UserController

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/login', methods=['POST'])(UserController.login)
auth_bp.route('/profile', methods=['GET'])(UserController.show_profile)
auth_bp.route('/logout', methods=['GET'])(UserController.logout)