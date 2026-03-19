from functools import wraps
from flask import redirect, url_for, flash, request, abort
from flask_login import current_user
import logging

# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_admin:
#             flash("You do not have permission to access this resource", category="error")
#             return redirect(url_for("views.user_base"))
#         return f(*args, **kwargs)
#     return decorated_function

# def regular_user_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if current_user.is_admin:
#             flash("You do not have permission to access this resource.", category="error")
#             return redirect(url_for("views.admin_base"))
#         return f(*args, **kwargs)
#     return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if not current_user.is_admin:
            logging.warning( "Unauthorised admin access attempt by user_id: {current_user.user_id} from IP: {request.remote_addr}")
            flash("You do not have permission to access this resource", category="error")
            return redirect(url_for("views.user_base"))
        return f(*args, **kwargs)
    return decorated_function

def regular_user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if current_user.is_admin:
            logging.warning("Admin user_id: {current_user.user_id} attempted to access a regular user route from IP: {request.remote_addr}")
            flash("You do not have permission to access this resource.", category="error")
            return redirect(url_for("views.admin_base"))
        return f(*args, **kwargs)
    return decorated_function

