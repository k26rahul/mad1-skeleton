from werkzeug.security import generate_password_hash
from datetime import date, time, timedelta
from models import db, User, Admin, Doctor, Patient, Department, Appointment, SlotReservation, Treatment


# ==========================================================
#   Helper Functions
# ==========================================================

def add_department(name, desc):
  dept = Department(name=name, description=desc)
  db.session.add(dept)
  return dept


def add_doctor(name, dept):
  doctor = Doctor(
      user=User(
          email=f"{name.lower().replace(' ', '')}@example.com",
          password=generate_password_hash("12345"),
          name=name,
          type="doctor"
      ),
      department=dept
  )
  db.session.add(doctor)
  return doctor


def add_patient(name, dob):
  patient = Patient(
      dob=dob,
      user=User(
          email=f"{name.lower().replace(' ', '')}@example.com",
          password=generate_password_hash("12345"),
          name=name,
          type="patient"
      )
  )
  db.session.add(patient)
  return patient


def add_slot(doctor, slot_date, slot_time, slot_type):
  slot = SlotReservation(
      doctor=doctor,
      date=slot_date,
      start_time=slot_time,
      type=slot_type
  )
  db.session.add(slot)
  return slot


def add_appointment(patient, doctor, slot, status, treatment_data=None):
  appt = Appointment(
      patient=patient,
      doctor=doctor,
      slot=slot,
      status=status
  )
  db.session.add(appt)

  if treatment_data:
    treat = Treatment(
        appointment=appt,
        diagnosis=treatment_data.get("diagnosis"),
        prescription=treatment_data.get("prescription"),
        tests=treatment_data.get("tests"),
        notes=treatment_data.get("notes")
    )
    db.session.add(treat)

  return appt


# ==========================================================
#   Main Populate Function
# ==========================================================

def populate():

  # Departments
  dept_names = ["Cardiology", "Neurology", "Orthopedics", "Dermatology", "Pediatrics"]
  departments = [add_department(name, f"{name} related treatments") for name in dept_names]
  db.session.commit()

  # Admin User
  admin = Admin(user=User(
      email='admin@example.com',
      password=generate_password_hash('12345'),
      name='Admin One',
      type='admin'
  ))
  db.session.add(admin)

  # 5 Doctors
  doctor_specs = [
      ("Dr. Arjun Mehta", 0),
      ("Dr. Kavita Rao", 1),
      ("Dr. Sameer Nair", 2),
      ("Dr. Priya Sharma", 3),
      ("Dr. Rohan Kulkarni", 4)
  ]

  doctors = [
      add_doctor(name, departments[dept_index])
      for name, dept_index in doctor_specs
  ]
  db.session.commit()

  # 5 Patients
  patient_info = [
      ("Riya Singh", date(1999, 5, 15)),
      ("Aman Verma", date(2001, 8, 10)),
      ("Meera Joshi", date(1997, 2, 20)),
      ("Suresh Kumar", date(1990, 7, 9)),
      ("Alaya Kapoor", date(2003, 11, 30))
  ]

  patients = [add_patient(name, dob) for name, dob in patient_info]
  db.session.commit()

  # Appointments List
  appointments_data = []

  # First patient - 5 appts with doctor 1
  for i in range(4):
    appointments_data.append({
        "patient": patients[0],
        "doctor": doctors[0],
        "date": date.today() - timedelta(days=(i + 1) * 5),
        "time": time(10, 0),
        "status": "completed",
        "treatment": {
            "diagnosis": "Routine checkup",
            "prescription": "General meds",
            "tests": "Blood test",
            "notes": "All good"
        }
    })

  appointments_data.append({
      "patient": patients[0],
      "doctor": doctors[0],
      "date": date.today() + timedelta(days=3),
      "time": time(11, 0),
      "status": "scheduled",
      "treatment": None
  })

  # Second patient - 3 appts with doctor 2
  for i in range(2):
    appointments_data.append({
        "patient": patients[1],
        "doctor": doctors[1],
        "date": date.today() - timedelta(days=(i + 1) * 4),
        "time": time(14, 0),
        "status": "completed",
        "treatment": {
            "diagnosis": "Mild headache",
            "prescription": "Painkillers",
            "tests": "None",
            "notes": "Recovered"
        }
    })

  appointments_data.append({
      "patient": patients[1],
      "doctor": doctors[1],
      "date": date.today() + timedelta(days=2),
      "time": time(15, 0),
      "status": "scheduled",
      "treatment": None
  })

  # Create Slots + Appointments
  for appt in appointments_data:
    slot = add_slot(
        doctor=appt["doctor"],
        slot_date=appt["date"],
        slot_time=appt["time"],
        slot_type="booked"
    )

    add_appointment(
        patient=appt["patient"],
        doctor=appt["doctor"],
        slot=slot,
        status=appt["status"],
        treatment_data=appt["treatment"]
    )

  db.session.commit()
