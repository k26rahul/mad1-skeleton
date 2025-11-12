from flask import Blueprint, render_template
from routes.role_required import role_required

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


@admin_bp.route('/home')
@role_required('admin')
def admin_home():
  return render_template('admin/home.html')
