from flask import Blueprint, render_template
from routes.role_required import role_required

patient_bp = Blueprint('patient_bp', __name__, url_prefix='/patient')


@patient_bp.route('/home')
@role_required('patient')
def patient_home():
  return render_template('patient/home.html')
