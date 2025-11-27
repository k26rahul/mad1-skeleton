from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user
from models import User, Patient, db
from datetime import datetime

auth_bp = Blueprint('auth_bp', __name__)


# ==========================================================
#   Login (GET + POST)
# ==========================================================
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


# ==========================================================
#   Patient Registration (GET + POST)
# ==========================================================
@auth_bp.route('/register_patient', methods=['GET', 'POST'])
def register_patient():
  error = None

  if request.method == 'POST':
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    dob = request.form.get('dob')

    # check if email exists
    existing = User.query.filter_by(email=email).first()
    if existing:
      error = "Email already registered."
      return render_template('register_patient.html', error=error)

    # create user
    user = User(
        name=name,
        email=email,
        password=generate_password_hash(password),
        type='patient'
    )
    db.session.add(user)
    db.session.commit()

    # create patient record
    patient = Patient(
        user_id=user.id,
        dob=datetime.strptime(dob, "%Y-%m-%d").date()
    )
    db.session.add(patient)
    db.session.commit()

    # log in new patient
    login_user(user)
    return redirect(url_for('patient_bp.patient_home'))

  return render_template('register_patient.html')


# ==========================================================
#   Logout
# ==========================================================
@auth_bp.route('/logout')
def logout():
  logout_user()
  return redirect('/login')
