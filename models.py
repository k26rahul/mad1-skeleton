from sqlalchemy import Column, Integer, String, Boolean, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# ================= User =================


class User(db.Model, UserMixin):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, autoincrement=True)
  email = Column(String, unique=True, nullable=False)
  password = Column(String, nullable=False)
  name = Column(String, nullable=False)
  type = Column(String)  # 'admin', 'doctor', 'patient'
  is_blocked = Column(Boolean, default=False)

  admin = relationship('Admin', back_populates='user', uselist=False)
  doctor = relationship('Doctor', back_populates='user', uselist=False)
  patient = relationship('Patient', back_populates='user', uselist=False)


# ================= Admin =================

class Admin(db.Model):
  __tablename__ = 'admins'
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('users.id'))
  user = relationship('User', back_populates='admin')


# ================= Doctor =================

class Doctor(db.Model):
  __tablename__ = 'doctors'
  id = Column(Integer, primary_key=True, autoincrement=True)
  dept_id = Column(Integer, ForeignKey('departments.id'))
  user_id = Column(Integer, ForeignKey('users.id'))

  user = relationship('User', back_populates='doctor')
  department = relationship('Department', back_populates='doctors')
  appointments = relationship(
      'Appointment',
      back_populates='doctor',
      cascade="all, delete-orphan"
  )


# ================= Patient =================

class Patient(db.Model):
  __tablename__ = 'patients'
  id = Column(Integer, primary_key=True, autoincrement=True)
  dob = Column(Date)
  user_id = Column(Integer, ForeignKey('users.id'))

  user = relationship('User', back_populates='patient')
  appointments = relationship(
      'Appointment',
      back_populates='patient',
      cascade="all, delete-orphan"
  )


# ================= Department =================

class Department(db.Model):
  __tablename__ = 'departments'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String)
  description = Column(String)
  doctors = relationship('Doctor', back_populates='department')


# ================= Appointment =================


class Appointment(db.Model):
  __tablename__ = 'appointments'
  id = Column(Integer, primary_key=True, autoincrement=True)
  patient_id = Column(Integer, ForeignKey('patients.id'))
  doctor_id = Column(Integer, ForeignKey('doctors.id'))
  date = Column(Date)
  time = Column(Time)
  status = Column(String, default='scheduled')  # scheduled, completed, canceled

  patient = relationship('Patient', back_populates='appointments')
  doctor = relationship('Doctor', back_populates='appointments')
  treatment = relationship(
      'Treatment',
      back_populates='appointment',
      uselist=False,
      cascade="all, delete-orphan"
  )


# ================= Treatment =================

class Treatment(db.Model):
  __tablename__ = 'treatments'
  id = Column(Integer, primary_key=True, autoincrement=True)
  appointment_id = Column(Integer, ForeignKey('appointments.id'), unique=True)
  diagnosis = Column(String)
  prescription = Column(String)
  tests = Column(String)
  notes = Column(String)

  appointment = relationship('Appointment', back_populates='treatment')
