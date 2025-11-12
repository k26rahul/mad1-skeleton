from functools import wraps
from flask import redirect, url_for
from flask_login import current_user


def role_required(role):
  def wrapper(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      if not current_user.is_authenticated or current_user.type != role:
        return redirect(url_for('auth_bp.login'))
      return f(*args, **kwargs)
    return decorated_function
  return wrapper
