from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user
from models import User

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
      login_user(user)
      if user.type == 'admin':
        return redirect(url_for('admin_bp.admin_home'))
      elif user.type == 'doctor':
        return redirect(url_for('doctor_bp.doctor_home'))
      elif user.type == 'patient':
        return redirect(url_for('patient_bp.patient_home'))
    else:
      error = "Invalid email or password."

  return render_template('login.html', error=error)


@auth_bp.route('/register_doctor')
def register_doctor():
  return render_template('register_doctor.html')


@auth_bp.route('/register_patient')
def register_patient():
  return render_template('register_patient.html')
