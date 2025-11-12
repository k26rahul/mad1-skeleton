from werkzeug.security import generate_password_hash
from datetime import date, time, timedelta
from models import *


def populate():
  # ======== Department ========
  dept = Department(name='Cardiology', description='Heart-related treatments')
  db.session.add(dept)
  db.session.commit()

  # ======== Admin ========
  admin_user = User(
      email='admin@example.com',
      password=generate_password_hash('12345'),
      type='admin'
  )
  admin = Admin(
      name='Admin One',
      phone_num='9999999999',
      user=admin_user
  )
  db.session.add(admin)

  # ======== Doctor ========
  doctor_user = User(
      email='doctor@example.com',
      password=generate_password_hash('12345'),
      type='doctor'
  )
  doctor = Doctor(
      name='Dr. Arjun Mehta',
      phone_num='8888888888',
      department=dept,
      user=doctor_user
  )
  db.session.add(doctor)

  # ======== Patient ========
  patient_user = User(
      email='patient@example.com',
      password=generate_password_hash('12345'),
      type='patient'
  )
  patient = Patient(
      name='Riya Singh',
      phone_num='7777777777',
      dob=date(1999, 5, 15),
      user=patient_user
  )
  db.session.add(patient)
  db.session.commit()

  # ======== Appointments ========
  # 1st Appointment — Future
  future_appt = Appointment(
      patient=patient,
      doctor=doctor,
      date=date.today() + timedelta(days=5),
      time=time(10, 30),
      status='scheduled'
  )

  # 2nd Appointment — Past (with treatment)
  past_appt = Appointment(
      patient=patient,
      doctor=doctor,
      date=date.today() - timedelta(days=10),
      time=time(15, 0),
      status='completed'
  )
  db.session.add_all([future_appt, past_appt])
  db.session.commit()

  # ======== Treatment (for past appointment) ========
  treatment = Treatment(
      appointment=past_appt,
      diagnosis='Mild chest pain',
      prescription='Medication A twice daily',
      notes='Follow-up required after 2 weeks',
      tests='ECG, Blood Pressure'
  )
  db.session.add(treatment)
  db.session.commit()
