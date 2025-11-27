from flask import Blueprint, render_template, request, redirect
from routes.role_required import role_required
from models import User, Doctor, Patient, Appointment, Department, db
from werkzeug.security import generate_password_hash
from datetime import date

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


# ==========================================================
#   Admin Home
# ==========================================================
@admin_bp.route('/home')
@role_required('admin')
def admin_home():
  doctors = Doctor.query.all()
  patients = Patient.query.all()

  # Only upcoming scheduled appointments
  appointments = Appointment.query.filter(
      Appointment.date >= date.today(),
      Appointment.status == 'scheduled'
  ).all()

  return render_template(
      'admin/home.html',
      doctors=doctors,
      patients=patients,
      appointments=appointments
  )


# ==========================================================
#   Doctor: Delete / Block / Unblock
# ==========================================================
@admin_bp.route('/doctor/<int:id>/delete')
@role_required('admin')
def delete_doctor(id):
  doctor = Doctor.query.get_or_404(id)
  db.session.delete(doctor)
  db.session.delete(doctor.user)
  db.session.commit()
  return redirect('/admin/home')


@admin_bp.route('/doctor/<int:id>/block')
@role_required('admin')
def block_doctor(id):
  doctor = Doctor.query.get_or_404(id)
  doctor.user.is_blocked = True
  db.session.commit()
  return redirect('/admin/home')


@admin_bp.route('/doctor/<int:id>/unblock')
@role_required('admin')
def unblock_doctor(id):
  doctor = Doctor.query.get_or_404(id)
  doctor.user.is_blocked = False
  db.session.commit()
  return redirect('/admin/home')


# ==========================================================
#   Patient: Delete / Block / Unblock
# ==========================================================
@admin_bp.route('/patient/<int:id>/delete')
@role_required('admin')
def delete_patient(id):
  patient = Patient.query.get_or_404(id)
  db.session.delete(patient)
  db.session.delete(patient.user)
  db.session.commit()
  return redirect('/admin/home')


@admin_bp.route('/patient/<int:id>/block')
@role_required('admin')
def block_patient(id):
  patient = Patient.query.get_or_404(id)
  patient.user.is_blocked = True
  db.session.commit()
  return redirect('/admin/home')


@admin_bp.route('/patient/<int:id>/unblock')
@role_required('admin')
def unblock_patient(id):
  patient = Patient.query.get_or_404(id)
  patient.user.is_blocked = False
  db.session.commit()
  return redirect('/admin/home')


# ==========================================================
#   Create Doctor (GET + POST)
# ==========================================================
@admin_bp.route('/doctor/create', methods=['GET', 'POST'])
@role_required('admin')
def create_doctor():
  departments = Department.query.all()

  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    dept_id = request.form['dept_id']

    user = User(
        name=name,
        email=email,
        password=generate_password_hash(password),
        type='doctor'
    )
    db.session.add(user)
    db.session.commit()

    doctor = Doctor(
        user_id=user.id,
        dept_id=dept_id
    )
    db.session.add(doctor)
    db.session.commit()

    return redirect('/admin/home')

  return render_template('admin/create_doctor.html', departments=departments)


# ==========================================================
#   Edit Doctor (GET + POST)
# ==========================================================
@admin_bp.route('/doctor/<int:id>/edit', methods=['GET', 'POST'])
@role_required('admin')
def edit_doctor(id):
  doctor = Doctor.query.get_or_404(id)
  departments = Department.query.all()

  if request.method == 'POST':
    doctor.user.name = request.form['name']
    doctor.user.email = request.form['email']
    doctor.dept_id = request.form['dept_id']
    db.session.commit()
    return redirect('/admin/home')

  return render_template('admin/edit_doctor.html', doctor=doctor, departments=departments)


# ==========================================================
#   Appointment History
# ==========================================================
@admin_bp.route('/appointment/<int:id>/history')
@role_required('admin')
def appointment_history(id):
  appt = Appointment.query.get_or_404(id)
  patient = appt.patient

  past_appointments = Appointment.query.filter_by(patient_id=patient.id).all()

  return render_template(
      'admin/appointment_history.html',
      patient=patient,
      appointments=past_appointments
  )
