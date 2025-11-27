from werkzeug.security import generate_password_hash
from datetime import date, time, timedelta
from models import *


def populate():

  # -------------------------
  #  Departments (5)
  # -------------------------
  dept_names = [
      "Cardiology",
      "Neurology",
      "Orthopedics",
      "Dermatology",
      "Pediatrics"
  ]

  departments = []
  for name in dept_names:
    d = Department(name=name, description=f"{name} related treatments")
    db.session.add(d)
    departments.append(d)

  db.session.commit()

  # -------------------------
  #  Admin
  # -------------------------
  admin_user = User(
      email='admin@example.com',
      password=generate_password_hash('12345'),
      name='Admin One',
      type='admin'
  )
  admin = Admin(user=admin_user)
  db.session.add(admin)

  # -------------------------
  #  Doctors (2 doctors, different departments)
  # -------------------------
  doctor1_user = User(
      email='doctor1@example.com',
      password=generate_password_hash('12345'),
      name='Dr. Arjun Mehta',
      type='doctor'
  )
  doctor1 = Doctor(
      user=doctor1_user,
      department=departments[0]   # Cardiology
  )
  db.session.add(doctor1)

  doctor2_user = User(
      email='doctor2@example.com',
      password=generate_password_hash('12345'),
      name='Dr. Kavita Rao',
      type='doctor'
  )
  doctor2 = Doctor(
      user=doctor2_user,
      department=departments[1]   # Neurology
  )
  db.session.add(doctor2)

  # -------------------------
  #  Patient (only one)
  # -------------------------
  patient1_user = User(
      email='patient1@example.com',
      password=generate_password_hash('12345'),
      name='Riya Singh',
      type='patient'
  )
  patient1 = Patient(
      dob=date(1999, 5, 15),
      user=patient1_user
  )
  db.session.add(patient1)

  db.session.commit()

  # -------------------------
  #  Appointments for Patient 1
  #  1 upcoming + 4 previous
  # -------------------------
  upcoming = Appointment(
      patient=patient1,
      doctor=doctor1,
      date=date.today() + timedelta(days=3),
      time=time(11, 0),
      status='scheduled'
  )

  past_list = []
  for i in range(1, 5):  # 4 previous appointments
    past = Appointment(
        patient=patient1,
        doctor=doctor1,
        date=date.today() - timedelta(days=i * 5),
        time=time(10, 0),
        status='completed'
    )
    past_list.append(past)

  db.session.add(upcoming)
  db.session.add_all(past_list)
  db.session.commit()

  # -------------------------
  #  Treatments for past appointments
  # -------------------------
  for appt in past_list:
    treat = Treatment(
        appointment=appt,
        diagnosis="Routine checkup",
        prescription="General medication",
        tests="Blood test",
        notes="No issues."
    )
    db.session.add(treat)

  db.session.commit()
