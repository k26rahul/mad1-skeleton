from flask import Blueprint, render_template
from routes.role_required import role_required

doctor_bp = Blueprint('doctor_bp', __name__, url_prefix='/doctor')


@doctor_bp.route('/home')
@role_required('doctor')
def doctor_home():
  return render_template('doctor/home.html')
